from django.shortcuts import render

# from .models import YourModel

def index(request):
    return render(request, "category_app/index.html")

