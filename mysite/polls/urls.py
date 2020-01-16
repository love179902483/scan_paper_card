from django.urls import path
from . import views
from . import form

urlpatterns = [
        path('1/', views.index, name='index'),
        path('test/', views.test, name='test'),
        path('test/form/', form.testSearch, name='testsearch'),
        ]
