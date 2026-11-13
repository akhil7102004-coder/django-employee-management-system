from datetime import timedelta

from django.db.models import Avg, Case, CharField, Count, Q, Value, When
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EmployeeForm
from .models import Employee


def home(request):
    today = timezone.localdate()
    month_starts = []
    month_start = today.replace(day=1)
    for _ in range(6):
        month_starts.append(month_start)
        month_start = (month_start - timedelta(days=1)).replace(day=1)
    month_starts.reverse()
    next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1)

    total_employees = Employee.objects.count()
    total_departments = Employee.objects.values('department').distinct().count()
    average_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    new_employees = Employee.objects.filter(
        joining_date__gte=today - timedelta(days=30),
        joining_date__lte=today,
    ).count()

    department_data = list(
        Employee.objects.values('department')
        .annotate(total=Count('id'))
        .order_by('department')
    )

    monthly_totals = {
        row['month'].date() if hasattr(row['month'], 'date') else row['month']: row['total']
        for row in Employee.objects.filter(
            joining_date__gte=month_starts[0],
            joining_date__lt=next_month,
        )
        .annotate(month=TruncMonth('joining_date'))
        .values('month')
        .annotate(total=Count('id'))
    }

    salary_band_labels = ['< ₹25k', '₹25k–₹50k', '₹50k–₹75k', '₹75k–₹100k', '₹100k+']
    salary_band_totals = {
        row['salary_band']: row['total']
        for row in Employee.objects.annotate(
            salary_band=Case(
                When(salary__lt=25000, then=Value(salary_band_labels[0])),
                When(salary__lt=50000, then=Value(salary_band_labels[1])),
                When(salary__lt=75000, then=Value(salary_band_labels[2])),
                When(salary__lt=100000, then=Value(salary_band_labels[3])),
                default=Value(salary_band_labels[4]),
                output_field=CharField(),
            )
        )
        .values('salary_band')
        .annotate(total=Count('id'))
    }

    return render(request, 'employees/home.html', {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'average_salary': average_salary,
        'new_employees': new_employees,
        'recent_employees': Employee.objects.order_by('-joining_date', '-id')[:6],
        'department_chart': {
            'labels': [row['department'] or 'Unassigned' for row in department_data],
            'values': [row['total'] for row in department_data],
        },
        'joining_chart': {
            'labels': [month.strftime('%b %Y') for month in month_starts],
            'values': [monthly_totals.get(month, 0) for month in month_starts],
        },
        'salary_chart': {
            'labels': salary_band_labels,
            'values': [salary_band_totals.get(label, 0) for label in salary_band_labels],
        },
    })


def employee_list(request):
    search_query = request.GET.get('q', '').strip()
    selected_department = request.GET.get('department', '')

    employees = Employee.objects.all()
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(designation__icontains=search_query)
            | Q(department__icontains=search_query)
        )
    if selected_department:
        employees = employees.filter(department=selected_department)

    departments = (
        Employee.objects.order_by('department')
        .values_list('department', flat=True)
        .distinct()
    )
    return render(request, 'employees/employee_list.html', {
        'employees': employees.order_by('id'),
        'search_query': search_query,
        'selected_department': selected_department,
        'departments': departments,
    })


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee'
    })


def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee'
    })


# Delete Employee
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {
        'employee': employee
    })