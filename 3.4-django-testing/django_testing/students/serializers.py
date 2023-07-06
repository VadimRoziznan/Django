
from rest_framework import serializers


from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'students')

    def create(self, validated_data):
        students_data = validated_data.pop('students')

        for student_data in students_data:
            student_exists = Student.objects.filter(name=student_data['name']).exists()
            if not student_exists:
                student = Student.objects.create(**student_data)

        course = Course.objects.create(**validated_data)
        course.students.set(students_data)
        return course

