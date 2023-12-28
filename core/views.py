from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny



User = get_user_model()

@method_decorator(csrf_protect,name="dispatch")
class IsAuthenticated(APIView):
    permission_classes = [AllowAny]
    def get(self,request,format=None):
        if self.request.user.is_authenticated:
            return Response({"success":"User is Authenticated","id":self.request.user.id,"email":self.request.user.email})
        else:
            return Response({"error":"User not Authenticated"})

@method_decorator(csrf_protect,name="dispatch")
class UserRegister(APIView):
    permission_classes = [AllowAny]

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
                    user = User.objects.create(email = email,username=username)
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    return Response({"success":"User Created successfully"})
        else:
            return Response({"error":"Passwords didn't match!"})


@method_decorator(ensure_csrf_cookie,name="dispatch")
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self,request,format=None):
        return Response({"success":"CSRF cookie Set"})


@method_decorator(csrf_protect,name="dispatch")
class UserLogin(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request,format=None):
        data = self.request.data
        email = data['email']
        password = data['password']
        print(data)

        user = authenticate(self.request,email=email,password=password)

        print(user)
        
        if user is not None:
            login(self.request,user)
            return Response({"success":"Logged in Successfully!","id":user.id,"email":user.email})
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
        

class GetAllUsers(APIView):
    permission_classes = [AllowAny]
    def get(self,request,format=None):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)