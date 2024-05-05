from django.contrib import admin
from django.urls import path
from .views import GetCodeView

urlpatterns = [
    path('get-code', GetCodeView.as_view(), name='get-code'),
]
