import requests
import urllib
import uuid

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

    auths = "BAD_AUTH1,BAD_AUTH2"
    def __init__(self, query : str, name : str = None) -> None:
        self.user_query = query
        if not name:
            self.query_name = uuid.uuid1()
        else:
            self.query_name = name

    def __del__(self):
        if self.query_id is not None:
            self.close()

    def close(self, url : str = None):
        # close
        if self.query_id is not None:
            if not url:
                url = self.url
            url += "/Query/" + self.query_id + "/close"
            url += "/" + self.query_logic + "/createAndNext"
            requests.put(url, payoad=self._buildQuery())
            self.query_id = None

    def _build_query(self):
        query_return = dict()
        query_return['query'] = urllib.urlencode( self.user_query )
        query_return['queryName'] = self.query_name
        query_return['begin'] = self.begin_date
        query_return['end'] = self.end_date
        query_return['pagesize'] = 10
        query_return['query.syntax'] = 'LUCENE'
        query_return['auths'] = self.auths
        query_return['columnVisibility'] = urllib.urlencode(self.visibility)
        return query_return

    def create(self, url : str = None):
        if not url:
            url = self.url
        url += "/" + self.query_logic + "/createAndNext"
        headers = {'content-type': self.json_content_type, 'Accept': self.json_content_type}
        requests.post(url, payoad=self._build_query(), headers=headers)
           


"""
import requests
url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
payload = open("request.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=payload, headers=headers)
"""