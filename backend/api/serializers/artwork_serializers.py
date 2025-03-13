from rest_framework import serializers
from api.models.artwork import User, Art
from bson import ObjectId

class ArtSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=100)
    artist = serializers.CharField()
    category = serializers.CharField(max_length=100)
    art_status = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """ Create a new art instance """
        art = Art(
            title=validated_data["title"],
            artist=validated_data["artist"],
            category=validated_data["category"],
            art_status=validated_data["art_status"],
            price=validated_data["price"],
            description=validated_data.get("description", ""),
        )
        art.save()
        return art

    def to_representation(self, instance):
        """ Convert art instance to dictionary format """
        # Get the artist's username from the artist reference
        artist_username = instance.artist.username if instance.artist else None
        
        return {
            "id": str(instance.id),
            "title": instance.title,
            "artist": {
                "id": str(instance.artist.id) if instance.artist else None,
                "username": artist_username
            },
            "category": instance.category,
            "art_status": instance.art_status,
            "price": instance.price,
            "description": instance.description,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }