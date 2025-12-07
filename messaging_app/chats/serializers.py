# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'role']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested user info

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested participants
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
