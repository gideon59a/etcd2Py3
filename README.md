etcd API V2 client using Python 3
etcd python module must be installed. I used python-etcd-0.4.5

run by:
# python3 etcd2py34ClinetTry2.py [<config file path string> [server ipv4 address string]]
Example:
# python etcd2py34ClinetTry2.py "etcd_client.conf" "127.0.0.1"

For TLS support a config file must be used. See example below.
If a non-localhost server is addressed, then run with the server address, e.g.:
# python3 etcd2py34ClinetTry2.py <config file path> "10.100.102.12"

Config file example:
[root@gCentos7 etcd2Py3CliP]# cat etcd_client.conf
# Edit this file for the etcd client
# *** NOTE: No string signs needed!
[Server]
HOST=127.0.0.1
[Security]
#ETCD_CLIENT_CERT_AUTH= False
#The following are relevant of the above is True
ETCD_CLIENT_CERT_FILE = /root/cfssl/client.pem
ETCD_CLIENT_KEY_FILE  = /root/cfssl/client-key.pem
ETCD_TRUSTED_CA_FILE  = /root/cfssl/ca.pem

