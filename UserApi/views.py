from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Create your views here.
class UserView(APIView):
    def post(self, request):
        user_data = request.data

        instance = User.objects.filter(username = user_data.get('username')) or None

        resposne_status = status.HTTP_200_OK

        #if username does not exists
        if not instance:
            user_serializer = UserSerializer(data=user_data)        
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
            user_serializer.save()
            resposne_status = status.HTTP_201_CREATED

        token = TokenObtainPairSerializer(data=user_data)
        if not token.is_valid():
            return Response(token.errors, status.HTTP_400_BAD_REQUEST)
            
        user_data.pop('password')
        access_token = token.validated_data['access']
        response = {**user_data, 'access' : access_token}
        return Response(response, resposne_status)
            
