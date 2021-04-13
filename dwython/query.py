import urllib
import uuid
import ssl
import http.client
from urllib.parse import urlparse
import json
import logging
import time
import requests
import ssl
from requests.adapters import HTTPAdapter
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib3.util.ssl_ import create_urllib3_context


log = logging.getLogger(__name__)

class SSLAdapter(HTTPAdapter):
    def __init__(self, certfile, keyfile, password=None, *args, **kwargs):
        self._certfile = certfile
        self._keyfile = keyfile
        self._password = password
        super(self.__class__, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs):
        context = create_urllib3_context()
        context.load_cert_chain(certfile=self._certfile,
                                keyfile=self._keyfile,
                                password=str(self._password))
        kwargs['ssl_context'] = context

class ResultSet:
    has_results = False
    query_id = None
    operation_time = 0
    wall_time = 0
    result_size = 0
    page_times = []
    events = []
    reponse_code=204
    session = None
    def __init__(self) -> None:
        self.operation_time = 0
        self.session = None
    
    def reset(self) -> None:
        self.has_results=False
        self.operation_time=0
        self.wall_time=0
        self.result_size=0
        self.events=[]
        self.response_code=204
        
class Query(object):

    query_logic = "EventQuery"
    begin_date = "19700101"
    end_date = "20990101"
    operation = "newQuery"

    default_content_type = 'application/x-www-form-urlencoded'

    json_content_type = 'application/json'

    url = 'https://localhost:8443/'

    current_result_set = None

    user_query = None

    query_name = None

    visibility = "BAR&FOO"

    cert_path = None
    key_path = None
    ca_cert = None
    key_pass = None

    endpoint = "DataWave/Query/"

    query_syntax =  'LUCENE'

    auths = "PUBLIC,fVATE,FOO,BAR,DEF,A,B,C,D,E,F,G,H,I,DW_USER,DW_SERV,DW_ADMIN,JBOSS_ADMIN"
    def __init__(self, query : str, cert_path : str = None, key_path : str = None, ca_cert : str = None, key_password : str = None, url : str = None, name : str = None) -> None:
        self.user_query = query
        if not name:
            self.query_name = str(uuid.uuid1())
        else:
            self.query_name = name
        self.cert_path = cert_path
        self.key_path = key_path
        self.ca_cert  = ca_cert
        self.key_pass = key_password

        if url is not None:
            self.url = url

    def with_url(self, url : str):
        if url is not None:
            self.url = url
        return self

    def with_cert(self, cert_path : str, key_path : str, key_password : str = None):
        self.cert_path = cert_path 
        self.key_path = key_path
        self.key_pass = key_password
        return self

    def with_begin(self, begin : str):
        self.begin_date = begin
        return self

    def with_end(self, end : str):
        self.end_date = end
        return self

    def with_query_logic(self, logic: str):
        self.query_logic = logic
        return self

    def with_syntax(self, syntax: str):
        self.query_syntax = syntax
        return self

    def __del__(self):
        if self.current_result_set is not None:
            self.close()

    def close(self, url : str = None):
        # close
        if self.current_result_set is not None and self.current_result_set.query_id is not None:
            if not url:
                url = self.url + self.endpoint + self.current_result_set.query_id + "/close"
            log.info("Closing query " + self.current_result_set.query_id)
            self.current_result_set.session.put(url)
            self.current_result_set.session = None
            self.current_result_set.query_id = None

    def _load_client(self):
        session = requests.Session()
        session.mount('https://', SSLAdapter(self.cert_path,  self.key_path, self.key_pass))
        session.verify=False
        return session

    def _build_query(self):
        return { "query" : self.user_query,
                 "queryName" : self.query_name,
                 "begin" : self.begin_date,
                 "end" : self.end_date,
                 "pagesize": 10,
                 "query.syntax" : self.query_syntax,
                 "auths" : self.auths,
                 "columnVisibility" : self.visibility}

    def next(self, url : str = None):
        if not self.current_result_set:
            raise RuntimeError("No Running Query")
        if not self.current_result_set.has_results:
            return self.current_result_set
        if not url:
            url = self.url + self.endpoint + self.current_result_set.query_id + "/next"
        headers = {'content-type': self.default_content_type, 'Accept': self.json_content_type}
        
        start_time = time.time()
        response = self.current_result_set.session.get(url=url, headers=headers)
        
        log.debug("Response code is " + str(response.status_code))
        self.current_result_set.reset()
        self.current_result_set.reponse_code = response.status_code
        
        if response.status_code == 200:
            decoded_response = response.text
            json_response = json.loads(decoded_response)
            self.current_result_set.has_results = json_response.get('HasResults',False)
            self.current_result_set.operation_time = json_response.get('OperationTimeMS',0)
            self.current_result_set.result_size = json_response.get('ReturnedEvents',0)
            self.current_result_set.events = json_response.get('Events',[])
            log.info("Received a 200 response code for " + self.current_result_set.query_id + " in " + str(self.current_result_set.operation_time) + " ms")
        self.current_result_set.wall_time = (time.time()-start_time)*1000
        self.current_result_set.page_times.append( self.current_result_set.wall_time )
        return self.current_result_set

    def create(self, url : str = None):
        if not url:
            url = self.url + self.endpoint + self.query_logic + "/createAndNext"
        headers = {'content-type': self.default_content_type, 'Accept': self.json_content_type}
        session = self._load_client()
        params = urllib.parse.urlencode(self._build_query())
        start_time = time.time()
        session.headers.update( headers )
        response = session.post(url=url, data=params)
        #session.request("POST",url,params, headers)
        log.debug("Response code is " + str(response.status_code))
        self.current_result_set = ResultSet()
        self.current_result_set.reponse_code = response.status_code
        self.current_result_set.session = session
        if response.status_code == 200:
            decoded_response = response.text
            json_response = json.loads(decoded_response)
            self.current_result_set.has_results = json_response.get('HasResults',False)
            self.current_result_set.query_id = json_response.get('QueryId',None)
            self.current_result_set.events = json_response.get('Events',[])
            self.current_result_set.operation_time = json_response.get('OperationTimeMS',0)
            self.current_result_set.result_size = json_response.get('ReturnedEvents',0)
            log.info("Received a 200 response code for " + self.current_result_set.query_id + " in " + str(self.current_result_set.operation_time) + " ms")
        self.current_result_set.wall_time = (time.time()-start_time)*1000
        self.current_result_set.page_times.append( self.current_result_set.wall_time )
        return self.current_result_set
