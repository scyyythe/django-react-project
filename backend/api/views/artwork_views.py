from rest_framework import generics
from api.models.artwork import  Art
from api.serializers.artwork_serializers import ArtSerializer 
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId
from api.models.users import User

class ArtCreateView(generics.ListCreateAPIView):
    queryset = Art.objects
    permission_classes=[IsAuthenticated]
    serializer_class = ArtSerializer
    
    def get_queryset(self):
        user = User.objects(id=self.request.user.id).first()
        
        print(f"Filtering artworks for user: {user.id} (Type: {type(user.id)})")  # Debugging

        if not user:
            return Art.objects.none()  # Return empty queryset if user not found

        return Art.objects.filter(artist=user)  # Use User object, not ObjectId
   
    
    def perform_create(self, serializer):
        print(f"User ID Type Before Query: {type(self.request.user.id)}")  # Debugging
        
        user = User.objects(id=self.request.user.id).first()  # Use MongoEngine query

        if not user:
            raise ValueError(f"User not found: {self.request.user.id}")  # Debugging

        print(f"User Found: {user.id} (Type: {type(user.id)})")  # Debugging

        if serializer.is_valid():
            serializer.save(artist=user)  # Save User object, not ObjectId
        else:
            print(serializer.errors)

            
class ArtDelete(generics.DestroyAPIView):
    serializer_class= ArtSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        return Art.objects.filter(artist=user) 