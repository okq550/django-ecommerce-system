Django Cheat Sheet

### Start a New Django Project

```
# Create et access project folder
mkdir project_name
cd project_name

# Create Python virtual env
python3 -m venv venv

# Activate virtual env
source venv/bin/activate

# If you want to deactivate virtual env
deactivate

# Install django (~= same as 4.2.*)
pip install django~=4.2.0

# New django project (from project_name folder)
django-admin startproject config

# Create app (from project_name folder)
python manage.py startapp app_name
```

#### Migration:

Django create a database table for each models present in your app using thoses commands:

*   Makemigrations: Create a file under app\_name/migrations with the database structure to create

```
python manage.py makemigrations
```

*   Migrate: Will read the migrations files and create the actual database and tables

```
python manage.py migrate
```

#### Create superuser for authenficiation/admin panel

```
python manage.py createsuperuser
```

#### Start server

```
python manage.py runserver  => ex.  http://127.0.0.1:8000
```

#### Requirements

```
# Create a requirements file that contain all your projet dependencies
pip freeze > requirements.txt

# Install your project requirements (if a requirements file exist)
pip install -r requirements.txt
```

#### Other commands

```
# Django shell (Run projet code direclty)
python manage.py shell

# example of code to run in the shell:
 >>> from app_name.models import User
 >>> user1 = User.objects.first()

# Prepare static folders for production
python manage.py collectstatic

# Take all data from app blog and export in json
python manage.py dumpdata blog > myapp.json

# Take all data in json file and import in app data table
python manage.py loaddata myapp.json

# To Create or Update a message file for Translation, run this command
django-admin makemessages -l de
# Updating message files
django-admin compilemessages
```

## Project config

### Configuration settings

##### Project base templates directory and Apps templates directory:

*   create folder project/templates
*   create folder appfolder/templates/appname

##### Create Static folder in base root and separate for apps:

*   project\_name\\static\\root
*   app\_name\\static\\app\_name

```
# Add app to settings.py
INSTALLED_APPS = [
         … ,
         'app_name.apps.App_nameConfig',
 ]

# template directory config
Project templates settings.py:
    TEMPLATES = [
        { …
           'DIRS': [BASE_DIR / 'templates'],
        … }

# Static folder:
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = 'static_root'
# Media folder:
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    (BASE_DIR / 'static'),
)
MEDIA_ROOT = BASE_DIR / 'media'

# To use PostgresSQL
# pip install psycopg2
# settings.py
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432'
        }
    }

TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
]

DATE_FORMAT = "Y/M/d"

# locale for Translations
LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
]

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

# CK Editor Configuration
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMGE_FILES = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    }}

# SSL
# If you have an SSL certificate
SECURE_SSL_REDIRECT = True
# cookies will only be sent via HTTPS connections
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Customize Admin Panel Header & Title
from django.contrib.admin import AdminSite

AdminSite.site_header = _('Administrator Control Panel')
AdminSite.site_title = _('Administrator Control Panel')
AdminSite.index_title = _('Wellcome to Control Panel')
```

## Create Data Model:

Theses models can be created as database tables with the migrations commands

```
# models.py
# The id fields is automaticly created by Django
# for each model that why it's not show below
from django.db import models

class Customer(models.Model)
    name = models.Charfield('Customer', max_length=120)
    age = models.IntegerField()
    note = models.TextField(blank=True, null = True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    credit = models.FloatField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to ='uploads/')
    # Select Field (return value, display value)
    TYPE_CHOICES = (
        ('Customer', 'Customer'),
        ('Supplier', 'Supplier'),
        ('Student', 'Student'),
    )
    type = models.CharField(choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):   # Model string representation
        return self.name

    # the URL that points to a resource or page on your website
    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})
```

#### Relationship between models

```
# One-to-Many: (use double quotes if the entity is not yet declare) ex. "Supplier"
supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE,related_name="supplierother")

# on_delete can be set to models.CASCADE, models.ST_DEFAULT or models.SET_NULL
# The related_name attribute specifies the name of the reverse relation from the supplier model back to your model

# Many-to-Many:
tags = models.ManyToManyField(Tag, blank=True)

# One to One
User = models.OneToOneField(User, on_delete=models.CASCADE)

# Overwrite save method
def save(self, (*args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
```

## Field Lookups

In Django, the `field__lookuptype` syntax is used to perform lookups on fields in queries. The `field` represents the name of the field you want to perform the lookup on, and `lookuptype` represents the type of lookup you want to perform.

For example, let's say you have a model called `Book` with a field called `title` . You can use the `field__lookuptype` syntax to perform different types of lookups on the `title` field.

Here are a few examples:

```
# 1. Exact Match Lookup:
Book.objects.filter(title__exact='Python Tricks')
# 2. Case-insensitive Lookup:
Book.objects.filter(title__iexact='python tricks')
# 3. Contains Lookup:
Book.objects.filter(title__contains='Python')
# 4. Startswith Lookup:
Book.objects.filter(title__startswith='Python')
# 5. Endswith Lookup:
Book.objects.filter(title__endswith='Tricks')
```

### Field Lookups Reference

A list of all field look up keywords:

