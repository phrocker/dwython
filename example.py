import logging
from dwython import query
import argparse


parser = argparse.ArgumentParser(description='Example datawave query')
parser.add_argument('--key', dest='key', required=True)
parser.add_argument('--cert', dest='cert', required=True)
parser.add_argument('--cacert', dest='cacert')
parser.add_argument('--key_pass', dest='key_pass')
parser.add_argument('--queryFile', dest='queryFile', required= True)


args = parser.parse_args()


cert =args.cert
key =args.key
cacert = args.cacert
key_pass = args.key_pass

logging.basicConfig()

logging.root.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)


with open(args.queryFile) as fp:
    line = fp.readline()
    while line:
        line = line.strip()
        user_query = query.Query(query = line,
                        cert_path = cert, key_path = key, ca_cert=cacert, key_password=key_pass )
        result = user_query.create()
        if result is not None:
            print("{},{}".format(line,result.operation_time))
        else:
            print("{},{}".format(line,0))
        line = fp.readline()