from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('atender_usuario/', views.atender_usuario, name='atender_usuario'),
    path('registros/', views.ver_registros_diarios, name='ver_registros_diarios'),
    path('registros/<int:registro_id>/', views.detalle_registro_diario, name='detalle_registro_diario'),
    path('descargar_archivo/<int:registro_id>/', views.descargas, name='descargar_archivo'),
    path('cargar_datos/',views.cargar_datos, name='carga_datos'),
]
