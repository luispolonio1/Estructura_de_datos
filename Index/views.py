from django.shortcuts import render , get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from .forms import UsuarioForm


def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'Home.html', {'usuarios': usuarios})



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
    return render(request, 'Registros.html')

