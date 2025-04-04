from rest_framework import serializers
from api.models.users import User
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
        
        if self.instance and self.instance.username == value:
            return value
        
        if User.objects(username=value).first():
            raise serializers.ValidationError("This username is already taken.")
        return value

    
    def validate_email(self, value):

        if self.instance and self.instance.email == value:
            return value
        
        if User.objects(email=value).first():
            raise serializers.ValidationError("This email is already registered.")
        
        return value

    def create(self, validated_data):
        role = validated_data.get("role", "User")
        user_status = validated_data.get("user_status", "Active")

        created_at = validated_data.get("created_at", datetime.utcnow())
        updated_at = validated_data.get("updated_at", datetime.utcnow())

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

    # Update user
    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        instance.user_status = validated_data.get("user_status", instance.user_status)
        instance.updated_at = datetime.utcnow()

        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

    # Convert to JSON format for the response
    def to_representation(self, instance):
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
