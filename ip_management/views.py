from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import IpAddress
from .serializers import IpAddressSerializer
from ipaddress import IPv4Network
from django.http import JsonResponse

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
        
        if ip.status == 'available':
            return Response({'error': 'IP address is already available'}, status=status.HTTP_400_BAD_REQUEST)
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

class SubnetCalculatorView(APIView):
    def post(self, request, format=None):
        try:
            ip = request.data.get('ip')
            subnet_mask = request.data.get('subnet_mask')
            ip_network = IPv4Network(f"{ip}/{subnet_mask}", strict=False)
            network_address = str(ip_network.network_address)
            broadcast_address = str(ip_network.broadcast_address)
            usable_ip_range = [str(ip) for ip in ip_network.hosts()]
            result = {
                "network_address": network_address,
                "broadcast_address": broadcast_address,
                "usable_ip_range": usable_ip_range,
            }
            return JsonResponse(result, status=status.HTTP_200_OK)
        except ValueError:
            return JsonResponse({'error': 'Invalid IP address or subnet mask'}, status=status.HTTP_400_BAD_REQUEST)