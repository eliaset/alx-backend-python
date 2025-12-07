# chats/views.py
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    # Optional: override create to handle participants dynamically
    def perform_create(self, serializer):
        # participants can be added via request.data['participants']
        serializer.save()


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Automatically set the sender as the logged-in user
        serializer.save(sender=self.request.user)
