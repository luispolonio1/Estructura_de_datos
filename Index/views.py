from django.shortcuts import render , get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario,UsuarioAtendido,RegistroHoy
from .forms import UsuarioForm
from datetime import date
from .Nodos import Lista_nodos
@csrf_exempt
def index(request):
        usuarios = Usuario.objects.all()
        lista_nodos = Lista_nodos()
        for usuario in usuarios:
            lista_nodos.insertar_final_nodo(usuario)
        ticket_actual = lista_nodos.obtener_y_eliminar_primero()
        lista_nodos = lista_nodos.imprimir()

        return render(request, 'Home.html', {'lista_nodos': lista_nodos,'ticket_actual': ticket_actual})
    # usuarios = Usuario.objects.all()
    # return render(request, 'Home.html', {'usuarios': usuarios,'ticket_actual': ticket_actual})



@csrf_exempt
def guardar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Agregar el usuario al registro diario
            agregar_usuario_al_registro_diario(usuario)
            return redirect('index')
    else:
        form = UsuarioForm()

    usuarios = Usuario.objects.all()
    return render(request, 'Registro.html', {'form': form, 'usuarios': usuarios})



def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('index')

# @csrf_exempt
# def Registros_vistas(request):
#     # Obtener la lista de usuarios atendidos desde UsuarioAtendido
#     usuarios_atendidos = UsuarioAtendido.objects.all()
#
#     # Renderizar una nueva plantilla para los usuarios atendidos
#     return render(request, 'Registros.html', {'usuarios_atendidos': usuarios_atendidos})




def atender_usuario(request):
    # Obtener el primer ticket no atendido (FIFO)
    usuario = Usuario.objects.order_by('fecha_registro').first()

    if usuario:
        # Crear un registro en la tabla `UsuarioAtendido`
        UsuarioAtendido.objects.create(
            nombre=usuario.nombre,
            cedula=usuario.cedula,
            edad=usuario.edad,
            fecha_registro=usuario.fecha_registro,
        )
        usuario.delete()  # Eliminar el ticket original

    return redirect('index')


def agregar_usuario_al_registro_diario(usuario):
    # Verificar si ya existe un registro para hoy
    hoy = date.today()
    registro, creado = RegistroHoy.objects.get_or_create(fecha=hoy)

    # Agregar el usuario al registro de hoy
    registro.usuarios.add(usuario)
    registro.save()



@csrf_exempt
def ver_registros_diarios(request):
    # Obtener todos los registros diarios
    registros = RegistroHoy.objects.all().order_by('-fecha')# Ordena por fecha de forma descendente
    hoy = date.today()
    usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=hoy)
    return render(request, 'Registros.html', {'registros': registros,'usuarios_atendidos': usuarios_atendidos})



@csrf_exempt
def detalle_registro_diario(request, registro_id):
    hoy = date.today()
    # Obtener el registro diario específico
    registro = get_object_or_404(RegistroHoy, id=registro_id)
    usuarios_atendidos = UsuarioAtendido.objects.all()
    return render(request, 'detalle_registro_diario.html', {'registro': registro, 'usuarios_atendidos': usuarios_atendidos})





