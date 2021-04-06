import requests
import urllib
import uuid
import ssl
import http.client
from urllib.parse import urlparse
import json
import logging


log = logging.getLogger(__name__)

class Query:

    query_logic = "EventQuery"
    begin_date = "19700101"
    end_date = "20990101"
    operation = "newQuery"

    default_content_type = 'application/x-www-form-urlencoded'

    json_content_type = 'application/json'

    url = 'https://localhost:8443/DataWave'

    query_id = None

    user_query = None

    query_name = None

    visibility = "BAR&FOO"

    cert_path = None
    key_path = None
    ca_cert = None
    key_pass = None

    auths = "PUBLIC,PRIVATE,FOO,BAR,DEF,A,B,C,D,E,F,G,H,I,DW_USER,DW_SERV,DW_ADMIN,JBOSS_ADMIN"
    def __init__(self, query : str, cert_path : str, key_path : str, ca_cert : str, key_password : str = None, name : str = None) -> None:
        self.user_query = query
        if not name:
            self.query_name = str(uuid.uuid1())
        else:
            self.query_name = name
        self.cert_path = cert_path
        self.key_path = key_path
        self.ca_cert  = ca_cert
        self.key_pass = key_password

    def __del__(self):
        if self.query_id is not None:
            self.close()

    def close(self, url : str = None):
        # close
        if self.query_id is not None:
            if not url:
                url = "/DataWave/Query/" + self.query_id + "/close"
            log.info("Closing query " + self.query_id)
            self._load_client().request(method="PUT",url=url)
            self.query_id = None

    def _load_client(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path ,password=self.key_pass)
        if self.ca_cert is not None:
            context.load_verify_locations(cafile=self.ca_cert)
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        url_parse = urlparse(self.url)
        connection = http.client.HTTPSConnection(url_parse.hostname, port=url_parse.port, context=context)
        return connection

    def _build_query(self):
        return { "query" : self.user_query,
                 "queryName" : self.query_name,
                 "begin" : self.begin_date,
                 "end" : self.end_date,
                 "pagesize": 10,
                 "query.syntax" : "LUCENE",
                 "auths" : self.auths,
                 "columnVisibility" : self.visibility}

    def create(self, url : str = None):
        if not url:
            url = "/DataWave/Query/" + self.query_logic + "/createAndNext"
        headers = {'content-type': self.default_content_type, 'Accept': self.json_content_type}
        connection = self._load_client()
        params = urllib.parse.urlencode(self._build_query())
        connection.request("POST",url,params, headers)
        response = connection.getresponse()
        if response.getcode() == 200:
            decoded_response = response.read().decode()
            json_response = json.loads(decoded_response)
            has_results = json_response.get('HasResults',False)
            self.query_id = json_response.get('QueryId',None)
            log.info("Received a 200 response code for " + self.query_id)
