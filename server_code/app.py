from flask import Flask,render_template,request,redirect,url_for,session,flash,jsonify,send_file,Response
from flask_socketio import SocketIO,emit
from functools import wraps
from werkzeug.utils import secure_filename
from wtforms import TextField,Form,validators,PasswordField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
#from pymysql import escape_string as thwart
from database import addUser,getPassword,changeName,changePassword,addAppliance,addSensor,getAppliance,getSensor,updateAppliance,abc,changeip,imageName,deleteAp,addcontact,changemac,getCamera
import gc
import time
import uuid
import os
import datetime
from ImageDatabase import ImageDB


UPLOAD_FOLDER = '/home/ticat/Projects'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socket = SocketIO(application)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/')
def index():
    if 'logged' in session:
        return redirect(url_for('appliances'))
    return render_template('index.html')

@application.route('/about/')
def about():
    return render_template('about.html')

@application.route('/android/')
def android():
    return render_template('android.html')

class ContactForm(Form):
    name = TextField("Name",[validators.DataRequired(),validators.Length(min=5, max=30)])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    message = TextField("Message",widget=TextArea())
    
@application.route('/contact/',methods=['POST','GET'])
def contact():
    try:
        form = ContactForm(request.form)
        if request.method == "POST" and form.validate():
            name = form.name.data
            email = form.email.data
            message = form.message.data
            if addcontact(name,email,message):
                return redirect(url_for('login'))
    except Exception as e:
        print(e)
    return render_template('contact.html',form=form)

@application.route('/how-to-use/')
def howtouse():
    return render_template('how_to_use.html')

@application.route('/forgetpass/')
def forgetpass():
    return render_template('index.html')


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@application.route('/Logout/')
@login_required
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for('index'))

@application.route('/login/',methods=['POST','GET'])
def login():
    if 'logged' in session:
        return redirect(url_for('appliances'))
    try:
        if request.method == 'POST':
            pa = getPassword(email=request.form['email'])
            if sha256_crypt.verify(request.form['password'], pa['password']):
                session['logged'] = True
                session['email'] = pa['_id']
                session['name'] = pa['name']

                return redirect(url_for('appliances'))
            else:
                flash("ID Password not Match")
        gc.collect()
    except Exception as e:
        print(e)
    return render_template('login.html')


class SignUpForm(Form):
    name = TextField("Name",[validators.Length(min=5, max=30)])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password",[validators.Required(),validators.EqualTo('confirm',message="Password must match.")])
    confirm = PasswordField('Repeat Password')

@application.route('/signup/',methods=['POST','GET'])
def signup():
    if 'logged' in session:
        return redirect(url_for('appliances'))
    try:
        form = SignUpForm(request.form)
        if request.method == "POST" and form.validate():
            name = form.name.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            response = addUser(name,email,password)
            if response:
                return redirect(url_for('login'))
    except Exception as e:
        print(e)
    return render_template('signup.html', form=form)

@application.route('/Applicances/')
@login_required
def appliances():
    conte = []
    try:
        conte = getAppliance(session['email'])['Appliances']
    except Exception as e:
        pass
    ctime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    return render_template('theme/appliances.html',data = conte)

@application.route('/Sensors/')
@login_required
def sensors():
    ctime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    return render_template('theme/sensor.html')#,switch = [ctime])
@application.route('/LiveView/')
@login_required
def camera():
    ctime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
    return render_template('theme/camera.html')#,switch = [ctime])

@application.route('/pic/')
def getIMage():
    imagename = imageName(session['email'])
    imagedata = ImageDB.getImage(imagename['image_url'])
    return send_file(imagedata, mimetype='image/jpeg')

@application.route('/Profile/')
@login_required
def profile():
    try:
        return render_template('theme/profile.html')
    except Exception as e:
        print("error")
        print(e)
        pass
    #return "Hello"
    return render_template('theme/profile.html')#,data=imagedata)

@application.errorhandler(404)
def page_not_found(e):
    return render_template('/errors/404.html')

@application.errorhandler(405)
def method_not_allowed():
    return render_template('/errors/405.html')

@application.errorhandler(500)
def internal_server_error(e):
    return render_template('/errors/500.html')

def toggle_switch(uid,bu,pin):
    pass


