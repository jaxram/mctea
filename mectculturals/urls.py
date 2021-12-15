from django.urls import path


from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('excel_conversion',views.excel_conversion,name='excel_conversion'),
    path('login_validation',views.login_validation,name='login_validation'),
    path('password_reset/<str:token>',views.password_reset,name='password_reset'),
    path('password_confirm/<str:token>',views.password_confirm,name='password_confirm'),
    path('password_save',views.password_save,name='password_save'),
    path('post_save',views.post_save,name='post_save'),
    path('event_save',views.event_save,name='event_save'),
    path('init_home',views.init_home,name='init_home'),
    path('edit_prof',views.edit_prof,name='edit_prof'),
    path('dp_update',views.dp_update,name='db_update'),
    path('init_events',views.init_events,name='init_events'),
    path('authenticate',views.authenticate,name='authenticate'),
    path('init_queries',views.init_queries,name='init_queries'),
    path('raise_query',views.raise_query,name='raise_query'),
    path('respond_query',views.respond_query,name='respond_query'),
    path('register_event',views.register_event,name='register_event'),
    path('delete_query',views.delete_query,name='delete_query'),
    path('unregister',views.unregister,name='unregister'),
    path('excel_filter',views.excel_filter,name='excel_filter')
]

