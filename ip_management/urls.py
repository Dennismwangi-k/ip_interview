
from .views import AllocateIPView, ReleaseIPView, ListAllocatedIPsView, ListAvailableIPsView, SubnetCalculatorView
from django.urls import path

urlpatterns = [
    path('ip/allocate/', AllocateIPView.as_view(), name='allocate_ip'),
    path('ip/release/<str:ip_address>/', ReleaseIPView.as_view(), name='release_ip'),
    path('ip/allocated/', ListAllocatedIPsView.as_view(), name='list_allocated_ips'),
    path('ip/available/', ListAvailableIPsView.as_view(), name='list_available_ips'),
    path('ip/subnet/', SubnetCalculatorView.as_view(), name='subnet_calculator'),
]