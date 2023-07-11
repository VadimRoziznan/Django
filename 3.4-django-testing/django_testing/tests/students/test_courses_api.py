
import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from students.models import Student, Course

from model_bakery import baker

from students.serializers import StudentSerializer, CourseSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, user, course_factory):
    #Arrange
    courses = course_factory(_quantity=1)

    #Act
    response = client.get(f'/api/v1/courses/?id={courses[0].pk}')


    #Assert
    assert response.status_code == 200
    data = response.json()
    print(response)
    assert data[0]['id'] == courses[0].pk
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_get_courses(client, user, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)

    #Act
    response = client.get('/api/v1/courses/')

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m, in enumerate(data):
        assert m['id'] == courses[i].id
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_check_id(client, user, course_factory):
    # Arrange
    courses = course_factory(_quantity=12)

    # Act
    response = client.get(f'/api/v1/courses/?id={courses[0].pk}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == courses[0].pk


@pytest.mark.django_db
def test_check_name(client, user, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/?name={courses[5].name}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_post_course(client, user):

    student_data = {
        'name': 'John',
        'birth_date': '1990-01-01'
    }
    student_serializer = StudentSerializer(data=student_data)
    assert student_serializer.is_valid(), student_serializer.errors
    student = student_serializer.save()

    course_data = {
        'name': 'Test Course',
        'students': [
            {
                'name': 'Jane',
                'birth_date': '1990-01-01'
            }
        ]
    }
    course_serializer = CourseSerializer(data=course_data)
    assert course_serializer.is_valid(), course_serializer.errors
    course = course_serializer.save()

    assert course.name == 'Test Course'
    assert course.students.count() == 1
    assert course.students.first().name == 'Jane'

    course.delete()

    student.delete()


@pytest.mark.django_db
def test_patch_course(client, user, course_factory):
    # Arrange
    course = course_factory()

    # Act
    course_data = {
        "name": "C"
    }
    response = client.patch(f"/api/v1/courses/{course.pk}/", data=course_data)

    # Assert
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "C"


@pytest.mark.django_db
def test_delete_course(client, user, course_factory):
    # Arrange
    course = course_factory()

    # Act
    response = client.delete(f"/api/v1/courses/{course.pk}/")

    # Assert
    assert response.status_code == 204

    # Убедитесь, что курс был удален из базы данных
    with pytest.raises(Course.DoesNotExist):
        course.refresh_from_db()
