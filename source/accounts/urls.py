from django.urls import path
from accounts.views import login_view, logout_view, register_view, UsersView,\
    user_activate, UserDetailView, UserPersonalInfoChangeView, UserPasswordChangeView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/activate/', user_activate, name='user_activate'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update', UserPersonalInfoChangeView.as_view(), name='update'),
    path('<int:pk>/password_change', UserPasswordChangeView.as_view(), name='password_change'),
    path('users/', UsersView.as_view(), name='all_users_view')
]

app_name = 'accounts'
