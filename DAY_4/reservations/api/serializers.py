from rest_framework import serializers
from reservations.models import Reservation
from decimal import Decimal
from datetime import datetime, timezone
from dateutil import parser
from cars.models import Car
from cars.api.serializers import CarSerializer


class ReservationSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    car_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    userId = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "car", "pickUpTime", "dropOffTime", 
                  "car_id", "user_id", "pickUpLocation", "dropOffLocation", 
                  "status", "totalPrice", "userId")
        
    def get_userId(self, obj):
        return obj.user.id
    
    def validate_pickUpTime(self, value):
        if value <=timezone.now():
            raise serializers.ValidationError('Pick up time must be grater than the current time')
        
        return value
    
    def validate_dropOffTime(self, value):
        pick_up_time = self.initial_data.get("pickUpTime")

        if value <= parser.parse(pick_up_time).replace(tzinfo=timezone.utc):
            raise serializers.ValidationError("dropOffTime must be greater than pickUpTime")
        
        return value
    
    def validate(self, attrs):
        pick_up_time = attrs['pickUpTime']
        drop_off_time = attrs['dropOffTime']
        car_id = attrs["car_id"]

        overlapping_reservations = Reservation.objects.filter(
            car_id = Car.object.get(id=car_id),
            pickUpTime__lt=drop_off_time,
            dropOffTime__gt=pick_up_time
        )

        if self.instance:
            overlapping_reservations = overlapping_reservations.exclude(pk=self.instance.pk)

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Reservations overlaps with existing reservations")
        
        return attrs
    
    def create(self, validated_data):
        try:
            car_id = validated_data["car_id"]
            car = Car.objects.get(id=car_id)
            pick_up_time = validated_data["pickUpTime"]
            drop_offtime = validated_data["dropOffTime"]
            price_per_hour = float(car.pricePerHour)
            total_hours = (drop_offtime - pick_up_time).total_seconds / 3600
            total_price = Decimal(total_hours) * Decimal(price_per_hour)
            validated_data["totalPrice"] = total_price
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"{e}")
        
    def update(self, instance, validated_data):
        car_id = validated_data["car_id"]
        car = Car.objects.get(id=car_id)
        pick_up_time = validated_data["pickUpTime"]
        drop_offtime = validated_data["dropOffTime"]
        price_per_hour = float(car.pricePerHour)
        total_hours = (drop_offtime - pick_up_time).total_seconds / 3600
        total_price = Decimal(total_hours) * Decimal(price_per_hour)
        validated_data["totalPrice"] = total_price

        return super().update(instance, validated_data)