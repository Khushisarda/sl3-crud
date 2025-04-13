from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Employee
from datetime import datetime


class EmployeeListView(ListView):
    model = Employee
    template_name = 'emp/employee_list.html'
    context_object_name = 'employees'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'emp/employee_detail.html'
    context_object_name = 'employee'
    pk_url_kwarg = 'employee_id'


class EmployeeCreateView(View):
    template_name = 'emp/employee_form.html'
    success_url = reverse_lazy('employee-list')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
      
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        birth_date_str = request.POST.get('birth_date')
        role = request.POST.get('role')

        errors = self.validate_employee_data(name, phone_number, birth_date_str, role)
        
        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'values': request.POST
            })

       
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            Employee.objects.create(
                name=name,
                phone_number=phone_number,
                birth_date=birth_date,
                role=role
            )
            messages.success(request, 'Employee created successfully!')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f'Error creating employee: {str(e)}')
            return render(request, self.template_name, {
                'errors': {'general': 'Failed to create employee'},
                'values': request.POST
            })

    def validate_employee_data(self, name, phone_number, birth_date_str, role):
        errors = {}
        
        if not name or len(name.strip()) < 2:
            errors['name'] = 'Name must be at least 2 characters'
            
        if not phone_number or len(phone_number.strip()) < 8:
            errors['phone_number'] = 'Enter a valid phone number'
            
        try:
            datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            errors['birth_date'] = 'Enter a valid date (YYYY-MM-DD)'
            
        if not role or len(role.strip()) < 2:
            errors['role'] = 'Role must be at least 2 characters'
            
        return errors

class EmployeeUpdateView(View):
    template_name = 'emp/employee_form.html'
    success_url = reverse_lazy('employee-list')

    def get(self, request, employee_id, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=employee_id)
        return render(request, self.template_name, {
            'values': {
                'name': employee.name,
                'phone_number': employee.phone_number,
                'birth_date': employee.birth_date.strftime('%Y-%m-%d'),
                'role': employee.role,
            },
            'is_update': True,
            'employee_id': employee_id
        })

    def post(self, request, employee_id, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=employee_id)
        

        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        birth_date_str = request.POST.get('birth_date')
        role = request.POST.get('role')

        errors = EmployeeCreateView.validate_employee_data(self, name, phone_number, birth_date_str, role)
        
        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'values': request.POST,
                'is_update': True,
                'employee_id': employee_id
            })

        
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            employee.name = name
            employee.phone_number = phone_number
            employee.birth_date = birth_date
            employee.role = role
            employee.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
            return render(request, self.template_name, {
                'errors': {'general': 'Failed to update employee'},
                'values': request.POST,
                'is_update': True,
                'employee_id': employee_id
            })


class EmployeeDeleteView(View):
    template_name = 'emp/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

    def get(self, request, employee_id, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=employee_id)
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, employee_id, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=employee_id)
        try:
            employee.delete()
            messages.success(request, 'Employee deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
        return redirect(self.success_url)