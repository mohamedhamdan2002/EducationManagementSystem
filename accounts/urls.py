from django.urls import path

from .views import (
    login_view, 
    logout_view, 
    profile_view,
    sign_up_view,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]