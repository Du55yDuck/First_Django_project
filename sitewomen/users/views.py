from django.http import HttpResponse
from django.shortcuts import render


def login_user(request):  # ф-я для авторизации
    return HttpResponse("login")


def logout_user(request):  # ф-я для выхода из авторизации
    return HttpResponse("logout")