#MobileRoutes
@application.route('/m/contact/',methods=['GET','POST'])
def contactff():
    try:
        if request.method == 'POST':
            rawname = request.form['name']
            rawemail = request.form['email']
            message = request.form['message']
            response = addcontact(rawname,rawemail,message)
            if response:
                return jsonify(success="successfully",status = True)
            else:
                return jsonify(status=False,error="error try later")
        gc.collect()
    except Exception as e:
        print(e)
        return jsonify(error="Please check later",status = False)

@application.route('/m/signup/',methods=['GET','POST'])
def mobileregistration():
    try:
        if request.method == 'POST':
            rawname = request.form['name']
            rawemail = request.form['email']
            rawpassword = request.form['password']
            password = sha256_crypt.encrypt((str(rawpassword)))
            response = addUser(rawname,rawemail,password)
            if response:
                return jsonify(success="You are registered successfully",status = True)
            else:
                return jsonify(status=False,error="Already exist")
        gc.collect()
    except Exception as e:
        print(e)
        return jsonify(error="Please check later",status = False)

@application.route('/m/login/',methods=['GET','POST'])
def mobilelogin():
    try:
        if request.method == 'POST':
            rawemail = request.form['email']
            rawpassword = request.form['password']
            pa = getPassword(email=rawemail)
            print(str(pa['password']))
            if sha256_crypt.verify(rawpassword, pa['password']):
                return jsonify(name=pa['name'],email=pa['_id'],userid=pa['id'],mac = "1512121",success = "Welcome to your account",status=True)
            else:
                return jsonify(error="Wrong password or email id")
        gc.collect()
    except Exception as e:
        print(e)
        return jsonify(error="Please check later")
    return jsonify(error="Server Error Please try later")

@application.route('/m/update/',methods=['GET','POST'])
def mobileupdate():
    try:
        if request.method == 'POST' or request.method == 'GET':
            t = request.args.get('type')
            if t == "name":
                if changeName(request.form['id'],request.form['update']):
                    print("Changed")
                    return jsonify(status = True,success="Succefully changed")
                else:
                    return jsonify(status = False, error="Try Later")
            if t == "password":
                if changePassword(request.form['id'],sha256_crypt.encrypt(request.form['update'])):
                    print("changed")
                    return jsonify(status=True, success="Succefully changed")
                else:
                    return jsonify(status=False, error="Try Later")
            if t == "ip":
                if changeip(request.form['id'],request.form['update']):
                    print("changed")
                    return jsonify(status=True, success="Succefully changed")
                else:
                    return jsonify(status=False, error="Try Later")
            if t == "mac":
                if changemac(request.form['id'],request.form['update']):
                    print("changed")
                    return jsonify(status=True, success="Succefully changed")
                else:
                    return jsonify(status=False, error="Try Later")
 

    except Exception as e:
        print(e)
        return jsonify(error="Please check later",status = False)

@application.route('/m/add_device/',methods=['GET','POST'])
def mobileaddDevice():
    try:
        if request.method == 'POST' or request.method == "GET":
            ty = request.args.get("type")
            if ty == "Sensor":
                if addSensor(request.form['id'],request.form['name'],request.form['pin']):
                    return jsonify(status = True,success = "Sensor Successfully Added")
            elif ty == "Appliance":
                if addAppliance(request.form['id'],request.form['name'],request.form['pin']):
                    return jsonify(status = True,success = "Appliance Successfully Added")
    except Exception as e:
        print(e)
        return jsonify(error="Please check later")
    return jsonify(error="Server Error Please try later")

@application.route('/m/getDevice/',methods=['GET','POST'])
def mobilegetDevice():
    try:
        if request.method == 'POST' or request.method == "GET":
            id = request.args.get("id")
            typ = request.args.get("type")
            if typ == "Appliance":
                return jsonify(data = getAppliance(id))
            if typ == "Sensor":
                return jsonify(data = getSensor(id))
    except Exception as e:
        print(e)
        return jsonify(error="Please check later")
    return jsonify(error="Server Error Please try later")

@application.route('/m/getDeviceIP/',methods=['GET','POST'])
def mobilegetDeviceIP():
    try:
        if request.method == 'POST' or request.method == "GET":
            id = request.args.get("id")
            return jsonify(data = getCamera(id))
    except Exception as e:
        print(e)
        return jsonify(error="Please check later")
    return jsonify(error="Server Error Please try later")

