from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup', views.signup_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('profile', views.profile),
]

# urlpatterns += static(setiing)