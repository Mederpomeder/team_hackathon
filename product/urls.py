from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import ProductViewSet

router = DefaultRouter()
router.register('', views.ProductViewSet)

urlpatterns = [
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('likes/', views.LikeCreateView.as_view()),
    path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
    path('', include(router.urls)),
]