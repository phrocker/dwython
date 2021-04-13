import logging
from dwython import query
import argparse
import os
import json
import tempfile


#https://stackoverflow.com/questions/14048948/how-to-find-a-particular-json-value-by-key
fp = tempfile.TemporaryFile()
fp.write(b'Hello world!')
print(fp.name)


parser = argparse.ArgumentParser(description='Example datawave query')
parser.add_argument('--query', dest='query', required= True)
parser.add_argument('-f', '--field', dest='field', action='append')
parser.add_argument('-s', '--syntax', dest='syntax')

pki_home = os.environ.get('DW_CLIENT_HOME') + "/pki/"
args = parser.parse_args()

query_string = args.query
fields = args.field
cert = pki_home + "testUser.pem"
key = pki_home + "testUser.key"
cacert = None #pki_home + "testUser.ca"
key_pass = os.environ.get('DW_CLIENT_TEST_CERT_PASS')
url = os.environ.get('DW_BASE_URI')

logging.basicConfig()

logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


syntax = args.syntax

if not syntax:
    syntax = "LUCENE"

user_query = query.Query(query = query_string,
            cert_path = cert, key_path = key, ca_cert=cacert, key_password=key_pass, url=url ).with_syntax(syntax)
ands = []
result = user_query.create()
if result.events is not None:
    for event in result.events:
        for field in event.get("Fields",[]):
            field_name = field.get("name","")
            value = field.get("Value",{})
            if field_name in fields:
                if value.get("value",""):
                    val = value.get("value","")
                    if syntax == "LUCENE":
                        ands.append(field_name +":\"" + val+ "\"")
                    else:
                        ands.append(field_name +"==\"" + val+ "\"")
print("{},{},{}".format(query_string,result.operation_time,result.wall_time))
for and_phrase in ands:
    if syntax == "LUCENE":
        new_query_string = query_string + " " + and_phrase 
    else:
        new_query_string = query_string + " && " + and_phrase 
    sub_query = query.Query(query = new_query_string,
                cert_path = cert, key_path = key, ca_cert=cacert, key_password=key_pass, url=url ).with_syntax(syntax)
    result = sub_query.create()
    print("{},{},{}".format(new_query_string,result.operation_time,result.wall_time))