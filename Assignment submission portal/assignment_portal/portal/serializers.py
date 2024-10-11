# portal/serializers.py
"""from rest_framework import serializers
from .models import User, Assignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_admin']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'user', 'task', 'admin', 'created_at', 'status', 'file']"""


# portal/serializers.py
from rest_framework import serializers
from .models import User, Assignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin']

class AssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # To show user information
    admin = UserSerializer(read_only=True)  # To show admin information

    class Meta:
        model = Assignment
        fields = ['id', 'user', 'task', 'admin', 'created_at', 'status', 'file']



