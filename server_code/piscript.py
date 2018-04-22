from socketIO_client import SocketIO,BaseNamespace

class Button(BaseNamespace):
    def on_aaa_response(self, *args, **kwargs):
        print('on_aaa_response', args)

def func(*args,**kwargs):
    try:
        data = args[0]
        pin = data['pin']
        access_code = data['accesscode']
        operate = data['operate']
        if operate:
            print("On")
        else:
            print("Off")
        #for name, value in data.items():
        #    print( '{0} = {1}'.format(name, value))
    except Exception as e:
        print(e)

socketIO = SocketIO('127.0.0.1', 5000)
button = socketIO.define(Button, '/operate')

button.on('operate', func)

socketIO.wait()

