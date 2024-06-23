from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet)
router.register(r'rooms/(?P<room_id>[^/.]+)/messages',
                ChatMessageViewSet, basename='room-messages')

urlpatterns = [
    path('', include(router.urls)),
]
