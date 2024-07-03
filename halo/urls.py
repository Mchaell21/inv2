from django.urls import path
from . import views 

urlpatterns = [
    path('home', views.home , name='home'),
    path('register/', views.register_page, name='register'),
    path('session_log/', views.sess_login, name='sesLog'),
    path('logout/', views.logout_page, name='logout'),
    path('change_pass/',views.change_pass, name= 'changePass'),
    path('postchangePass/', views.postchangePass, name= 'postPass'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('invoice/', views.invoice, name = 'invoice'),
    path('product/', views.product, name = 'product'),
    path('company/', views.company, name = 'company'),
    path('invoice/create/', views.createInvoice, name='create-invoice'),
    path('invoice/create-build/<slug:slug>', views.createBuildInvoice, name = 'create-build-invoice'),
]