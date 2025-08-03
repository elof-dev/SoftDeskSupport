from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'birth_date',
            'can_be_contacted', 'can_data_be_shared', 'first_name', 'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'birth_date': {'required': True}
        }

    def validate_birth_date(self, value):
        from datetime import date, timedelta
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user