"""
URL configuration for course_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from crud_api import views

urlpatterns = [
    path('api/orders', views.OrdersViewsList.as_view(), name='OrdersList'),
    path('api/orders/<int:pk>', views.OrdersViewsDetails.as_view(), name='OrdersDetails'),
    path('api/assignments', views.AssignmentsViewsList.as_view(), name='AssignmentsList'),
    path('api/assignments/<int:pk>', views.AssignmentsViewsDetails.as_view(), name='AssignmentsDetails'),
    path('api/cars', views.CarsViewsList.as_view(), name='CarsList'),
    path('api/cars/<int:pk>', views.CarsViewsDetails.as_view(), name='CarsDetails'),
    path('api/drivers', views.DriversViewsList.as_view(), name='DriversList'),
    path('api/drivers/<int:pk>', views.DriversViewsDetails.as_view(), name='DriversDetails'),
    path('api/orders_drivers', views.OrdersDriversViewsList.as_view(), name='OrdersDriversList'),
    path('api/orders_drivers/<int:pk>', views.OrdersDriversViewsDetails.as_view(), name='OrdersDriversDetails'),
    path('api/clients', views.ClientsViewsList.as_view(), name='ClientsList'),
    path('api/clients/<int:pk>', views.ClientsViewsDetails.as_view(), name='ClientsDetails'),
    path('api/positions', views.PositionsViewsList.as_view(), name='PositionsList'),
    path('api/positions/<int:pk>', views.PositionsViewsDetails.as_view(), name='PositionsDetails'),
    path('api/staff', views.StaffViewsList.as_view(), name='StaffList'),
    path('api/staff/<int:pk>', views.StaffViewsDetails.as_view(), name='StaffDetails'),
    path('api/tech_inspection', views.TechInsViewsList.as_view(), name='TechInspectionsList'),
    path('api/tech_inspection/<int:pk>', views.TechInsViewsDetails.as_view(), name='TechInspectionsDetails'),
]
