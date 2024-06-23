from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound  # Import NotFound exception
from .models import ChatRoom, ChatMessage
from .serializer import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset for schema generation
            return ChatMessage.objects.none()
        room_id = self.kwargs.get('room_id')
        if room_id is None:
            raise NotFound(detail='room_id parameter is required.')
        return ChatMessage.objects.filter(room__id=room_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
