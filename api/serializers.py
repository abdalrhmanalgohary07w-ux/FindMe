from rest_framework import serializers
from .models import MissingPerson

class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = [
            'id', 
            'full_name', 
            'age', 
            'gender', 
            'last_seen_date', 
            'last_seen_location', 
            'contact_phone', 
            'status', 
            'description', 
            'clothing_description',
            'image', 
            'created_at'
        ]
