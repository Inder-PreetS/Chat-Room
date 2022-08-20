from django.db import models

# Create your models here.

class Room(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    visitors = models.IntegerField()

    def __str__(self):
        return self.title


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message