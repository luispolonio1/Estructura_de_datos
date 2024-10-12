from django.shortcuts import render , get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
import json


def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'Home.html', {'usuarios': usuarios})



@csrf_exempt
def guardar_usuario(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nombre = data.get("nombre")
        cedula = data.get("cedula")

        if nombre and cedula:
            usuario = Usuario(nombre=nombre, cedula=cedula)
            usuario.save()
            usuarios = Usuario.objects.all()
            return render(request, 'Home.html', {'usuarios': usuarios})

    usuarios = Usuario.objects.all()
    return render(request, 'Home.html', {'usuarios': usuarios})





def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('index')

