#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from  django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view

def user_list(resquest):
 if resquest.method=='GET':
  try:
   Users=User.objects.all()
   Users_serializer=UserSerializer(Users,many=True)

   response={
    'message':"Get all Users'Infos Successfully",
    'Users':Users_serializer.data,
    'error':""
   }
   return JsonResponse(response,status=status.HTTP_200_OK)
  except:
   error={
    'message':"Fail! ->can NOT get all the Users list. Please check again.",
    'Users': "[]",
    'error': "Error"
   }
   return JsonResponse(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 elif resquest.method=='POST':
  try:
   User_data= JSONParser().parse(resquest)
   User_serializer=UserSerializer(data=User_data)

   if UserSerializer.is_valid():
    UserSerializer.save()
    print(User_serializer.data)
    response={
     'message':'Successfully Upload a User with id=%d' %User_serializer.data.get('id'),
     'Users':[User_serializer.data],
     'error':""
    }
    return JsonResponse(response,status=status.HTTP_201_CREATED)
   else:
    error={
     'message':"can NOT upload successfully",
     'Users':"[]",
     'error':User_serializer.errors
    }
    return JsonResponse(error,status=status.HTTP_400_BAD_REQUEST)
  except:
   exceptionError={
    'message':"Can NOT upload successfully",
    'Users': "[]",
    'error': "Having an exception"
   }
   return JsonResponse(exceptionError,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def user_detail(request,pk):
 try:
  user=User.objects.get(pk=pk)
 except User.DoesNotExist:
  exceptionError={
   'message': "NOT found a USER with id= %s" %pk,
   'Users': "[]",
   'error': "404 code - Not Found!"
  }
  return JsonResponse(exceptionError,status=status.HTTP_404_NOT_FOUND)
 if request.method=='PUT':
  try:
   User_data=JSONParser().parse(resquest)
   user_serializer=UserSerializer(user,data=User_data)

   if user_serializer.is_valid():
    user_serializer.save()
    response={
     'message': "Successfully Update a User with id = %s "%pk,
     'Users': [user_serializer.data],
     'error': ""
    }
    return JsonResponse(response)
   response={
    'message': "Fail to Update a User with id = %s" %pk,
    'Users':[user_serializer.data],
    'error': User_serializer.errors
   }
   return JsonResponse(response,status=status.HTTP_400_BAD_REQUEST)
  except:
   exceptionError={
    'message':"Fail to update a User with id = %s" %pk,
    'Users': [user_serializer.data],
    'error':"Internal Error"
   }
   return JsonResponse(exceptionError,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 elif request.method=='DELETE':
  print("Deleting a User with id = %s" %pk)
  user.delete()
  user_serializer= UserSerializer(user)
  response={
   'message':"Successfully Delete a User with id = %s" %pk,
   'Users': [user_serializer.data],
   'error': ""
  }
  return JsonResponse(response)









