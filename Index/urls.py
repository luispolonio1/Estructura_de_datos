from django.urls import path
from . import views


urlpatterns=[
    path('',views.index,name='index'),
    path('guardar_usuario/',views.guardar_usuario,name='guardar_usuario'),
    path('eliminar/<int:usuario_id>',views.eliminar_usuario,name='eliminar'),
    path('registros',views.Registros_vistas,name='registros'),
]