from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
import base64
import random
import string
from .models import *
from django.http import JsonResponse
import cv2
from PIL import Image
import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
from django.shortcuts import redirect


from django.http import request
 
# Initialising database,auth and firebase for further use
interpreter = tflite.Interpreter(model_path = r"C:\Users\USER\Desktop\Projects\cpanel\novella\static\converted_model.tflite")
interpreter.allocate_tensors()
face_cascade = cv2.CascadeClassifier(r'C:\Users\USER\Desktop\Projects\cpanel\novella\static\face.xml')
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

emotions = ['Angry','Angry','Fear','Happy','Sad','Surprise','Happy']
@csrf_exempt
def index(request):
    if request.method == "POST":
        mood=[]
        data = request.body
        data = json.loads(data[0:len(data)])
        temp = len('data:image/jpeg;base64,')
        d=data[0]
        d = d[temp:len(d)]
        imgdata = base64.b64decode(d)
        filename = randomString()+'.jpg'  # I assume you have a way of picking unique filenames
        with open('media/'+filename, 'wb') as f:
                f.write(imgdata)
        im=cv2.imread('media/'+filename)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im=gray
        faces = face_cascade.detectMultiScale(
        im,  
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
        print(im.shape,faces)
        (x, y, w, h)=(0,0,0,0)
        if(len(faces)>0):
            (x, y, w, h)=faces[0]
            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 0, 255), 2)
            faces = im[y:y + h, x:x + w]
            cv2.imwrite('media/'+filename, faces)
            im=cv2.imread('media/'+filename)
            im=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
            resized=im.reshape(im.shape)
            resized=cv2.resize(resized,(48,48))
            resized=resized.reshape(48,48,1)
            im = resized.astype(np.float32)
            
            print(im)
            input_data = np.array([im])
            input_shape = input_details[0]['shape']
            interpreter.set_tensor(input_details[0]['index'], input_data)

            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            

            ems=emotions[np.argmax(output_data,axis=1)[0]]
            print(ems)
            request.session['curr_emo']=ems

            
            print(output_data)
        else:
            return JsonResponse({'data': 'fail'})
        return JsonResponse({'data': 'Success'})
    return render(request, 'index.html')


from django.template  import Context, Template
def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def home(request):
    return render(request,'home.html')



def story(request):
    return render(request,'storyselect.html')
from django.http import HttpResponse
from django.template import loader

def x(request):
    data=pd.read_csv(r'C:\Users\USER\Desktop\Projects\cpanel\novella\static\final.csv')
    template = loader.get_template('reading.html')
    sr=data.loc[data['5']==request.session['curr_emo']].sample().values[0]
    title=sr[1]
    stry=sr[5].replace("[Illustration]"," ")
    stry=stry.split("--")
    print(len(stry))
    ls=[]
    for i in range(0,len(stry)):
        if(i%2==0):
            ls.append(True)
        else:
            ls.append(False)
    mylist = zip(ls, stry)
    context = {
        'title':title,
        'data': mylist,
    }
    #template = Template(" {{ sr }}.")
    return render(request, 'reading.html', context)
# Create your views here.


