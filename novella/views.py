from django.shortcuts import render
import pyrebase
from django.shortcuts import redirect
import cv2
import threading

config={
    'apiKey': "AIzaSyAwoegyEpEvJQQCiRnCivFUruYwn35nRnc",
    'authDomain': "story-tell-f239d.firebaseapp.com",
    'databaseURL': "https://story-tell-f239d-default-rtdb.firebaseio.com/",
    'projectId': "story-tell-f239d",
    
    'storageBucket': "story-tell-f239d.appspot.com",
    'messagingSenderId': "445859516878",
   'appId': "1:445859516878:web:d3ec015d5dad5d3a155b9f",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
 

def signIn(request):
    return render(request,"login.html")
def getstarted(request):
    return render(request,"getstarted.html")

def signUp(request):
    return render(request,"Registration.html")
 
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        print(email,'***')
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        print(email,'***')
        uid = user['localId']
        print(email,'***')
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html")
     return render(request,"Login.html")

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    print(email,pasw)
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    print(str(session_id))
    return redirect('/home/')
    #return render(request,"getstarted.html",{"email":email})
 
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")
 