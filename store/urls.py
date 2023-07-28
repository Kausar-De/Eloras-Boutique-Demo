from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.homepage, name = "homepage"),
    path('store/', views.store, name = "store"),
    path('myorders/', views.myOrders, name = "myorders"),
    
    path('cart/', views.cart, name = "cart"),
    path('update_item/', views.updateItem, name = "update_item"),
    path('checkout/', views.checkout, name = "checkout"),
    path('process_order/', views.processOrder, name = "process_order"),
]