from bson import ObjectId
from rest_framework import serializers
from api.models.artwork import Art
from datetime import datetime
from api.models.users import User  # For artist reference
from api.models.interaction import Comment,Like  # For referencing comments

class CommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    user = serializers.CharField(read_only=True)  # We will set this automatically in the view
    art = serializers.CharField(write_only=True)  # Take the art ID in the request body
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Set the user and art based on the request
        user = validated_data.get('user')  # Get the logged-in user
        art_id = validated_data.get('art')  # Get the art ID
        art = Art.objects.get(id=art_id)  # Get the artwork instance

        comment = Comment(
            content=validated_data['content'],
            user=user,
            art=art
        )
        comment.save()
        return comment
    

class LikeSerializer(serializers.Serializer):
    user = serializers.CharField(read_only=True)  # We will set this automatically in the view
    art = serializers.CharField(write_only=True)  # Take the art ID in the request body
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Set the user and art based on the request
        user = validated_data.get('user')  # Get the logged-in user
        art_id = validated_data.get('art')  # Get the art ID
        art = Art.objects.get(id=art_id)  # Get the artwork instance

        like = Like(user=user, art=art)
        like.save()
        return like
