from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)


urlpatterns = [
    path('', include(router.urls))
]
