from re import search
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
User = get_user_model()
from .serializers import UserCreateSerializer,UserSerializer,UserProfileSerializer,RetrieveUsersSerializer,PicSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserAccount, UserProfile
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser



# from rest_framework.permissions import IsAuthenticated
from django.db.models import Q



class RegisterView(APIView):
    
    def post(self, request):
        data = request.data

        # instead of this
        # first_name = data['first_name']
        # last_name = data['last_name']
        # email = data['email']
        # password = data['password']

        # serializer = UserCreateSerializer(data={
            # first_name : first_name,
            # last_name : last_name,
            # email : email,
            # password : password
        # })

        serializer = UserCreateSerializer(data=data)
        
        if not serializer.is_valid() :
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data,status=status.HTTP_201_CREATED)




class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)


class TestView(APIView):
    def get(self, request):

        return Response({"Fetch": True},status=status.HTTP_200_OK)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['isSuperuser'] = user.is_superuser


        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        print(user)
        # profile = UserProfile.objects.filter(user=user.id)
        profile = user.userprofile_set.all()
        serializer = UserProfileSerializer(profile, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class RetrieveUsersView(APIView):
    def get(self, request):
        search = request.GET.get('search')
        print(search)
        if search:
            users = UserAccount.objects.exclude(is_staff=True).filter(
                
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search))
        else:
            users = UserAccount.objects.exclude(is_staff=True)

        print(users)
        serializer = RetrieveUsersSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class UpdateUserAPIView(APIView):
    def put(self, request, id):
        user_obj = UserAccount.objects.get(id=id)
        serializer = UserSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserAPIView(APIView):
    def delete(self, request, id):
        try:
            user_obj = UserAccount.objects.get(id=id)
            user_obj.delete()
            return Response("Delete successfully")
        except UserAccount.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserView(APIView):
    def get(self, request,id):
        users = UserAccount.objects.filter(id=id)
        print(users)
        serializer = RetrieveUsersSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




class UpdateProfileAPIView(APIView):
    def put(self, request, id):
        try:
            user_obj = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response("User profile not found", status=status.HTTP_404_NOT_FOUND)

        serializer = PicSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


