from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.middleware.csrf import get_token



User = get_user_model()

@method_decorator(csrf_protect,name="dispatch")
class IsAuthenticated(APIView):
    def get(self,request,format=None):
        if User.is_authenticated:
            return Response({"success":"User is Authenticated"})
        else:
            return Response({"error":"User not Authenticated"})

@method_decorator(csrf_protect,name="dispatch")
class UserRegister(APIView):

    def post(self,request,format=None):
        data = self.request.data 

        print(data)
        
        username = data['username']
        email = data['email']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return Response({"error":"Username already exists"})
            elif User.objects.filter(email=email).exists():
                return Response({"error":"Email already exists"})
            else:
                if(len(password)<8):
                    return Response({"error":"Password should minimum of 8 characters"})
                else:
                    user = User.objects.create(email = email,username=username,password=password)
                    user.save()
                    return Response({"success":"User Created successfully"})
        else:
            return Response({"error":"Passwords didn't match!"})


@method_decorator(ensure_csrf_cookie,name="dispatch")
class GetCSRFToken(APIView):
    def get(self,request,format=None):
        return Response({"success":"CSRF cookie Set"})


@method_decorator(csrf_protect,name="dispatch")
class UserLogin(APIView):
    def post(self,request,format=None):
        data = self.request.data
        email = data['email']
        password = data['password']

        user = authenticate(self.request,email=email,password=password)
        
        if user is not None:
            login(self.request,user)
            return Response({"success":"Logged in Successfully!"})
        else:
            return Response({"error":"Invalid login credentials."})


@method_decorator(csrf_protect,name="dispatch")
class UserLogout(APIView):
    def post(self,request,format=None):
        try:
            logout(request)
            return Response({"success":"User Logged Out Successfully!"})
        except:
            return Response({"error":"Something went wrong when logging out"})