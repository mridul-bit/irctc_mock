from rest_framework import serializers
from .models import User, Train, Booking

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name') 
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # We use set_password to ensure the password is cryptographically hashed
        password = validated_data.pop('password')
        validated_data['username'] = validated_data.get('email')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    # Nested serializer to include train details in the GET response
    train_details = TrainSerializer(source='train', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'train', 'train_details', 'seats_booked', 'booking_date']
        read_only_fields = ['user', 'booking_date']