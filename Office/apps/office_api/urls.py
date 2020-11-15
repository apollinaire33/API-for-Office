from .views import OfficeRoomViewSet, EmployeeViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('office', OfficeRoomViewSet, basename='rooms')

router1 = DefaultRouter()
router1.register('users', EmployeeViewSet, basename='users')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/<int:pk>/', include(router.urls)),

    path('api/', include(router1.urls)),
    path('api/<int:pk>/', include(router1.urls)),
]