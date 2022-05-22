from rest_framework import serializers, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, password_validation
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from qms.utils import fetch_jwttoken_claims
from lib.pagination import QPagination
from django.http import Http404
from .models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


class UserAPIView(generics.GenericAPIView):
    pagination_class = QPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        elif self.request.method == "GET" or self.request.method == "DELETE" or self.request.method == "PUT":
            return [IsAuthenticated()]

    def get_object(self,pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
            user = User.objects.get(id=fetch_jwttoken_claims(request)['user_id'])
            response = {
                'user': UserSerializer(user,context={'request':request}).data
            }
            return Response(response, status=status.HTTP_200_OK)
        # if pk is not None:
        #     user = self.get_object(pk)
        #     response = {
        #         'user': UserSerializer(user).data
        #     }
        #     return Response(response, status=status.HTTP_200_OK)
        # else:
        #     users = User.objects.all().order_by('id')
        #     page = self.paginate_queryset(users)
        #     serializer = self.get_paginated_response(UserSerializer(page, many=True).data)
        #
        #     response = {
        #         'users': serializer.data
        #     }
        #     return Response(response, status=status.HTTP_200_OK)

    def post(self,request,pk=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**serializer.data)
            user.role = 2
            user.set_password(serializer.validated_data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            token = refresh.access_token
            token['user_id'] = user.id
            refresh['user_id'] = user.id
            token['role'] = user.role
            refresh['role'] = user.role
            response = {
                'access': str(token),
                'refresh': str(refresh)
            }
            return Response(response, status=status.HTTP_201_CREATED)

    # def put(self,request):
        user_id = fetch_jwttoken_claims(request)['user_id']
        instance = self.get_object(user_id)
        serializer = UserEditSerializer(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):

            user.name = serializer.validated_data.get('name', user.name)
            user.phone_number = serializer.validated_data.get('phone_number', user.phone_number)
            user.location = serializer.validated_data.get('location', user.location)
            user.image = serializer.validated_data.get('image', user.image)
            user.save()
            response = {
                'user': UserSerializer(user, context={'request': request}).data
            }
            return Response(response, status=status.HTTP_200_OK)
    

    # def delete(self,request,pk=0):
    #     instance = self.get_object(pk)
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginAPIView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user is None:
                return Response('invalid login credentials',status=status.HTTP_401_UNAUTHORIZED)
            else:
                if user.disable == True:
                    return Response('user disabled by Admin',status=status.HTTP_401_UNAUTHORIZED)
                refresh = RefreshToken.for_user(user)
                token = refresh.access_token
                token['user_id'] = user.id
                refresh['user_id'] = user.id
                token['role'] = user.role
                refresh['role'] = user.role
                return Response({
                    'refresh': str(refresh),
                    'access': str(token)
                })


# class ChangePasswordAPIView(generics.GenericAPIView):

#     def get_object(self,request):
#         payload = fetch_jwttoken_claims(request)
#         user = User.objects.get(id=payload['user_id'])
#         return user

#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object(request)
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'message': 'Password updated successfully',
#             }
#             return Response(response,status=status.HTTP_200_OK)