from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Employee


class DashboardTests(TestCase):
    def test_dashboard_renders_database_driven_statistics_and_charts(self):
        today = timezone.localdate()
        recent_employee = Employee.objects.create(
            name='Casey Rivera',
            email='casey@example.com',
            phone='555-0110',
            department='Engineering',
            designation='Engineer',
            salary='75000.00',
            joining_date=today,
        )
        Employee.objects.create(
            name='Morgan Patel',
            email='morgan@example.com',
            phone='555-0111',
            department='Design',
            designation='Designer',
            salary='45000.00',
            joining_date=today - timedelta(days=60),
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_employees'], 2)
        self.assertEqual(response.context['total_departments'], 2)
        self.assertEqual(response.context['average_salary'], 60000)
        self.assertEqual(response.context['new_employees'], 1)
        self.assertEqual(response.context['recent_employees'][0], recent_employee)
        self.assertEqual(response.context['department_chart']['values'], [1, 1])
        self.assertIn(today.strftime('%b %Y'), response.context['joining_chart']['labels'])
        self.assertIn(1, response.context['joining_chart']['values'])
        self.assertEqual(sum(response.context['salary_chart']['values']), 2)
        self.assertContains(response, 'department-chart-data')


class EmployeeListFilterTests(TestCase):
    def setUp(self):
        self.matching_employee = Employee.objects.create(
            name='Avery Smith',
            email='avery@example.com',
            phone='555-0101',
            department='Engineering',
            designation='Backend Developer',
            salary='75000.00',
            joining_date='2024-01-15',
        )
        Employee.objects.create(
            name='Jordan Lee',
            email='jordan@example.com',
            phone='555-0102',
            department='Marketing',
            designation='Developer Relations',
            salary='68000.00',
            joining_date='2023-06-01',
        )

    def test_search_and_department_filter_can_be_combined(self):
        response = self.client.get(reverse('employee_list'), {
            'q': 'BACK',
            'department': 'Engineering',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['employees']), [self.matching_employee])
        self.assertEqual(response.context['search_query'], 'BACK')
        self.assertEqual(response.context['selected_department'], 'Engineering')

    def test_department_filter_without_matching_employees_shows_message(self):
        response = self.client.get(reverse('employee_list'), {
            'q': 'missing',
            'department': 'Engineering',
        })

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['employees'], [])
        self.assertContains(response, 'No employees match your search and department filter.')


class EmployeeCrudTests(TestCase):
    def test_create_update_and_delete_employee(self):
        employee_data = {
            'name': 'Taylor Morgan',
            'email': 'taylor@example.com',
            'phone': '555-0103',
            'department': 'Operations',
            'designation': 'Coordinator',
            'salary': '52000.00',
            'joining_date': '2025-02-10',
        }

        response = self.client.post(reverse('add_employee'), employee_data)
        self.assertRedirects(response, reverse('employee_list'))

        employee = Employee.objects.get(email='taylor@example.com')
        employee_data['name'] = 'Taylor Updated'
        response = self.client.post(
            reverse('edit_employee', args=[employee.id]),
            employee_data,
        )
        self.assertRedirects(response, reverse('employee_list'))
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'Taylor Updated')

        response = self.client.post(reverse('delete_employee', args=[employee.id]))
        self.assertRedirects(response, reverse('employee_list'))
        self.assertFalse(Employee.objects.filter(id=employee.id).exists())
