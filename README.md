# django-base-template

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000


1. mkdir django_project_root/your_app_name
2. python manage.py startapp your_app_name django_project_root/your_app_name

3. Modify configuration_root/urls.py => INSTALLED_APPS  = [
    path('your_app_name/', include('django_project_root.your_app_name.urls')),
]

4. Modify your_app_name/apps.py => 
name = 'django_project_root.your_app_name'

4. vi django_project_root/your_app_name/urls.py => 

from django.urls import path
from . import views

app_name = 'your_app_name'

urlpatterns = [
    path('', views.index, name='index'),
]

5. Create Template Structure => 

mkdir -p django_project_root/templates/your_app_name

6. Create Base Template =>

{% extends 'core/base.html' %}

{% block title %}Your App{% endblock %}

{% block content %}
    <!-- Your content here -->
{% endblock %}

7. Define Models =>

from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

8. Create and Apply Migrations =>

python manage.py makemigrations
python manage.py migrate

9. Register Models in Admin =>


from django.contrib import admin
from .models import YourModel

admin.site.register(YourModel)

10. Create Views =>

from django.shortcuts import render
from .models import YourModel

def index(request):
    return render(request, 'your_app_name/index.html')

