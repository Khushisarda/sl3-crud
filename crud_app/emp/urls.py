from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee-list'),
    path('crud_app/<int:employee_id>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('crud_app/new/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('crud_app/<int:employee_id>/edit/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('crud_app/<int:employee_id>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
]