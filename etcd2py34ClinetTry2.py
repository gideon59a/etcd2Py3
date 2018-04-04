# etcd2 clinet, using python3
# ex: python3 <this py file> [<etcd server ip address>]
#
import etcd
import json
import sys


#Get etcd server address
if len(sys.argv) < 2:
        HOST='127.0.0.1'
else:
        HOST=sys.argv[1]

#Get TLS file names
TLS = False
CERT_DIR="/root/cfssl/"
CERT=CERT_DIR+'client.pem'
KEY=CERT_DIR+'client-key.pem'
CA=CERT_DIR+'ca.pem'

def pjson(dictdata,dstr=""):
    print (dstr, json.dumps(dictdata,sort_keys=True,indent=4, separators=(',', ': ')))


class Etcd2Py3Cli:
    def __init__(self):
        if TLS:
            self.c0 = etcd.Client(host=HOST,port=2379,protocol='https', cert=(CERT,KEY),ca_cert=CA)
        else:
            self.c0 = etcd.Client(host=HOST,port=2379,protocol='http')
        #print ("Connected. Server version ",self.c0.version)
        
        try:
            print ("Connected to server ", HOST, "etcd version ",self.c0.version)
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

    def get_value(self,key): # ???
        if hasattr(dir0,'key') and hasattr(dir0,'value'):
            print (dir0.key, dir0.value)       

    def get_top_keys(self):
        top0 = self.c0.read('/')
        top_keys=[]
        for item in top0._children:
            top_keys.append(item['key'])
        return (top_keys)

    def get_top_children(self):
        childs = []
        dir0 = self.c0.read('/',recursive = True)
        for child in dir0._children:
            childs.append(child)
            ###if hasattr(dir0,'key') and hasattr(dir0,'value'):
            ###    print (child['key'], child['value'])
            pjson(child, "Child:\n")
        ##x print("All children: \n",childs)

    def get_dir_tree(self,dirstr):
        try:
            dir0 = self.c0.read(dirstr,recursive = True)
            #print ("dir0: ",dir0)
        except etcd.EtcdKeyNotFound:
            print ("Error, no such dir")
            return 1
        pjson(dir0._children,"THE REQUESTED DIRECTORY: \n")
        #x print ("THE REQUESTED DIRECTORY: ", dir0._children)

        dict={}
        dict['key'] = dir0.key
        if hasattr(dir0,'value'):
            dict['value'] = dir0.value
        print ("...dict: \n") 
        pjson(dict)

        if dir0._children == []:
            print("No children. End of tree.")
        for child in dir0._children:
            if hasattr(dir0,'key') and hasattr(dir0,'value'):
                print (child['key'], child['value'])

        return 0

    def jprint_all_tree(self):
        return  

#====================================================
	
e0 = Etcd2Py3Cli()

#write someting
e0.c0.write('/branch1/n1', 1)
e0.c0.write('/branch1/n2', 2)
e0.c0.write('/branch1/dir2/m2', 222)
e0.c0.write('/branch1/dir2/m3', 333)

top_level_keys = e0.get_top_keys()
print ("Top level keys: ")
pjson(top_level_keys)

e0.get_top_children()


''' temp
### Build a dict from the above result
print ("Level dict:")
level_dict = {}
for ki in top_level_keys:
    one_level = level_dict(ki, e0.get_value(ki))
    print (dirstr," level: ", one_level)
###pjson(level_dict)   

exit()
for level in top_level_keys:
    e0.get_level_keys(level)


#keypath = '/foo2'
#itsClass = e0.c0.read(keypath) 
#print ("itsClass: ",itsClass)
#print ("...")
#print (itsClass.value)

''' #end temp

goon = True
while goon:
    dirstr = input("Enter requested dir: ")
    if dirstr != "":
        #depth = input("Enter depth: ")
        print ("Requested: ",dirstr)
        dir = e0.get_dir_tree(dirstr)
    else:
        goon = False

