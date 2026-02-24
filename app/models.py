from django.db import models
from django.contrib.auth.models import AbstractUser
from django_mongodb_backend.fields import ObjectIdAutoField
 
class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    ROLE_CHOICES = (('ADMIN', 'Admin'), ('USER', 'User'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    


class Train(models.Model):
    train_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    source = models.CharField(max_length=100, db_index=True)
    destination = models.CharField(max_length=100, db_index=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)



class SearchLog(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    endpoint = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    params = models.JSONField()
    user_id = models.IntegerField(null=True, blank=True)
    execution_time = models.FloatField() 
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_search_logs'
        managed = True




