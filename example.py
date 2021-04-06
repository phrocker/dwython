import logging
from dwython import query
import argparse


parser = argparse.ArgumentParser(description='Example datawave query')
parser.add_argument('--key', dest='key', required=True)
parser.add_argument('--cert', dest='cert', required=True)
parser.add_argument('--cacert', dest='cacert')
parser.add_argument('--key_pass', dest='key_pass')
parser.add_argument('--query', dest='query', required= True)


args = parser.parse_args()


cert =args.cert
key =args.key
cacert = args.cacert
key_pass = args.key_pass

logging.basicConfig()

logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

query = query.Query(query = args.query,
                    cert_path = cert, key_path = key, ca_cert=cacert, key_password=key_pass )
query.create()