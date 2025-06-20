from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostView, UserView

router = DefaultRouter()
router.register(r'user', UserView.UserViewset, basename='user')
router.register(r'blog',PostView.PostViewSet, basename='blog')

urlpatterns = [
    path('api/', include(router.urls)),
]
