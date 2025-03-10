from rest_framework import serializers
from api.models import User, Art
from datetime import datetime

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    role = serializers.CharField(max_length=100, required=False)
    user_status = serializers.CharField(max_length=100, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_username(self, value):
        if User.objects(username=value).first():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects(email=value).first():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        
        role = validated_data.get("role", "User")  
        user_status = validated_data.get("user_status", "Active") 

        created_at = validated_data.get("created_at", datetime.utcnow())
        updated_at = validated_data.get("updated_at", datetime.utcnow())

        # Create the user instance and pass the explicit created_at and updated_at
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=role, 
            user_status=user_status, 
            created_at=created_at,  
            updated_at=updated_at, 
        )
        user.set_password(validated_data["password"])  
        user.save()
        return user

    def to_representation(self, instance):
        """ Convert user instance to dictionary format """
        return {
            "id": str(instance.id),
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "role": instance.role,
            "user_status": instance.user_status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }



class ArtSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=100)
    artist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Linking to the User model
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
