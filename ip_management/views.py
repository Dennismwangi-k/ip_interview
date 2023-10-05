from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import IpAddress
from .serializers import IpAddressSerializer

class AllocateIPView(APIView):
    def post(self, request, format=None):
        customer_name = request.data.get('customer_name')
        email = request.data.get('email')

        if not customer_name or not email:
            return Response({'error': 'Customer name and email are required'}, status=status.HTTP_400_BAD_REQUEST)

        available_ip = IpAddress.objects.filter(status='available').first()
        
        if not available_ip:
            return Response({'error': 'No IPs are available'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
        available_ip.status = 'allocated'
        available_ip.customer_name = customer_name
        available_ip.customer_email = email
        available_ip.save()
        
        serializer = IpAddressSerializer(available_ip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReleaseIPView(APIView):
    def put(self, request, ip_address, format=None):
        ip = IpAddress.objects.filter(ip_address=ip_address).first()
        
        if not ip:
            return Response({'error': 'IP address not found'}, status=status.HTTP_404_NOT_FOUND)
        
        ip.status = 'available'
        ip.customer_name = None
        ip.customer_email = None
        ip.save()
        
        serializer = IpAddressSerializer(ip)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListAllocatedIPsView(APIView):
    def get(self, request, format=None):
        start_ip = request.query_params.get('start_ip')
        end_ip = request.query_params.get('end_ip')

        if start_ip and end_ip:
            ips = IpAddress.objects.filter(status='allocated', ip_address__range=(start_ip, end_ip))
        else:
            ips = IpAddress.objects.filter(status='allocated')
        
        serializer = IpAddressSerializer(ips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListAvailableIPsView(APIView):
    def get(self, request, format=None):
        start_ip = request.query_params.get('start_ip')
        end_ip = request.query_params.get('end_ip')

        if start_ip and end_ip:
            ips = IpAddress.objects.filter(status='available', ip_address__range=(start_ip, end_ip))
        else:
            ips = IpAddress.objects.filter(status='available')
        
        serializer = IpAddressSerializer(ips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)