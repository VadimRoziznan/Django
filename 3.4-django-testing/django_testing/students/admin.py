from django.contrib import admin
from students.models import Course, Student


@admin.register(Course)
class CourseAdmuin(admin.ModelAdmin):

    list_display = ['name',]


@admin.register(Student)
class StudentAdmuin(admin.ModelAdmin):

    list_display = ['name', 'birth_date']
