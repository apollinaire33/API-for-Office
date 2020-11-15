from django.db import models
from django.db.models import F
from django.http import HttpResponseServerError
from django.contrib.postgres.fields import JSONField


class OfficeRoom(models.Model):

    waiting = 'waiting'
    backend = 'backend'
    frontend = 'frontend'
    fullstack = 'fullstack'
    CATEGORY_CHOICES = (
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

    is_free = models.CharField(max_length=50, choices = ROOM_CHOICES, default='-') 
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES, default='-') 
    name = models.CharField(max_length=50)
    seats_num = models.IntegerField()

    def __str__(self):
        return self.name    


class Employee(models.Model):
    username = models.CharField(max_length=30)
    borrowed_rooms = models.ForeignKey(OfficeRoom, related_name='users', on_delete=models.SET(1), blank=True, null=True)
    borrowed_from = models.DateTimeField(null=True, blank=True)
    borrowed_to = models.DateTimeField(null=True, blank=True)
    history = models.CharField(max_length=30000, null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        curr_room = OfficeRoom.objects.get(pk=self.borrowed_rooms_id)
        if curr_room.seats_num != 0: 
            if self.borrowed_from < self.borrowed_to:
                if not self.pk:
                    OfficeRoom.objects.filter(pk=self.borrowed_rooms_id).update(seats_num=F('seats_num')-1)
                    if curr_room.seats_num == 1:
                        OfficeRoom.objects.filter(pk=self.borrowed_rooms_id).update(is_free='unfree')       
                elif self.pk:
                    prev_room = Employee.objects.get(pk=self.pk)
                    OfficeRoom.objects.filter(pk=prev_room.borrowed_rooms_id).update(seats_num=F('seats_num')+1)
                    OfficeRoom.objects.filter(pk=self.borrowed_rooms_id).update(seats_num=F('seats_num')-1)
                    if curr_room.seats_num == 1:
                        OfficeRoom.objects.filter(pk=self.borrowed_rooms_id).update(is_free='unfree')
                    else:
                        OfficeRoom.objects.filter(pk=prev_room.borrowed_rooms_id).update(is_free='free')   
                super().save(*args, **kwargs) 
            elif self.borrowed_from > self.borrowed_to:
                raise Exception('Expiry date cannot be greater than created date')
        elif curr_room.seats_num == 0:
            raise Exception('No free places, try to find another room')

  
        