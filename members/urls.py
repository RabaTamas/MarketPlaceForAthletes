from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
    path('login/', views.login_user, name='login'), 
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('about/', views.about, name='about'),
    path('item/<int:pk>/', views.item, name='item'),
    path('addlisting/', views.createlisting, name='addlisting' ),
    path('my-ads/', views.my_ads, name='my_ads' ),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('advertisers/', views.advertisers, name='advertisers'),
    path('advertisers/add_score/<int:user_id>/', views.add_score, name='add_score'),
     
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
         
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]