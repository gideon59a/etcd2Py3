# etcd2 clinet, using python3
# ex: python3 <this py file> [<etcd server ip address>]
#
import etcd
import json
import sys
import configparser
import os.path

#print ("argvs:", sys.argv[0],sys.argv[1],sys.argv[2])

if len(sys.argv) > 1:
    config_file_path = sys.argv[1]
else:
    config_file_path = 'etcd_client.conf'
config_file_exists = os.path.isfile(config_file_path)

TLS = False
HOST = '127.0.0.1'
if config_file_exists:
    config = configparser.ConfigParser()
    config.read('etcd_client.conf')
    #Get etcd server address
    if len(sys.argv) < 3:
        HOST = config['Server']['HOST']
    else:
        HOST = sys.argv[2]
    #Get TLS file names
    TLS  = "true" in (config['Security']['ETCD_CLIENT_CERT_AUTH']).lower() # A boolean
    CERT = config['Security']['ETCD_CLIENT_CERT_FILE'] # returns a string
    KEY  = config['Security']['ETCD_CLIENT_KEY_FILE'] # returns a string
    CA   = config['Security']['ETCD_TRUSTED_CA_FILE'] # returns a string
else:
    if len(sys.argv) > 2:
        HOST = sys.argv[2]

#print ("Server:",HOST,"TLS:",TLS)

def pjson(dictdata,dstr=""):
    print (dstr, json.dumps(dictdata,sort_keys=True,indent=4, separators=(',', ': ')))


class Etcd2Py3Cli:
    def __init__(self):
        if TLS:
            self.c0 = etcd.Client(host=HOST,port=2379,protocol='https', cert=(CERT,KEY),ca_cert=CA)
        else:
            self.c0 = etcd.Client(host=HOST,port=2379,protocol='http')

        try:
            print ("Connected to server ", HOST, "etcd version ",self.c0.version, "TLS:",TLS)
            print ("Cluster machines:", self.c0.machines, "\nCluster leader: ", self.c0.leader)
            print (" ")
        except:
            print (" *** Error conneting to etcd server. Exit.  ***")
            exit(1)

    def check_version(self):
        try:
            ver = self.c0.version
            print ("Connected. Server version ",ver)
        except:
            print ("Error")
            exit(1)
        retrun(0)

    def get_level_keys(self,dirstr):
        #Get just the single requested level, non-recursive
        try:
            level0 = self.c0.read(dirstr)

            ## print (dirstr," level: ",level0)
            #print ("Type: ",type(dirstr))
            #print ("\nJSON PRINT: ")
            #fails: print (json.dumps(level0,sort_keys=True,indent=4, separators=(',', ': ')))
        except etcd.EtcdKeyNotFound:
            print ("Error, no such dir")
            return 1
        return level0

    def pr_value(self,key):
        if hasattr(dir0,'key') and hasattr(dir0,'value'):
            if dir0.value != None:
                print (dir0.key, dir0.value)

    def get_top_keys(self):
        top0 = self.c0.read('/')
        top_keys=[]
        for item in top0._children:
            top_keys.append(item['key'])
        return (top_keys)

    def get_top_children(self):
        print ("printing all children: ")
        childs = []
        child_number = 0
        dir0 = self.c0.read('/',recursive = True)
        for child in dir0._children:
            childs.append(child)
            ###if hasattr(dir0,'key') and hasattr(dir0,'value'):
            ###    print (child['key'], child['value'])
            child_number += 1
            print_str = "Child " + str(child_number) + " : \n"
            pjson(child, print_str)
        ##x print("All children: \n",childs)

    def pr_key_val(self,_data):
        if hasattr(_data, 'key') and hasattr(_data, 'value'):
            if _data.value != None:
                print('"key":   ',_data.key,',\n"value": ', _data.value)

    def get_dir_tree(self,dirstr):
        try:
            dir0 = self.c0.read(dirstr,recursive = True)
            print ("dir0: ",dir0)
        except etcd.EtcdKeyNotFound:
            print ("Error, no such dir")
            return 1
        print("\nTHE REQUESTED DIRECTORY:")

        #pjson(dir0._children,"THE REQUESTED DIRECTORY: \n")

        self.pr_key_val(dir0) # print key+val at dir top level
        for child in dir0._children:
            pjson(dir0._children)
            if hasattr(child,'key') and hasattr(child,'value'):
                print (child['key'], child['value'])
        if dir0._children == []:
            print("No children. End of tree.")
        return 0

    def jprint_all_tree(self):
        return  

# ****************************************************************
# start:
	
e0 = Etcd2Py3Cli()

#write someting
#e0.c0.write('/branch1/n1', 1)
#e0.c0.write('/branch1/n2', 2)
#e0.c0.write('/branch1/dir2/m2', 20)
#e0.c0.write('/branch1/dir2/m3', 30)
#e0.c0.write('/branch1/dir2/dird3', 311)

top_level_keys = e0.get_top_keys()
print ("Top level keys: ")
pjson(top_level_keys)

if (input("\nEnter t to print all tree: ") == 't' ):
    e0.get_top_children()

goon = True
while goon:
    pjson(top_level_keys,"Top level keys: ")
    dirstr = input("\nEnter requested dir: ")
    #depth = input("Enter depth: ")
    if (dirstr != ""):
        print ("Requested: ",dirstr)
        dir = e0.get_dir_tree(dirstr) #get the directory tree and print it
    goon = (input("\nEnter any character to continue, or none to end: ") != "") # becomes false on null

print ("End.")
