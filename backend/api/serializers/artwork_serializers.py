from rest_framework import serializers
from api.models.artwork import User, Art
from bson import ObjectId

class ArtSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=100)
    artist = serializers.CharField()  # Expecting an ObjectId
    category = serializers.CharField(max_length=100)
    art_status = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """ Convert artist ID to ObjectId before saving """

      
        artist_id = validated_data.get("artist")

        # Validate artist ID
        if not ObjectId.is_valid(artist_id):
            raise serializers.ValidationError({"artist": "Invalid artist ID format"})

        validated_data["artist"] = ObjectId(artist_id)  

      

        art = Art(**validated_data)
        art.save()

       

        return art