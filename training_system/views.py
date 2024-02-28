from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.
def home(request: Request) -> Response:
    return render(request, 'index.html')