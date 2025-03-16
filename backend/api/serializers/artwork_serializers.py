from bson import ObjectId
from rest_framework import serializers
from api.models.artwork import Art
from datetime import datetime
from api.models.users import User  
from api.models.interaction import Comment,Like


class ArtSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=100)
    artist = serializers.CharField(read_only=True)  
    category = serializers.CharField(max_length=100)
    art_status = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(art=obj)
        return [
            {
                "id": str(comment.id),
                "content": comment.content,
                "user": {
                    "id": str(comment.user.id),
                    "username": comment.user.username,
                    "email": comment.user.email
                },  # Include full user details
                "created_at": comment.created_at
            }
            for comment in comments
        ]


    def get_likes_count(self, obj):
        return Like.objects.filter(art=obj).count()

    def create(self, validated_data):
        art = Art(**validated_data)
        art.save()
        return art
    
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
            "comments": self.get_comments(instance),
            "likes_count": self.get_likes_count(instance)
        }
