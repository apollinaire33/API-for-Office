from rest_framework import serializers
from .models import OfficeRoom, Employee


class OfficeRoomSerializer(serializers.ModelSerializer):
    waiting = 'waiting'
    backend = 'backend'
    frontend = 'frontend'
    fullstack = 'fullstack'
    CHOICES = (
        (backend, 'backend'), 
        (frontend, 'frontend'), 
        (fullstack, 'fullstack'), 
        (waiting, 'waiting'), 
    )

    free = 'free'
    unfree = 'unfree'
    ROOM_CHOICES = (
        (free, 'free'), 
        (unfree, 'unfree'), 
    )

    is_free = serializers.ChoiceField(choices=ROOM_CHOICES)
    category = serializers.ChoiceField(choices= CHOICES) 
    users = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field= 'username'
     )
    
    class Meta:
        model = OfficeRoom
        fields = ['id', 'name', 'seats_num', 'category', 'is_free', 'users']    


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'borrowed_rooms', 'borrowed_from', 'borrowed_to', 'history'] 
        read_only_fields = ['history']
  
        