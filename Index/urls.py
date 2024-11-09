from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('atender_usuario/', views.atender_usuario, name='atender_usuario'),
    path('registros/', views.ver_registros_diarios, name='ver_registros_diarios'),
    path('registros/<int:pk>/', views.detalle_registro_diario, name='detalle_registro_diario'),
    path('descargar_archivo/<int:pk>/', views.descargas, name='descargar_archivo'),
    path('cargar_datos/',views.cargar_datos, name='carga_datos'),
    path('buscar/', views.buscar_usuario, name='buscar_usuario'),
    path('descargar_noatendidos',views.descargas_Noatendidos, name='descargar_noatendidos'),
    path('reiniciar-ids/', views.reiniciar_ids, name='reiniciar_ids'),
]
