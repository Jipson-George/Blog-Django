from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostView, UserView

router = DefaultRouter()
router.register(r'users', UserView.UserViewset, basename='user')
router.register(r'posts', PostView.PostViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]