| **Keyword** | **Description** |
| --- | --- |
| contains | Contains the phrase |
| icontains | Same as contains, but case-insensitive |
| date | Matches a date |
| day | Matches a date (day of month, 1-31) (for dates) |
| endswith | Ends with |
| iendswith | Same as endswidth, but case-insensitive |
| exact | An exact match |
| iexact | Same as exact, but case-insensitive |
| in | Matches one of the values |
| isnull | Matches NULL values |
| gt | Greater than |
| gte | Greater than, or equal to |
| hour | Matches an hour (for datetimes) |
| lt | Less than |
| lte | Less than, or equal to |
| minute | Matches a minute (for datetimes) |
| month | Matches a month (for dates) |
| quarter | Matches a quarter of the year (1-4) (for dates) |
| range | Match between |
| regex | Matches a regular expression |
| iregex | Same as regex, but case-insensitive |
| second | Matches a second (for datetimes) |
| startswith | Starts with |
| istartswith | Same as startswith, but case-insensitive |
| time | Matches a time (for datetimes) |
| week | Matches a week number (1-53) (for dates) |
| week\_day | Matches a day of week (1-7) 1 is Sunday |
| iso\_week\_day | Matches a ISO 8601 day of week (1-7) 1 is Monday |
| year | Matches a year (for dates) |
| iso\_year | Matches an ISO 8601 year (for dates) |

## Admin Panel:

Every Django projects come with an Admin Panel that can be open at /admin url (ex: localhost:8000/admin)

To display the model in the Admin panel register the model in the app\_name/admin.py file

For each models you can specify the fields you want to use

```
from django.contrib import admin
from app_name.models import Blog

# Custom model Admin (admin.py):
@admin.register(Blog)   # Register app
class BlogAdmin(admin.ModelAdmin)
    fields = ("title", "description") # Fields to use for add/edit/show page
    list_display = ("title", "description") # fields to display in search page
    list_display_links = ("title",) # fields that will be a link in search page
    ordering = ("date_created",) # Ordering allowed in the search page
    search_fields = ("title", "description") # Search fields allowed in the search page
    list_filter =("title",) # define list filters that appear in the right sidebar
```

## Routing:

Django routing info is store in project\_folder/urls.py file

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # pre-created admin urls routes
    path('', include('app_name.urls')) # include your app urls
]
```

the 'include()' method allow to link another urls.py file created in your app folder (app\_name/urls.py)

```
from django.urls import path
from app_name import views