@application.route('/m/operateDevice/',methods=['GET','POST'])
def mobileOperateDevice():
    try:
        if request.method == 'POST' or request.method == "GET":
            id = request.args.get("id")
            typ = request.args.get("type")
            pin = request.form['pin']
            index = request.form['index']
            name = request.form['name']
            op = request.form['op']
            if typ == "Appliance":
                print("Im in")
                if updateAppliance(id,name,pin,index,op):
                    print("bilol")
                    try:
                        if (op == "off"):
                            emit('abcdef', {'data': 'foo'}, namespace='/bc',broadcast=True)
                        else:
                            emit('abc',{'data':'foo'},namespace='/cd',broadcast=True)
                        print("ill emit")
                    except Exception as e:
                        print("DATA = "+str(e))
                    #mit('abc', {'pin': 10}, broadcast=True)
                    return jsonify(status = True,success = "done")
                else:
                    print("error")
                    return jsonify(status = False,success = "Sorry")
    except Exception as e:
        print(e)
        return jsonify(error="Please check later")
    return jsonify(error="Server Error Please try later")


@application.route('/m/upload/', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'pofile_pic' not in request.files:
            print('No file Selected')
        f = request.files['pofile_pic']
        if f.filename == '':
            print("No file Selected")
        if f and allowed_file(f.filename):
            print("something")
            filename = secure_filename(f.filename)
            f.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            try:
                ImageDB.uploadImage(os.path.join(application.config['UPLOAD_FOLDER'], filename),session['email'])
            except:
                id = request.args.get("email")
                print(id)
                ImageDB.uploadImage(os.path.join(application.config['UPLOAD_FOLDER'], filename),id)                
            #return redirect(url_for('profile'))
            return jsonify(sucess = "File Sucessfully uploaded")
    return jsonify(error = "Error")

@application.route('/m/changepass/', methods = ['GET', 'POST'])
def changepass():
    if request.method == 'POST':
        password = sha256_crypt.encrypt((str(request.form['passwo'])))
        id = session['email']
        if changePassword(id,password):
            print("Success fully done")
    return redirect(url_for('index')) 
    

#########################################################
#Sockets are here
#########################################################
@socket.on('addit')
def handle(data):
    print(str(data['name']))
    print(str(data['pin']))
    if addAppliance(session['email'],data['name'],data['pin']):
        print(session['email']+"   added")
        emit('response',{'status':True})
    else:
        emit('response',{'status':False})

@socket.on('deleteit')
def handle(data):
    index = data['index']
    id = session['email']
    if (deleteAp(id,index)):
        socket.emit("deleted",{'status':True})


@socket.on('updateip')
def handle(data):
    ip = data['ip']
    id = session['email']
    if changeip(id,ip):
        print("Success fully done")
        socket.emit('response',{'status':True})

'''@socket.on('updatepassword')
def handle(data):
    password = data['word']
    id = session['email']
    if changePassword(id,password):
        print("Success fully done")
        socket.emit('response',{'status':True})
'''

@socket.on('updatename')
def handle(data):
    name = data['uname']
    id = session['email']
    print(name)
    if changeName(id,name):
        print("Success fully done")
        socket.emit('nameresponse',{'status':True})
        #session['name'] = name


@socket.on('updateit')
def handle(data):
    index = data['index']
    id = session['email']
    op = data['operation']
    print(type(op))
    if abc(id,index,op):
        try:
            if(op == 0):
                print("ON")
                emit('operate', {'pin': 20,'operate':True,'accesscode':'access code here'}, namespace='/operate',broadcast=True)
            else:
                emit('operate', {'pin': 20,'operate':False,'accesscode':'access code here'}, namespace='/operate',broadcast=True)
                print("OFF")
        except Exception as e:
            print("DATA = "+str(e))
            #mit('abc', {'pin': 10}, broadcast=True)
        #return jsonify(status = True,success = "done")
    else:
        print("error")
        #return jsonify(status = False,success = "Sorry")
@application.route('/live/')
def getLive():
    pass
    #emit('getlive',namespace='/liveme',broadcast=True)
    #@socket.on('stream')
    #def handle(streamdata):
    #    return Response(streamdata(0)['data'], mimetype='multipart/x-mixed-replace; boundary=frame')

@socket.on('stream')
def handle(streamdata):
    print(streamdata)
    return Response(streamdata(0)['data'], mimetype='multipart/x-mixed-replace; boundary=frame')

#@socket.on('stream')
#def handle(streamdata):
    

if __name__=='__main__':
    application.secret_key = "modfodscdksnckdcnkdsmsxalxm"
    socket.run(application,host = '192.168.43.147',port=5000)
#172.16.72.1 host="192.168.43.147",

