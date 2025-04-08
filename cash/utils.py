from users.models import User
from django.shortcuts import get_object_or_404

def check_user(user):
    return user.is_authenticated and user.is_staff

def user_student(user):
    return user.course_purchased