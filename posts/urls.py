from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #users
    path('update-profile/', views.ProfileUpdateView.as_view(), name='profile-update'),# set
    path('users/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.ProfileEditView.as_view(),name='profile_edit'), # update

]
