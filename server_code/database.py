from pymongo import MongoClient
from uuid import uuid4
import time

MONGO_HOST = "ds247449.mlab.com"
MONGO_PORT = 47449
MONGO_DB = "homeautomation"
MONGO_USER = "ticatwolves"
MONGO_PASS = "ticatwolves1"
connection = MongoClient()#MONGO_HOST, MONGO_PORT)
#db = connection[MONGO_DB]

#connention = MongoClient('mongodb://<>:<>@:')

ref = connection[MONGO_DB]
#ref.authenticate(MONGO_USER, MONGO_PASS)
db = ref['users']

def setImage(id,image):
    try:
        db.update({'_id':id},{"$set":{'image_url':image}})
        return True
    except Exception as e:
        return e

def imageName(id):
    try:
        d = db.find({'_id':id},{'image_url':1})
        return d[0]
    except:
        return False
def addUser(name,email,password):
    try:
        db.insert({
            '_id':email,
            'name':name,
            'time':time.time(),
            'password':password,
            'id':str(uuid4()),
            'verify':False
        })
        return True
    except Exception as e:
        print(e)
        return False

def getPassword(email):
    try:
        data = db.find({'_id':email},{'password':1,'name':1,'id':1})
        return data[0]
    except Exception as e:
        print(e)
        return False

def addSensor(id,name,pin):
    try:
        db.update({'_id':id},{"$push":{"Sensor":{"name":name,"pin":pin,"status":0}}})
        return True
    except Exception as e:
        print(e)
        return False


def addAppliance(id,name,pin):
    try:
        db.update({'_id':id},{"$push":{"Appliances":{"name":name,"pin":pin,"status":0}}})
        return True
    except Exception as e:
        print(e)
        return False

def getAppliance(id):
    try:
        data = db.find({'_id':id},{"Appliances":1})
        print(id)
        return data[0]
    except Exception as e:
        print(e)
        return False

def getSensor(id):
    try:
        data = db.find({'_id':id},{"Sensor":1})
        print(id)
        return data[0]
    except Exception as e:
        print(e)
        return False

def updateAppliance(id,name,pin,index,op):
    try:
        if(op == "on"):
            print(pin +" On")
            db.update({'_id':id,'Appliances.name':name},{"$set":{"Appliances."+index+".status":0}})
        else:
            print(pin +" OFF")
            db.update({'_id':id,'Appliances.name':name},{"$set":{"Appliances."+index+".status":1}})
        return True
    except Exception as e:
        print(e)
        return False
def abc(id,index,op):
    try:
        if(op == 0):
            print("On in server")
            db.update({'_id':id},{"$set":{"Appliances."+str(index)+".status":1}})
        else:
            print("OFF in server")
            db.update({'_id':id},{"$set":{"Appliances."+str(index)+".status":0}})
        return True
    except Exception as e:
        print(e)
        return False

def changeName(id,name):
    try:
        db.update({'_id':id},{"$set":{'name':name}})
        return True
    except Exception as e:
        return e

def changeip(id,ip):
    try:
        db.update({'_id':id},{"$set":{'ip':ip}})
        return True
    except Exception as e:
        return e

def changemac(id,mac):
    try:
        db.update({'_id':id},{"$set":{'mac':mac}})
        return True
    except Exception as e:
        return e

def changeEmail(id,email):
    pass
def changePassword(id,password):
    try:
        db.update({'_id':id},{"$set":{'password':password}})
        return True
    except Exception as e:
        return e

def deleteAp(id,inde):
    try:
        db.update({'_id':id},{"$unset": {"Appliances."+str(inde)+"":1}})
        return True
    except Exception as e:
        print(e)
        return False

def addcontact(name,email,mess):
    try:
        db = ref['contact']
        db.insert({'message':mess,'name':name,'email':email})
        return True
    except Exception as e:
        return False

def getCamera(id):
    try:
        data = db.find({'_id':id},{"ip":1})
        return data[0]
    except Exception as e:
        return False