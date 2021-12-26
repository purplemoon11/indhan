from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # Client page
    path('', views.homePage, name='home'),
    path('entry/', views.entryPage, name='entry'),
    path('report/', views.reportPage, name='report'),
    path('update/<int:id>', views.updatePage, name='update'),

    # Login, Register and LogOut form
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/',views.logoutUser, name='logout'),

    #admin 
    path('adminpage/', views.adminPage, name='adminpage'),
    path('adminentry/', views.adminEntry, name='adminentry'),
    path('adminreport/', views.adminReport, name='adminreport'),
    path('adminpublish/', views.adminPublish, name='adminpublish'),
    path('adminupdate/<int:id>', views.adminUpdate, name='adminupdate'),
    path('<int:id>/', views.deletePage, name='delete'),

    #Searching for admin & client
    path('search-gasloine', csrf_exempt(views.search_list), name='search_list'),

    #render_pdf_view
    #path('renderpdfview/<int:id>/', views.render_pdf_view, name='render_pdf_view'),
    path('test/<int:id>', views.test, name='test'),

]
