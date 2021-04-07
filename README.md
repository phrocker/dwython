# dwython
Dwython is a Datawave API interconnect within Python.

## Example

```python
user_query = query.Query(query = query,
    cert_path = cert, key_path = key, ca_cert=cacert, key_password=key_pass, url=url )
result = user_query.create()
print("{},{},{}".format(line,result.operation_time,result.wall_time))
result = user_query.next()
print("{},{},{}".format(line,result.operation_time,result.wall_time))
```