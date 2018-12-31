
from django.shortcuts import render 
import pyrebase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

config = {
    'apiKey': "AIzaSyAM78zG2ciOXV0a4CexJCcyvMGLCyDzLWs",
    'authDomain': "platedetectorproject.firebaseapp.com",
    'databaseURL': "https://platedetectorproject.firebaseio.com",
    'projectId': "platedetectorproject",
    'storageBucket': "platedetectorproject.appspot.com",
    'messagingSenderId': "824986743444"
  }


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


def SignIn(request):
    return render(request, "SignIn.html")


def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"SignIn.html",{"messg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "welcome.html",{"e":email})


def logout_user(request):
    logout(request)
    return render(request,'SignIn.html')    

def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data={"name":name,"status":"1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
        

    
    return render(request,"signIn.html")




def create(request):

    return render(request,'create.html')


def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress =request.POST.get('progress')

    idtoken= request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        'progress':progress
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})    