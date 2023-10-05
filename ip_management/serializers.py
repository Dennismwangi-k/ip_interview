from rest_framework import serializers
from .models import IpAddress

class IpAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = ['ip_address', 'status', 'customer_name', 'customer_email']
