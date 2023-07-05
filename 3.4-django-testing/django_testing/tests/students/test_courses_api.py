
import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from students.models import Student, Course

from model_bakery import baker


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
    course = course_factory()

    #Act
    response = client.get('/api/v1/courses/')

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course.name


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
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_check_id(client, user, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/?id={courses[2].id}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[2].id


@pytest.mark.django_db
def test_check_name(client, user, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/?name={courses[5].name}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_post_course(client, user):
    # Arrange
    count = Course.objects.count()

    # Act
    response = client.post(
        '/api/v1/courses/',
        data={
            'name': 'C',
            'student_id': user.id
        })

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(client, user, course_factory):
    # Arrange
    course = course_factory()

    # Act
    json_data = {
        "name": "C"
    }
    response = client.patch(f"/api/v1/courses/{course.id}/", data=json_data)

    # Assert
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == "C"


@pytest.mark.django_db
def test_delete_course(client, user, course_factory):
    # Arrange
    course = course_factory()

    # Act
    response = client.delete(f"/api/v1/courses/{course.id}/")

    # Assert
    assert response.status_code == 204  # Проверка успешного кода состояния

    # Убедитесь, что курс был удален из базы данных
    with pytest.raises(Course.DoesNotExist):
        course.refresh_from_db()


