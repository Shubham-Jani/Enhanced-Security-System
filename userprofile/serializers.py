from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
import base64


class FaceEncodingsSerializer(serializers.Field):
    def to_representation(self, value):
        # Convert binary data to base64 string
        return base64.b64encode(value).decode('utf-8')

    def to_internal_value(self, data):
        # Convert base64 string back to binary data
        return base64.b64decode(data)


class ProfileSerializer(serializers.ModelSerializer):
    face_encodings = FaceEncodingsSerializer()

    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()
    date_joined = serializers.DateTimeField(read_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username",
                  "password", "date_joined", "is_staff", "profile"]
