from bson import ObjectId
from rest_framework import generics, permissions
from api.models.artwork import Art
from api.models.users import User
from api.serializers.artwork_serializers import ArtSerializer

class ArtCreateView(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            mongo_user = User.objects.get(id=ObjectId(self.request.user.id))
        except Exception as e:
            print("Error retrieving MongoEngine user:", e)
            raise e

        serializer.save(artist=mongo_user)