urlpatterns = [
    path('posts', views.index, name='posts.index'),
    path('posts/create/', views.create, name='posts.create',
    path('posts/<int:id>/', views.show, name='posts.show'),
    path('posts/<int:id>/edit/', views.edit, name='posts.edit'),
    path('posts/<int:id>/delete/', views.delete, name='posts.delete'),
    path('posts/<int:id>/<int:state>/', views.status, name='posts.status'), # two arguments
]
```

## Static Route and Customize Admin Panel

Header and Title admin panel & Custom 404,500,503 Template

```
# add in project/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  ...  ]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Costomize 404 Template page
handler404 = 'app_name.views.handler404'
handler500 = 'app_name.views.handler500'
handler503 = 'app_name.views.handler503'
```

## Function Based Views

```
# views.py
from django.shortcuts import render, redirect
from app_name.models import Post
from app_name.forms import PostForm

def index(request):
    # Get all Posts
    posts = Post.objects.all()

    # Render app template with context
    return render(request, 'appfolder/index.html', {'posts': posts})

def show(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'appfolder/show.html', {'post': post})

def create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        # optionally we can access form data with form.cleaned_data['first_name']
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('/posts')

    return render(request, 'appfolder/create.html', {'form': form)

def edit(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('/posts')

    return render(request, 'appfolder/edit.html', {'form': form)

def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/posts')

def status(request, id, state):
    post = Post.objects.get(id=id, state=state)
    return redirect('appfolder/status.html', {'post': post})
```

## Class Based Views

```
from django.views.generic import TemplateView, ListView, DetailView,
           CreateView, UpdateView, DeleteView

class LandingPageView(TemplateView):
    template_name = 'landing.html'

    # Optional: Change context data dict
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Landing Page'
        return context

class PostsListView(ListView):
    queryset = Post.objects.all()
    # Optional
    # context_object_name = "posts" (default: post_list)
    # template_name = 'posts.html' (default: posts/post_list.html)

class PostsDetailView(DetailView):
    model = Post # object var in template
    # Optional
    # template_name = 'post.html' (default: posts/post_detail.html)

class PostsCreateView(CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html' # no default value

    def get_success_url(self):
        return reverse('posts-list')

    # Optional: Overwrite form data (before save)
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            from.instance.author = self.request.user
        return super().form_valid(form)

class PostsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'

    def get_success_url(self):
        return reverse('post-list')

    # Optional: Change context data dict
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_text'] = 'Update'
        return context

class PostsDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts-list')

# Urls.py route declaration
path('<int:pk>/update/', PostsUpdateView.as_view(), name='post-update')
```

## Django Template

Templates are store in project\_folder/templates or in your app\_folder/templates/app\_name/\*.html

```
# Extend from another template
# can use the same parts of your HTML for different template
{% extends 'base.html' %}

# A part of the parent template that is defined and is replaced by a part in the child template
{% block contents %}
{% endblock contents %}

# include template
{% include 'partials/header.html' %}
# include template with One or More Parameters
{% include 'body.html' with key1=value1 key2=value2 %}

# If statement in template
{% if user.username = 'Mike' %}
    <p>Hello Admin</p>
{% elif user.username = 'john' %}
    <p>Hello John Doe</p>
{% else %}
    <p>Hello User</p>
{% endif %}

# for loop in template
{% for product in products %}
  <p> row:
      {{ forloop.counter }} # starting index 1
      {{ forloop.counter0 }} # starting index 0
  </p>
  <p>The product name is {{ product.name }}<p>
  <p>The product name is {{ product.price }}<p>
{% endfor %}

# Access to the variable in the template
{{ var_name }}

# Template variables formating
{{ title | lower }}
{{ blog.post | truncatwords:50 }}
{{ order.date | date:"D M Y" }}
{{ list_items | slice:":3" }}
{{ total | default:"nil" }}

# Current path (ex. posts/1/show)
{{ request.path }}

# URL by name with param
{% url 'posts.delete' id=post.id %}

# Use static in template:
{% load static %}
{% static 'css/main.css' %}

# Define the variable in the template
{% with name="World" %}
<html>
<div>Hello {{ name }}!</div>
</html>
{% endwith %}

# Template translate text
{% load i18n %}
<title>{% trans "This is the title." %}</title>
# Use variable translate in the template
<title>{% trans object.title %}</title>

# Define the list in the template
<input type="number"
{% if product.unit in 'kg,milligram,milliliter' %}
    step="0.01"
{% else %}
    step="1"
{% endif %}>

# Safely Pass Data to JavaScript in a Django Template:
#+ Use data attributes for simple values
<script data-username="{{ username }}">
    const data = document.currentScript.dataset;
    const username = data.username;
</script>

#+ Separate script files: can use document.currentScript for separate script files
<script src="{% static 'index.js' %}" data-username="{{ username }}"></script>

#+ Case conversion
<script src="{% static 'index.js' %}" data-full-name="{{ full_name }}"></script>
# Read it in JavaScript as fullName:
const data = document.currentScript.dataset;
const fullName = data.fullName;

#+ Non-string types
<script src="{% static 'index.js' %}" data-follower-count="{{ follower_count }}"></script>
# parseInt() to convert this value from a string:
const data = document.currentScript.dataset;
const followerCount = parseInt(data.followerCount, 10);

#+ There’s no limit: A <script> can have as many data attributes as you like:
<script src="{% static 'index.js' %}"
        defer
        data-settings-url="{% url 'settings' %}"
        data-configuration-url="{% url 'configuration' %}"
        data-options-url="{% url 'options' %}"
        data-preferences-url="{% url 'preferences' %}"
        data-setup-url="{% url 'setup' %}"
        >
</script>
```

## Create custom template tags and filters

For example, if your custom tags/filters are in a file called `basetags.py`, your app layout might look like this:

```
app_name/
└─── templatetags/
     └─── basetags.py
     __init__.py
     models.py
     views.py
```

*   And in your template you would use the following:

```
{% load basetags %}
```

*   the module must contain a module-level variable named register that is a template.Library instance, in which all the tags and filters are registered. So, near the top of your module, put the following:

#### Writing custom template filters

Custom filters are Python functions that take one or two arguments:

The value of the variable (input) – not necessarily a string.

The value of the argument – this can have a default value, or be left out altogether.

For example, in the filter `{{ var|foo:"bar" }}`, the filter foo would be passed the variable var and the argument "bar".

The Library.filter() method takes two arguments:

The name of the filter – a string.

The compilation function – a Python function (not the name of the function as a string).

You can use register.filter() as a decorator instead:

```
# basetags.py
from django import template

register = template.Library()

@register.filter(name="cut")
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")

# Most filters don’t take arguments. In this case, leave the argument out of your function
@register.filter()
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

@register.simple_tag
def to_class_name(object):
    return str(object.__class__.__name__)

# Template
# And here’s an example of how that filter would be used in Template:
{{ somevariable | cut:"0" }}

# Put the result of simple tag into a variable
{% to_class_name object as objectmodel %}
<p>Model Class Name: {{ objectmodel }}</p>
```

## Creating custom Context Processor

1.  Anywhere, create a context\_processors.py file

```
project_name
└───app_name
    ├───...
    └───context_processors.pyy
```

2.  Create a function in context\_processors.py that accepts a HttpRequest object as an argument and returns a dictionary

A context processor is just a function that accepts an HttpRequest object as an argument and returns a dictionary. Like this:

```
# app_name/context_processors.py
def site_email(request):
    return { 'site_email' : 'example@gmail.com' }
```

1.  Add this to your context\_processors setting in settings.py (at the bottom for security reasons)

```
TEMPLATES = [
    { …
        'OPTIONS': {
          'context_processors': [
            …
              'app_name.context_processors.site_email', # <- New context processor here
            …
          ],
    … },

# Now be able to access the 'site_email' template variable on every single django template across your whole site.
```

## Model Managers and Querysets

Model manager allow model database reads and writes

```
# One line create and save
Article.objects.create(name='Item 1', price=19.95)

# Read all
Article.objects.all()

# Create
user = User.objects.first()
article = Article(user=user, name='Item 1', price=19.95)

# Save
article.save()

# Read one
Article.objects.get(id=1)

# Select Related (to avoid n+1 query)
posts = Post.objects.select_related('user', 'category').all()

# Read or render a 404 not found page
from django.shortcuts import get_object_or_404
article = get_object_or_404(Article, id=512)

# Filter
Article.objects.filter(model='dyson', name__icontains='dyson') # __icontains
Article.objects.filter(year__gt=2016) # __gt = greater than
Article.objects.filter(year__lt=2001) # __lt = less than

# Filter on relationship sub model field
Article.objects.get(user__username='mike')

# Ordering
Article.objects.order_by('name')     # ascending
Article.objects.order_by('-name')   # descending

# Slicing return first
Article.objects.all().order_by('name')[0]

# Slicing return last
Article.objects.all().order_by('-name')[0]

# Slicing limit/offset
Article.objects.all().order_by('name')[1..10]

# Updating
article = Article.objects.first()
article.name = 'new name'
article.save()

# One line update
Article.objects.filter(id=4).update(name='new name')

# Deleting
article = Article.objects.first()
article.delete()

# One line delete
article.objects.get(id=1).delete()

# Delete all
Article.objects.all().delete()

# Set ForeignKey field value
model1 = Model(name='dyson')
article.model = model1

# Get ForeignKey value
article1.model.name
model1.article_set.all()

# Add Many-to-Many
article1.tags.add(tag1)
article1.tags.all()
tag1.articles_set.all()
```

## Form

In HTML, a form is a collection of elements inside `<form>...</form>` that allow a visitor to do things like enter text, select options, manipulate objects or controls, and so on, and then send that information back to the server.

```
# app_name/forms.py
from django import forms
class ArticleForm(forms.Form):
    name = forms.Charfield(max_length=100)
    description = forms.Charfield(blank=True, null = True)

# Model Form
from django.forms import ModelForm
from app_name.models import Article
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'description', 'price'] # Use '__all__' for all fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'First Name',
        }
        error_messages = {
            'name': {'required': 'This field is required',},
            }
        help_texts = {
        'name': 'Enter Your First Name',
        }
```

```
# Render form in template
<form method=“post” action=“” novalidate>
    {% csrf_token %}
    {{ form }}
    <button type="submit">Submit</button>
</form>

# Bootstrap (pip install django-crispy-forms + installed_apps: 'crispy_forms')
{% load crispy_forms_tags %}
{{ form|crispy }}
{{ form.email|as_crispy_field }}
```

```
# crispy-tailwind
pip install crispy-tailwind
```

```
# settings.py
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'
```

```
# template usage
{% load tailwind_filters %}
{{ form|crispy}}
```

#### Form validation

```
# forms.py
from django.core.exceptions import ValidationError

# field validation
def clean_first_name(self):
    data = self.cleaned_data['first_name']
    if data = 'Mike':
        raise ValidationError('Your name must not be Mike')
    return data

# form validation
def clean(self):
    first_name = self.cleaned_data['first_name']
    last_name = self.cleaned_data['last_name']
    if first_name + last_name = 'MikeTaylor':
        raise ValidationError('Your name must not be Mike Taylor')
```

## Flash messages

```
messages.success(request, 'Login successful')
messages.error(request, 'Login error')

# Message tags
# debug, info, success, warning and error

# Display flash in template
{% if messages %}
    {% for message in messages %}
        {% message %}
        {% message.tags %}
    {% endfor %}
{% endif %}
```

## User Model

User Model (pre-created)

```
# Get a reference to Django pre-created User model
from django.contrib.auth import get_user_model

User = get_user_model()

# Or if you want to custom user model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # add custom fields and methods

# To make Django use that model go to settings.py and add: AUTH_USER_MODEL = 'app_name.User'
```

## Authentication Configure

#### Authentication : LoginView

```
# LoginView is already pre-created by Django
from django.contrib.auth.views import LoginView

# Add a url to reach that view
path('login/', LoginView.as_view(), name='login')

# By default the LoginView will try to open a template name 'registration/login.html' and send a login form with it.
```

```
# Create a template under registration/login.html
{% extends "base.html" %}
{% block content %}
    <form method="post">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Login</button>
    </form>
{% endblock content %}

# When user click the Login button, the LoginView will try to authenticate the user with the form username ans password.

# If successful il will then login the user and redirect to LOGIN_REDIRECT_URL specified in your settings.py
```

#### Authentication : LogoutView

```
# LogoutView is already pre-created by Django
from django.contrib.auth.views import LogoutView

# Add a url to reach that view
path('logout/', LoginView.as_view(), name='logout')

# Include a link in a template
<a> href="{% url 'logout' %}">Logout</a>

# After link is execute, the user will be logout and redirect to LOGOUT_REDIRECT_URL specified in your settings.py
```

#### Authentication : SignupView

```
# Create a SignupView (that view is not created by default)
# import sinupview form pre-created by Django
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("login")
```

```
# Create template: registration/signup.html
{% extends "base.html" %}
{% block content %}
    <form method="post">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Signup</button>
    </form>
{% endblock content %}
```

```
# Add a url to reach that view
from posts.views import SignupView

path('signup/', SignupView.as_view(), name='signup')

# Optional: Customize the UserCreationForm
# (forms.py)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()
class CustomUserCreationForm(UserCreattionForm):
    class Meta:
        model = User
        fields = ['username']
        fields_classes = {'username': UsernameField}
```

#### Optional pre-created Authentication routes

```
# urls.py
urlpatterns += path('', include('django.contrib.auth.urls'))
# /login, /lougout, /signup, etc.
```

#### Template Authentication helpers

```
# Authentication links
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'signup' %}">Signup</a>
<a href="{% url 'logout' %}">Logout</a>

# Check if user login
{% if request.user.is_authenticated %}
    Logged in as: {{ request.user.username }}
{% endif %}
```

#### Authorization: LoginRequiredMixin and login\_required

```
from django.contrib.auth.mixins import LoginRequiredMixin

# Restrict views to auth user only (views.py)
class PostsCreateView(LoginRequiredMixin, generic.CreateView):
    ...
    ...

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def search_page(request):
    ...
    ...
```

#### Manual Authentication , Login and Logout

```
from django.contrib.auth import authenticate, login

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")

return render(request, "registration/login.html", {})

def logout_page(request):
    logout(request)
    return redirect("index")
```

#### User Change password

```
# set_password will hash the password
user.set_password('raw password')
```

## Create Custom Accounts Model

```
python manage.py startapp accounts
```

```
# Add accounts app to settings.py
INSTALLED_APPS = [ … ,
         'accounts.apps.AccountsConfig',
          ]
.
.
.
AUTH_USER_MODEL = 'accounts.User'
```

```
# accounts/models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,  email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(username, email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Username', max_length=255, unique=True)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone = models.BigIntegerField(verbose_name='Phone Number', unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    is_staff = models.BooleanField(default=False, verbose_name="is_staff")
    is_superuser = models.BooleanField(default=False, verbose_name="is_superuser")

    objects = UserManager()

    # We can use any field for username
    USERNAME_FIELD = 'username'  # or 'email' or 'phone'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
```

```
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'is_active', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='Email')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),label='Password')

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

        widgets = {  # Optional
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(
                attrs={'class': 'form-control', 'type': 'tel', 'maxlength': '11',
                       'minlength': '11',  'onkeypress': 'return isNumber(event)', 'required': 'false'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        else:
            return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

class ChangePassword(forms.Form):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        else:
            return password2
```

```
# accounts/admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from accounts.models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password', 'is_active', 'is_staff')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_editable = ('is_staff', 'is_active')
    list_filter = ('is_staff', 'groups')
    fieldsets = (
        (None, {'fields': ( 'username', 'email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Group Permissions', {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions'),
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
        ('Group Permissions', {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions'),
        })
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username', 'email', 'phone')
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
# unregister the Group model from admin.
# admin.site.unregister(Group)
```

```
# accounts/urls.py
from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.userLogin, name='login'),
    path('register/', views.userRegister, name='register'),
    path('logout/', views.LogoutPage, name='logout')
]
```

```
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from accounts.forms import LoginForm, RegisterForm
from django.contrib import messages
from accounts.models import User

def userRegister(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not User.objects.filter(email=cd['username']).exists():
                if not User.objects.filter(email=cd['email']).exists():
                    user = User.objects.create_user(
                        username=cd['username'], phone=cd['phone'], email=cd['email'], password=cd['password1'])
                    user.save()
                    login(request, user)
                    messages.success(request, _("You successfully registered a user"), extra_tags="success")
                    return redirect('app_name:home')
                else:
                    messages.error(request, _("This Email is exists"), extra_tags="warning")
            else:
                messages.error(request, _("This Username is exists"), extra_tags="warning")
        else:
            import json
            er = json.loads(form.errors.as_json())
            for e in er:
                messages.error(request, er[e][0]['message'], 'warning')
    return render(request, 'accounts/register.html', {'form': form})

def userLogin(request):
    if not request.user.is_active:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if User.objects.filter(username=cd['username']).exists():
                    user = authenticate(request, username=cd['username'], password=cd['password'])
                    if user is not None:
                        login(request, user)
                        messages.success(request, _("logged in successfully"), extra_tags="success")
                        return redirect('app_name:home')
                    else:
                        messages.error(request, _("your username Or Password is wrong"), extra_tags="warning")
                else:
                    messages.error(request, _("No account created with this username"), extra_tags="warning")
                    return redirect('accounts:login')
            else:
                messages.error(request, _("Please enter your information correctly"), extra_tags="warning")
        else:
            form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('app_name:home')

@login_required()
def LogoutPage(request):
    logout(request)
    messages.success(request, _("You Logged Out successfully"), extra_tags="success")
    return redirect('app_name:home')
```

## Send Email

```
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Send email function
from django.core.email import send_mail

send_mail(
    subject = "A new post has been created",
    messsage = "Go to the web site to see the detail",
    from_email = "test@test.com",
    recipient_list = ["test2@text.com"]
)
```

## Signals

```
# models.py
from django.db.models.signals import post_save, pre_save

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Launch the post_user_create_singal method if User model is save
post_save.connect(post_user_created_signal, sender=User)
```

## Seed

```
from app_name.models import Product, Category
from django.shortcuts import HttpResponse
from faker import Faker

def seed(request):
    Product.objects.all().delete()
    Category.objects.all().delete()

    category = Category()
    category.name = "Sports"
    category.save()

    category = Category()
    category.name = "Home"
    category.save()

    fake = Faker()
    for _ in range(100):
        product = Product()
        product.name = fake.unique.word()
        product.short_description = fake.sentence()
        product.main_picture = fake.image_url()
        product.price = fake.random_digit() * 10
        product.category =  Category.objects.order_by('?').first()
        product.save()

    return HttpResponse('Seeded')
```

## Environment Variables

#### .env key/value file

```
$ pip install python-decouple
```

##### Create a file name '.env' in the root folder of your project

```
SECRET_KEY = 'your secret key'
ALLOWED_HOST = 127.0.0.1
```

##### In settings.py change security related settings to point to the .env file

```
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOST = config('ALLOWED_HOST')
```

## Asynchronous Task with Django Celery Redis

Celery is a distributed task queue that can collect, record, schedule, and perform tasks outside of your main program.

##### Step 1: Install Celery Using pip

```
pip install celery       # pip install celery[redis]
```

##### Step 2. Add celery.py File in Your Project Module

```
# your_project/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','your_project_name.settings')
app = Celery('your_project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

##### Step 3: Import the Celery App to Django

To ensure that the Celery app is loaded when Django starts, add the following code into the `__init__.py` file that sits on the project module beside on settings.py file.

```
# your_project/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)
```

##### Step 4: Download and Run Redis as a Celery ‘broker’

```
redis-server
```

You can test that Redis is working properly by typing this into your terminal:

```
redis-cli ping
```

> Redis should reply with PONG - try it!

##### Step 5: Add Redis as a Dependency in the Django Project:

```
pip install redis
```

##### step 6: Celery Stuff Configure to the Django Settings File

Once Redis is up, add the following code to your settings.py file and use celery-result

```
pip install django-celery-results
```

> This extension enables you to store Celery task results using the Django ORM.
> 
> It defines a single model (`django_celery_results.models.TaskResult`) used to store task results, and you can query this database table like any other Django model.

```
INSTALLED_APPS = [
                … ,
                'django_celery_results',
                ]

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'redis://localhost:6379/1',
        "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

##### That’s it! You should now be able to use Celery with Django

Test that the Celery worker is ready to receive tasks:

```
celery -A your_project_name worker -l info
```

> The most important task is: Always run a worker is needed to execute the celery task
> 
> if any error throws from Redis like this:

```
AttributeError: 'str' object has no attribute 'items'
```

*   the solution is: you have to use Redis old version

#### Add a New Task to the Celery Step by Step:

##### Step 1: Add tasks.py File to Your Django App.

```
# app_name/tasks.py
from celery import shared_task
from celery.decorators import task
from time import sleep

@task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    return('first_task_done')

@shared_task
def test_func():
    for i in range(10):
        print(i)
    return 'End_OK'

@shared_task
def adding(x, y):
    time.sleep(10)
    result = x + y
    return result
```

##### Step 2: Assign Task to the Celery.

You need to assign a task to the celery. To assign this task you need to call this function with something different. celery gives us two methods `delay()` and `apply_async()` to call task.

```
# Normal function call in python
my_first_task()

# add task to the celery with function call
my_first_task.delay()
```

> you can send argument to the function using the delay method.
> 
> To check celery on the action open a separate tab of the terminal then go to the project directory (activate environment if you are using one) and run this command again

```
celery -A your_project_name worker -l info
```

##### Create a View in your App

```
# app_name/views.py
from django.http import HttpResponse
from app_name.tasks import my_first_task, test_func, adding

def index(request):
    my_first_task.delay(10)
    result = adding.delay(x=4, y=5)
    return HttpResponse(f'response done. {result}')

def test(request):
    test_func.delay()
    return HttpResponse("Done")
```

##### Then call the view from your app URL

```
# app_name/urls.py
from django.urls import path
from app_name.views import index, test
urlpatterns = [
    path('celery-index/', index, name='celery_index_url'),
    path('celery-test/', test, name='celery_test_url'),
]
```

### Celery In Production Using Supervisor on Linux Server Step by Step:

#### Step 1: Install Supervisor on Ubuntu Server

```
sudo apt-get install supervisor
```

#### Step 2: Add .conf File in Supervisor

```
sudo nano /etc/supervisor/conf.d/app_name.conf
```

> app\_name can be anything you like, it should be similar to your project name.

#### Step 3: Add some Configure in app\_name.conf

```
[program:your_app_name]
command=/path/to/env/bin/celery worker -A your_project_name --loglevel=INFO
directory=/path/to/workflow/your_project_name/
user=www-data
autostart=true
autorestart=true
stdout_logfile=/path/to/workflow/your_project_name/logs/celeryd.log
redirect_stderr=true
```

> let's describe the configure file:

```
[program:your_app_name]
#The name of your supervisord program

command=/path/to/env/bin/celery worker -A your_project_name --loglevel=INFO
#Set full path to celery program if using virtualenv

directory=/path/to/workflow/your_project_name/
#The directory to your Django project

user=www-data
#The web server has to be run under a specific user. That user must exist.

autostart=true
#If true, this program will start automatically when supervisord is started

autorestart=true
#May be one of false, unexpected, or true. If false, the process will never be autorestarted. If unexpected, the process will be restart when the program exits with an exit code that is not one of the exit codes associated with this process’ configuration (see exitcodes). If true, the process will be unconditionally restarted when it exits, without regard to its exit code.

stdout_logfile=/path/to/workflow/your_project_name/logs/celeryd.log
#Put process stdout output in this file

redirect_stderr=true
#If true, cause the process’ stderr output to be sent back to supervisord on its stdout file descriptor (in UNIX shell terms, this is the equivalent of executing /the/program 2>&1).
```

#### Step 4: Inform Configuration to the Server

After adding a new program, we should run the following two commands, to inform the server to reread the configuration files and to apply any changes.

```
sudo supervisorctl reread
sudo supervisorctl update
```

#### Managing Supervisor App

```
sudo supervisorctl
```

You will be greeted with a list of the registered processes. You will see a process called `your_app_name` with a `RUNNING` status.

```
your_app_name                 RUNNING   pid 6853, uptime 0:22:30
supervisor>
```

Type `help` for a list of available commands.

```
supervisor> help
default commands (type help <topic>):
=====================================
add    exit      open  reload  restart   start   tail
avail  fg        pid   remove  shutdown  status  update
clear  maintail  quit  reread  signal    stop    version
```

In a nutshell, we can `start`, `stop` and `restart` programs bypassing the program name as an argument to the respective command.

We can also take a look at the program output with the `tail` command.

Once you are finished, you can `quit`.

```
supervisor> quit
```

## Deployment Django

### Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu

#### Step 1 — Installing the Packages from the Ubuntu Repositories

```
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

#### Step 2 — Creating the PostgreSQL Database and User

```
sudo -u postgres psql
```

*   First, create a database for your project:

```
postgres=# CREATE DATABASE myproject;
```

*   Next, create a database user for our project. Make sure to select a secure password:

```
postgres=# CREATE USER myprojectuser WITH PASSWORD 'password';
```

*   Afterwards, you’ll modify a few of the connection parameters for the user that you just created

```
postgres=# ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
postgres=# ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

*   Now, you can give the new user access to administer the new database:

```
postgres=# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

*   When you are finished, exit out of the PostgreSQL prompt by typing:

```
postgres=# \q
```

#### Step 3 — Creating a Python Virtual Environment for your Project

*   thin the project directory, create a Python virtual environment by typing:

```
mkdir ~/myprojectdir
cd ~/myprojectdir
```

*   Within the project directory, create a Python virtual environment by typing:

```
python3 -m venv myprojectenv
```

*   Before installing your project’s Python requirements, you will need to activate the virtual environment. You can do that by typing:

```
source myprojectenv/bin/activate
```

*   With your virtual environment active, install Django, Gunicorn, and the psycopg2 PostgreSQL adaptor with the local instance of pip

```
(myprojectenv)$ pip install django gunicorn psycopg2-binary
```

#### Step 4 — Creating and Configuring a New Django Project

*   With your Python components installed, you can now create the actual Django project files.

```
(myprojectenv)$ django-admin startproject myproject ~/myprojectdir
```

*   The first thing you should do with your newly created project files is adjust the settings. Open the settings file in your text editor:

```
(myprojectenv)$ nano ~/myprojectdir/myproject/settings.py
```

*   Start by locating the ALLOWED\_HOSTS directive.

```py

 ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']
```

*   Next, find the section that configures database access. It will start with DATABASES. The configuration in the file is for a SQLite database.

```py
. . .
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
. . .
```

*   Next, move down to the bottom of the file and add a setting indicating where the static files should be placed.

```
. . .
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

#### Step 5 — Completing Initial Project Setup

*   Now, you can migrate the initial database schema to our PostgreSQL database using the management script:

```
(myprojectenv)$ ~/myprojectdir/manage.py makemigrations
(myprojectenv)$ ~/myprojectdir/manage.py migrate
```

*   Create an administrative user for the project by typing:

```
(myprojectenv)$ ~/myprojectdir/manage.py createsuperuser
```

*   You can collect all of the static content into the directory location that you configured by typing:

```
(myprojectenv)$ ~/myprojectdir/manage.py collectstatic
```

#### Step 6 — Testing Gunicorn’s Ability to Serve the Project

```
(myprojectenv)$ cd ~/myprojectdir
(myprojectenv)$ gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

*   You’re now finished configuring your Django application. You can back out of our virtual environment by typing:

```
(myprojectenv)$ deactivate
```

#### Step 7 — Creating systemd Socket and Service Files for Gunicorn You have tested tha

```
sudo nano /etc/systemd/system/gunicorn.socket
```

*   Inside, you will create a `[Unit]` section to describe the socket, a `[Socket]` section to define the socket location, and an `[Install]` section to make sure the socket is created at the right time:

```bash

 [Unit]

 Description=gunicorn socket

[Socket]

 ListenStream=/run/gunicorn.sock

[Install]

 WantedBy=sockets.target
```

*   Save and close the file when you are finished.
*   Next, create and open a systemd service file for Gunicorn with sudo privileges in your text editor. The service filename should match the socket filename with the exception of the extension:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

*   You can now start and enable the Gunicorn socket. This will create the socket file at /run/gunicorn.sock now and at boot. When a connection is made to that socket, systemd will automatically start the gunicorn.service to handle it

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

#### Step 8 — Checking for the Gunicorn Socket File

*   Check the status of the process to find out whether it was able to start:

```
sudo systemctl status gunicorn.socket
```

*   Next, check for the existence of the gunicorn.sock file within the /run directory:

```
file /run/gunicorn.sock
```

#### Step 9 — Testing Socket Activation

```
sudo systemctl status gunicorn
```

*   To test the socket activation mechanism, you can send a connection to the socket through curl by typing:

```
curl --unix-socket /run/gunicorn.sock localhost
```

*   You should receive the HTML output from your application in the terminal. This indicates that Gunicorn was started and was able to serve your Django application. You can verify that the Gunicorn service is running by typing:

```
sudo systemctl status gunicorn
```

*   Check your /etc/systemd/system/gunicorn.service file for problems. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing

```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

#### Step 10 — Configure Nginx to Proxy Pass to Gunicorn

*   Start by creating and opening a new server block in Nginx’s sites-available directory:

```
sudo nano /etc/nginx/sites-available/myproject
```

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/sammy/myprojectdir/staticfiles/;
    }

    location /media {
        autoindex on;
        alias /home/sammy/myprojectdir/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

*   Save and close the file when you are finished. Now, you can enable the file by linking it to the sites-enabled directory:

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

*   Test your Nginx configuration for syntax errors by typing:

```
sudo nginx -t
```

*   If no errors are reported, go ahead and restart Nginx by typing:

```
sudo systemctl restart nginx
```

*   you need to open up your firewall to normal traffic on port 80

```
sudo ufw allow 'Nginx Full'
```

You should now be able to go to your server’s domain or IP address to view your application.

#### Step 11 — Troubleshooting Nginx and Gunicorn

*   Nginx Is Showing the Default Page Instead of the Django Application

```
sudo tail -F /var/log/nginx/error.log
```

*   Django Is Displaying: “could not connect to server: Connection refused”

```
sudo systemctl status postgresql
```

*   If it is not, you can start it and enable it to start automatically at boot (if it is not already configured to do so) by typing:

```
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

If you change Gunicorn socket or service files, reload the daemon and restart the process by typing:

```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
```

If you change the Nginx server block configuration, test the configuration and then Nginx by typing:

```
sudo nginx -t && sudo systemctl restart nginx
```








# The Ultimate Django Rest Framework Cheat Sheet: A Comprehensive GuideDjango Rest Framework CheetSheet: Mastering API Development

## Serializers

Serializers play a pivotal role in converting complex data types, such as Django models, into Python data types that can be easily rendered into JSON, XML, or other content types. Here's a quick guide to DRF serializers:

*   Define a serializer class by inheriting from `serializers.Serializer` or `serializers.ModelSerializer` (for model-based serializers).
*   Specify fields using class attributes like `CharField`, `IntegerField`, etc.
*   Implement validation logic using methods like `validate_<field_name>()`.
*   Use serializers to handle both input data validation and output data rendering.

```python
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

## Copy Basic View Types

Views in DRF are analogous to Django's views, but tailored specifically for handling API requests. They're responsible for processing incoming requests and returning appropriate responses.

DRF provides different types of views to handle various use cases:

*   `APIView`: The base class for all views. It provides basic request/response handling.
*   `ViewSet`: Combines multiple views (list, create, retrieve, update, delete) into a single class.
*   `GenericAPIView`: Provides common behavior for CRUD operations.
*   `ModelViewSet`: A combination of `GenericAPIView` and `ViewSet` tailored for model-backed APIs.

## HTTP Methods and Corresponding Views

DRF maps HTTP methods to view methods:

*   `GET`: `list()`, `retrieve()`
*   `POST`: `create()`
*   `PUT`: `update()`
*   `PATCH`: `partial_update()`
*   `DELETE`: `destroy()`

## Authentication and Permissions

DRF provides authentication and permission classes to control access to views:

```python
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class MyView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
```

## Copy Custom Permissions

Define custom permissions to control access:

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

## Copy ViewSets and Routers

DRF offers ViewSets for a more concise way of defining views:

```python
from rest_framework import viewsets

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

Copy `ViewSets` can be registered with `routers` to generate URLs automatically:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet)
urlpatterns += router.urls
```

## Copy Pagination

DRF offers built-in pagination classes for handling large data sets:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## Copy Filtering and Ordering

Filter and order querysets using URL query parameters:

```python
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
```

## Copy API Versioning

You can version your API to avoid breaking changes:

```python
urlpatterns = [
    path('v1/', include('myapp.urls')),  # Use API versioning in URLs
]
```

## Copy Versioning

Version your APIs using DRF's versioning classes:

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

## Copy Throttling and Rate Limiting

Protect your API using throttling and rate limiting:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}
```

## Copy Content Negotiation

DRF supports content negotiation for handling different media types (JSON, XML, etc.):

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
    ],
}
```

## Copy Exception Handling

DRF provides built-in exception handling and error responses:

```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['custom_message'] = 'An error occurred'
    return response
```

## Copy Overriding Generic Views

You can customize the behavior of generic views by overriding methods:

```python
class MyModelListCreateView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

## Copy View Function Decorators

Use decorators to add behavior to views, such as authentication and permission checks:

```python
from rest_framework.decorators import authentication_classes, permission_classes

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_view(request):
    # View logic here
```

## Copy Serializer Context

Pass additional context to serializers:

```python
serializer = MyModelSerializer(instance, context={'request': request})
```

Copy Rendering Custom Data

Render custom data using `Response` and `status`:

```python
from rest_framework.response import Response
from rest_framework import status

class MyView(APIView):
    def get(self, request):
        data = {'message': 'Hello, world!'}
        return Response(data, status=status.HTTP_200_OK)
```

## Copy File Uploads

Handle file uploads in views using serializers:

```css
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['file']

class MyModelView(APIView):
    def post(self, request):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## Copy Testing Views

DRF provides testing tools to test views and API functionality:

```python
from rest_framework.test import APITestCase

class MyViewTest(APITestCase):
    def test_my_view(self):
        response = self.client.get('/my-view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

Copy Serializer Validation

Add custom validation to serializers using `validate_<field_name>` methods:

```python
class MySerializer(serializers.ModelSerializer):
    def validate_my_field(self, value):
        if value < 0:
            raise serializers.ValidationError('Value cannot be negative')
        return value
```

## Copy DRF with Function-Based Views

You can use DRF features with function-based views:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def my_function_view(request):
    data = {'message': 'Hello, function view!'}
    return Response(data)
```

Copy Serializing Relationships

Handle related data using serializers:

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'books']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = ['title', 'author']
```

## Copy Combining Views

Combine multiple views into one using `ViewSets` and `mixins`:

```python
from rest_framework import mixins, viewsets

class MyViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

## Copy Caching

Cache responses using DRF's caching decorators:

```python
from rest_framework.decorators import cache_page

class MyView(APIView):
    @cache_page(60 * 15)  # Cache for 15 minutes
    def get(self, request):
        # ...
```

## Copy DRF's Mixins

Leverage DRF's mixins for common CRUD operations:

```python
from rest_framework import mixins, viewsets

class MyViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
```

## Copy Custom Action

Create custom actions in viewsets:

```python
class MyViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def do_something(self, request, pk=None):
        # Custom action logic
```

## Copy Query Parameters

Retrieve query parameters in views:

```python
class MyView(APIView):
    def get(self, request):
        param_value = request.query_params.get('param_name')
        # ...
```

## Copy Custom Nested Relationships

You can use serializer methods to create custom nested relationships:

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_data = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_author_data(self, obj):
        author = obj.author
        return AuthorSerializer(author, context=self.context).data
```

## Copy Multiple Serializers for a Single View

## Use different serializers for different request methods:

```python
class MyModelAPIView(APIView):
    serializer_class_read = MyModelReadSerializer
    serializer_class_write = MyModelWriteSerializer

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD']:
            return self.serializer_class_read
        return self.serializer_class_write

    def get(self, request):
        # ...
    
    def post(self, request):
        # ...
```

## Copy Related Data Creation

Override `perform_create` in your view to handle related data creation:

```css
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        products_data = self.request.data.get('products')
        if products_data:
            for product_data in products_data:
                product = Product.objects.get(id=product_data['id'])
                OrderItem.objects.create(order=order, product=product, quantity=product_data['quantity'])
```
