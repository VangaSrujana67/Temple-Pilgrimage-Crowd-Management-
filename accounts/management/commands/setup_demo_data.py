from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Classroom, Semester, Section
from scheduler.models import TimeSlot
from faculty.models import Faculty
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with realistic academic demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing demo data generation...")

        # 1. Create Departments
        depts_data = [
            {'name': 'Computer Science & Engineering', 'code': 'CSE'},
            {'name': 'Electronics & Communication', 'code': 'ECE'},
            {'name': 'Mechanical Engineering', 'code': 'MECH'},
        ]
        depts = []
        for d in depts_data:
            dept, _ = Department.objects.get_or_create(name=d['name'], code=d['code'])
            depts.append(dept)

        # 2. Create Classrooms
        rooms_data = [
            {'name': 'LH-101', 'cap': 60, 'type': 'classroom'},
            {'name': 'LH-102', 'cap': 60, 'type': 'classroom'},
            {'name': 'CS-LAB-1', 'cap': 30, 'type': 'lab'},
        ]
        for r in rooms_data:
            Classroom.objects.get_or_create(name=r['name'], capacity=r['cap'], room_type=r['type'])

        # 3. Create Time Slots (Standard Morning Session)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        times = [
            (datetime.time(9, 0), datetime.time(10, 0), False),
            (datetime.time(10, 0), datetime.time(11, 0), False),
            (datetime.time(11, 0), datetime.time(11, 30), True, 'Short Break'),
            (datetime.time(11, 30), datetime.time(12, 30), False),
        ]
        
        for day in days:
            for t in times:
                TimeSlot.objects.get_or_create(
                    day=day, 
                    start_time=t[0], 
                    end_time=t[1],
                    is_break=t[2],
                    break_name=t[3] if len(t) > 3 else None
                )

        # 4. Create a Demo Faculty
        # Note: Ensure a user with this email doesn't already exist or change it
        user, created = User.objects.get_or_create(
            email="faculty_demo@college.edu",
            defaults={'role': 'faculty', 'is_active': True, 'is_verified': True}
        )
        if created:
            user.set_password('demo1234')
            user.save()
        
        Faculty.objects.get_or_create(
            user=user,
            department=depts[0],
            designation="Assistant Professor",
            employee_id="EMP001"
        )

        # 5. Create Semester & Section
        sem, _ = Semester.objects.get_or_create(number=4, academic_year="2025-26")
        Section.objects.get_or_create(name="A", semester=sem, department=depts[0], student_count=55)

        self.stdout.write(self.style.SUCCESS('Successfully populated academic infrastructure!'))