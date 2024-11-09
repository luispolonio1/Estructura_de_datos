from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
from .models import Usuario,UsuarioAtendido,RegistroHoy
from .forms import UsuarioForm ,CSVUploadForm
from datetime import date,datetime
from .Nodos import Lista_nodos
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
import csv


def iniciar_nodos():
    usuarios = Usuario.objects.all()
    lista_nodos = Lista_nodos()
    for usuario in usuarios:
        lista_nodos.insertar_final_nodo(usuario)
    return lista_nodos




def index(request):
        lista_nodos=iniciar_nodos()
        criterio = request.GET.get('criterio', 'nombre')
        ticket_actual = lista_nodos.obtener_y_eliminar_primero()
        lista_nodos_datos = lista_nodos.imprimir()
        lista_nodos_datos = merge_sort(lista_nodos_datos, criterio)

        return render(request, 'Home.html',  {'lista_nodos_datos': lista_nodos_datos, 'ticket_actual': ticket_actual, 'criterio': criterio})


def merge_sort(data_list, criterio):
    if len(data_list) <= 1:
        return data_list

    mid = len(data_list) // 2
    left_half = merge_sort(data_list[:mid], criterio)
    right_half = merge_sort(data_list[mid:], criterio)

    return merge(left_half, right_half, criterio)

def merge(left, right, criterio):
    sorted_list = []
    while left and right:
        if criterio == 'nombre':
            if getattr(left[0], criterio).upper() <= getattr(right[0], criterio).upper():
               sorted_list.append(left.pop(0))
            else:
               sorted_list.append(right.pop(0))
        elif getattr(left[0], criterio) <= getattr(right[0], criterio):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))

    sorted_list.extend(left if left else right)
    return sorted_list


@login_required
def reiniciar_ids(request):
    if request.method == 'POST':
        try:
            tabla = Usuario._meta.db_table
            Usuario.objects.all().delete()
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabla}'")
        except Exception as e:
            messages.error(request, f'Error al reiniciar los IDs: {str(e)}')

        return redirect('index')

def guardar_usuario(request):
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario guardado exitosamente")
            return redirect('index')
    else:
        messages.warning(request, "Ocurrio un error , Por Favor Ingrese bien sus datos")

    return render(request, 'Registro.html', {'form': form})


def eliminar_usuario(request,pk):
    usuario = get_object_or_404(Usuario,pk=pk)
    usuario.delete()
    return redirect('index')


def atender_usuario(request):
    usuario = Usuario.objects.all().first()

    if usuario:
        UsuarioAtendido.objects.create(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            cedula=usuario.cedula,
            edad=usuario.edad,
            fecha_registro=usuario.fecha_registro,
        )
        usuario.delete()
    return redirect('index')


def ver_registros_diarios(request):

        hoy = date.today()
        registro_hoy, created = RegistroHoy.objects.get_or_create(fecha=hoy)
        registros = RegistroHoy.objects.all().order_by('-fecha')
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=hoy)

        return render(request, 'Registros.html', {'registros': registros,'usuarios_atendidos': usuarios_atendidos})


def detalle_registro_diario(request,pk):
    registro = get_object_or_404(RegistroHoy,pk=pk)
    usuarios_atendidos = UsuarioAtendido.objects.all()
    return render(request, 'detalle_registro_diario.html', {'registro': registro, 'usuarios_atendidos': usuarios_atendidos})


def descargas(request,pk):
    if request.method == 'GET':
        registro = get_object_or_404(RegistroHoy,pk=pk)
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=registro.fecha)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="registro_{registro.fecha}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre','Apellido', 'Cédula', 'Edad', 'Fecha de Registro'])
        for usuario in usuarios_atendidos:
            writer.writerow([usuario.nombre,usuario.apellido, usuario.cedula, usuario.edad, usuario.fecha_registro])

        return response

def descargas_Noatendidos(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.filter(fecha_registro=date.today())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="registro_{date.today()}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre','Apellido', 'Cédula', 'Edad', 'Fecha de Registro'])
        for usuario in usuarios:
            writer.writerow([usuario.nombre,usuario.apellido, usuario.cedula, usuario.edad, usuario.fecha_registro])
        return response

def cargar_datos(request):
    if request.method == 'POST':
        forms = CSVUploadForm(request.POST, request.FILES)
        if forms.is_valid():
            archivo_csv = request.FILES['file']
            try:
                decoded_file = archivo_csv.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                header = next(reader)
                for fila in reader:
                    nombre,apellido, cedula, edad, fecha_registro = fila
                    fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()
                    usuario_atendido = UsuarioAtendido.objects.create(
                        nombre=nombre,
                        apellido=apellido,
                        cedula='0' + cedula,
                        edad=int(edad),
                        fecha_registro=fecha_registro
                    )
                    registro, creado = RegistroHoy.objects.get_or_create(fecha=fecha_registro)
                    registro.usuarios.add(usuario_atendido)
                    registro.save()
                return redirect('ver_registros_diarios')

            except Exception as e:
                forms.add_error('file', f"Error al procesar el archivo: {e}")
        else:
            forms.add_error('file', "El archivo proporcionado no es válido.")
    else:
        forms = CSVUploadForm()

    return render(request, 'cargar_csv.html', {'forms': forms})



def buscar_usuario(request):
    filtro = request.GET.get('filtro')
    valor = request.GET.get('valor')
    lista_nodos = iniciar_nodos()
    resultados = lista_nodos.buscar(filtro, valor)

    return render(request, 'Resultado_busqueda.html', {'resultados': resultados})








