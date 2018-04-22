from pymongo import MongoClient
import gridfs
import time
from database import setImage
from bson.objectid import ObjectId
from PIL import Image
from io import StringIO,BytesIO
import mimetypes

connection = MongoClient()
database = connection['image']
# create a new gridfs object.
fs = gridfs.GridFS(database)

class ImageDB():
    def uploadImage(filename,id):
        print('Upload Image')
        with open(filename, 'rb') as f:
            thedata = f.read()
        # store the data in the database. Returns the id of the file in gridFS
        mime_type = mimetypes.guess_type(filename)
        fname = time.time()
        _id = fs.put(thedata,contentType=mime_type, filename=fname)
        print(str(_id))
        setImage(id,fname)
        # retrieve what was just stored. 
        #outputdata =fs.get(stored).read()
    def getImage(filename):
        """retrieve an image from mongodb gridfs"""
        if not fs.exists(filename=filename):
            raise Exception("mongo file does not exist! {0}".format(filename))        
        im_stream = fs.get_last_version(filename)
        im = Image.open(im_stream)
        img_io = BytesIO() 
        im.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return img_io
        
        #return serve_pil_image(im)

        #d = ObjectId('5ad204a5c2eb5d031a7fd7e5')        
        #connection = MongoClient()
        #database = connection['image']
        # create a new gridfs object.
        #fs = gridfs.GridFS(database)
        #outputdata = fs.get(d).read()
        #decode=outputdata#.decode()
        #return decode

'''def insert_image(request):
    with open(request.GET["image_name"], "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print encoded_string
    abc=db.database_name.insert({"image":encoded_string})
    return HttpResponse("inserted")
'''
def retrieve_image(request):
    pass
'''    data = db.database_name.find()
    data1 = json.loads(dumps(data))
    img = data1[0]
    img1 = img['image']
    decode=img1.decode()
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
    return HttpResponse(img_tag)
'''
# create an output file and store the image in the output file
#outfilename = "anony.png"
#output= open(outfilename,"w")
#output.write(outputdata)
#close the output file
#output.close()

"""
# for experimental code restore to known state and close connection
    #fs.delete(stored)
    #connection.drop_database('example');
#    print(connection.database_names())
    #connection.close()
"""
