from django.shortcuts import render , get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario,UsuarioAtendido
from .forms import UsuarioForm


def index(request):
    usuarios = Usuario.objects.all()
    ticket_actual = Usuario.objects.order_by('fecha_registro').first()
    return render(request, 'Home.html', {'usuarios': usuarios,'ticket_actual': ticket_actual})



@csrf_exempt
def guardar_usuario(request):
    form = UsuarioForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        form = UsuarioForm()
    usuarios = Usuario.objects.all()
    return render(request,'Registro.html',{'form':form,'usuarios':usuarios})


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('index')


def Registros_vistas(request):
    # Obtener la lista de usuarios atendidos desde UsuarioAtendido
    usuarios_atendidos = UsuarioAtendido.objects.all()

    # Renderizar una nueva plantilla para los usuarios atendidos
    return render(request, 'Registros.html', {'usuarios_atendidos': usuarios_atendidos})




def atender_usuario(request):
    # Obtener el primer ticket no atendido (FIFO)
    usuario = Usuario.objects.order_by('fecha_registro').filter(atendido=False).first()

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
