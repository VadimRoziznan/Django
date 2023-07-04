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
    # course = course_factory(_quantity=5)

    #Act
    response = client.get("/api/v1/courses/")

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert
    # assert len(data) == len(course)
    # for i, m in enumerate(data):
    #     assert m["name"] == course[i].name


# @pytest.mark.django_db
# def test_create_course(client):
#     count = Course.objects.count()
#     response = client.post("/courses/",
#                            data={"name": })


