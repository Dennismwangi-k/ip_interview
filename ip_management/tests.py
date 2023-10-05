from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from ip_management.models import IpAddress

class AllocateIPViewTestCase(APITestCase):
    def setUp(self):
        self.available_ip = IpAddress.objects.create(ip_address='192.168.1.1', status='available')
        self.allocated_ip = IpAddress.objects.create(ip_address='192.168.1.2', status='allocated', customer_name='Test', customer_email='test@example.com')

    def test_allocate_ip_success(self):
        response = self.client.post('/ip/allocate/', {'customer_name': 'John Doe', 'email': 'john.doe@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   
    def test_release_ip_success(self):
        allocated_ip = IpAddress.objects.filter(ip_address='192.168.1.2').first()
        if allocated_ip:
            allocated_ip.delete()
        response = self.client.put('/ip/release/192.168.1.2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
