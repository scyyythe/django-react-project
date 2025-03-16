from bson import ObjectId
from rest_framework import serializers
from api.models.artwork import Art
from datetime import datetime

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
    
    # update art
    def update(self, instance, validated_data):
        # Update the fields that are passed in the request
        instance.title = validated_data.get("title", instance.title)
        instance.category = validated_data.get("category", instance.category)
        instance.art_status = validated_data.get("art_status", instance.art_status)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        instance.updated_at = datetime.utcnow()  # Update the timestamp
        instance.save()
        return instance
    
    def to_representation(self, instance):
    
        return {
            "id": str(instance.id),
            "title": instance.title,
            "artist": str(instance.artist.id) if instance.artist else None,  # artist's id
            "category": instance.category,
            "art_status": instance.art_status,
            "price": instance.price,
            "description": instance.description,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }