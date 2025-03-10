import jwt
import datetime
import bcrypt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from api.models import User, Art
from api.serializers import UserSerializer , ArtSerializer 
from rest_framework.permissions import IsAuthenticated

# User Registration View
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class ArtCreateView(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = ArtSerializer
    
    def get_queryset(self):
        user=self.request.user
        return Art.objects.filter(artist=user)    
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(artist=self.request.user)
        else:
            print(serializer.errors)
            
class ArtDelete(generics.DestroyAPIView):
    serializer_class= ArtSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        return Art.objects.filter(artist=user) 

        
# Custom JWT Token View (Login)
class CustomTokenObtainPairView(APIView):
    """Handles JWT authentication for MongoEngine users"""

    def post(self, request):
        username, password = request.data.get("username"), request.data.get("password").encode("utf-8")

        # Find user in MongoDB and verify password
        user = User.objects(username=username).first()
        if not user or not bcrypt.checkpw(password, user.password.encode("utf-8")):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

     
        def generate_token(payload, exp_delta):
            payload.update({"exp": datetime.datetime.utcnow() + exp_delta, "iat": datetime.datetime.utcnow()})
            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Create access token
        access_token = generate_token({
            "user_id": str(user.id), 
            "username": user.username, 
            "jti": f"{user.id}_access"
        }, datetime.timedelta(hours=1))

        # Create refresh token
        refresh_token = generate_token({
            "user_id": str(user.id), 
            "jti": f"{user.id}_refresh"
        }, datetime.timedelta(days=7))

        # Return the access token, refresh token, user ID, and username in the response
        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user.id),
            "username": user.username
        }, status=status.HTTP_200_OK)



class CustomTokenRefreshView(APIView):
    """Handles JWT token refresh"""

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "refresh_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the refresh token and get the user from the database
            decoded_refresh_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects(id=decoded_refresh_token["user_id"]).first()
            
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Create a new access token
            access_token = jwt.encode({
                "user_id": str(user.id),
                "username": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                "iat": datetime.datetime.utcnow()
            }, settings.SECRET_KEY, algorithm="HS256")

            # Create a new refresh token
            refresh_token = jwt.encode({
                "user_id": str(user.id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
                "iat": datetime.datetime.utcnow()
            }, settings.SECRET_KEY, algorithm="HS256")

            # Return both tokens, along with user info
            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": str(user.id),
                "username": user.username
            }, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Refresh token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

