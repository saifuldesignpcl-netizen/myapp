from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
]
