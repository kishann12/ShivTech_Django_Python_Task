from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name = "index"),
    path("create_project", views.create_product, name='create'),
    path("product/<str:id>", views.detail, name = 'detail'),
    path("", views.SignupPage, name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),

]