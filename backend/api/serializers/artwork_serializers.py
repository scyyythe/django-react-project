from bson import ObjectId
from rest_framework import serializers
from api.models.artwork import Art

class ArtSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=100)
    artist = serializers.CharField(read_only=True)  # Read-only; set automatically in the view
    category = serializers.CharField(max_length=100)
    art_status = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Do not attempt to convert the artist here.
        art = Art(**validated_data)
        art.save()
        return art
