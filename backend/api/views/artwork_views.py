
from rest_framework import  generics
from rest_framework.permissions import AllowAny
from api.models.artwork import Art
from api.serializers.artwork_serializers import ArtSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ArtCreateView(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ArtSerializer

    def create(self, request, *args, **kwargs):
        print("DEBUG: Incoming Request Data =", request.data)  # Log request data
        print("DEBUG: User =", request.user)  # Log user details
        
        response = super().create(request, *args, **kwargs)
        
        print("DEBUG: Response Data =", response.data)  # Log response data
        return response


            
class ArtDelete(generics.DestroyAPIView):
    serializer_class= ArtSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        return Art.objects.filter(artist=user) 
