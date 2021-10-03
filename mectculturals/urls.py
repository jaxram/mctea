from django.urls import path


from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('excel_conversion',views.excel_conversion,name='excel_conversion'),
    path('login_validation',views.login_validation,name='login_validation'),
    path('password_reset/<int:uid>/<str:token>',views.password_reset,name='password_reset'),
    path('password_confirm/<int:uid>/<str:token>',views.password_confirm,name='password_confirm'),
    path('password_save',views.password_save,name='password_save'),
    path('post_save',views.post_save,name='post_save'),
    path('event_save',views.event_save,name='event_save'),
    
 
]

