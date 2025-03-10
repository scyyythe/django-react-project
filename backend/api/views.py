import jwt
import datetime
import bcrypt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from api.models import User  # Import your MongoDB User model
from api.serializers import UserSerializer  # Import your serializer

# ✅ User Registration View
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ✅ Custom JWT Token View (Login)
class CustomTokenObtainPairView(APIView):
    """Handles JWT authentication for MongoEngine users"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password").encode("utf-8")  # Encode password for bcrypt

        # Find user in MongoDB
        user = User.objects(username=username).first()
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ Verify hashed password with bcrypt
        if not bcrypt.checkpw(password, user.password.encode("utf-8")):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ Generate JWT tokens manually
        access_token_payload = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  
            "iat": datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_token_payload = {
            "user_id": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),  
            "iat": datetime.datetime.utcnow(),
        }
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")

        return Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            },
            status=status.HTTP_200_OK,
        )
