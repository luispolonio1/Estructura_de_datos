from django.shortcuts import render , get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Usuario,UsuarioAtendido,RegistroHoy
from .forms import UsuarioForm ,CSVUploadForm
from datetime import date,datetime
from .Nodos import Lista_nodos
import csv


def iniciar_nodos():
    usuarios = Usuario.objects.all()
    lista_nodos = Lista_nodos()
    for usuario in usuarios:
        lista_nodos.insertar_final_nodo(usuario)
    return lista_nodos



@csrf_exempt
def index(request):
        lista_nodos=iniciar_nodos()
        criterio = request.GET.get('criterio', 'nombre')
        ticket_actual = lista_nodos.obtener_y_eliminar_primero()

        # Obtener la lista de datos sin alterar los nodos en la estructura
        lista_nodos_datos = lista_nodos.imprimir()

        # Ordenar la lista extraída con Merge Sort basado en el criterio
        lista_nodos_datos = merge_sort(lista_nodos_datos, criterio)

        return render(request, 'Home.html',  {'lista_nodos_datos': lista_nodos_datos, 'ticket_actual': ticket_actual, 'criterio': criterio})


def merge_sort(data_list, criterio):
    """Aplica Merge Sort a la lista de datos extraídos de los nodos."""
    if len(data_list) <= 1:
        return data_list

    # Dividir la lista en mitades
    mid = len(data_list) // 2
    left_half = merge_sort(data_list[:mid], criterio)
    right_half = merge_sort(data_list[mid:], criterio)

    return merge(left_half, right_half, criterio)


def merge(left, right, criterio):
    """Fusión de dos listas ordenadas para el Merge Sort."""
    sorted_list = []
    while left and right:
        if getattr(left[0], criterio) <= getattr(right[0], criterio):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))

    # Agregar elementos restantes
    sorted_list.extend(left if left else right)
    return sorted_list





@csrf_exempt
def guardar_usuario(request):
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                usuario = form.save()  # Crear solo la instancia de Usuario
                return redirect('index')
        else:
            form = UsuarioForm()

        usuarios = Usuario.objects.all()
        return render(request, 'Registro.html', {'form': form, 'usuarios': usuarios})


def eliminar_usuario(request,pk):
    usuario = get_object_or_404(Usuario,pk=pk)
    usuario.delete()
    return redirect('index')


def atender_usuario(request):
    # Obtener el primer ticket no atendido (FIFO)
    usuario = Usuario.objects.all().first()

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

def agregar_usuario_al_registro_diario(usuario_atendido):
    hoy = date.today()
    registro, creado = RegistroHoy.objects.get_or_create(fecha=hoy)
    registro.usuarios.add(usuario_atendido)  # Agregar `UsuarioAtendido` al registro diario
    registro.save()

@csrf_exempt
def ver_registros_diarios(request):
        # Asegurarse de que haya un registro para hoy si se crea un objeto UsuarioAtendido hoy
        hoy = date.today()
        registro_hoy, created = RegistroHoy.objects.get_or_create(fecha=hoy)

        # Obtener todos los registros diarios, ordenados por fecha en orden descendente
        registros = RegistroHoy.objects.all().order_by('-fecha')
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=hoy)

        return render(request, 'Registros.html', {'registros': registros,'usuarios_atendidos': usuarios_atendidos})

@csrf_exempt
def detalle_registro_diario(request,pk):
    # Obtener el registro diario específico
    registro = get_object_or_404(RegistroHoy,pk=pk)
    usuarios_atendidos = UsuarioAtendido.objects.all()
    return render(request, 'detalle_registro_diario.html', {'registro': registro, 'usuarios_atendidos': usuarios_atendidos})

@csrf_exempt
def descargas(request,pk):
    if request.method == 'POST':
        # Obtener el registro del día
        registro = get_object_or_404(RegistroHoy,pk=pk)

        # Filtrar usuarios atendidos por la fecha del registro
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=registro.fecha)

        # Configurar la respuesta como un archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="registro_{registro.fecha}.csv"'

        # Crear el escritor CSV y definir las columnas
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Cédula', 'Edad', 'Fecha de Registro'])

        # Escribir la información de cada usuario en el CSV
        for usuario in usuarios_atendidos:
            writer.writerow([usuario.nombre, usuario.cedula, usuario.edad, usuario.fecha_registro])

        return response

@csrf_exempt
def cargar_datos(request):
    if request.method == 'POST':
        forms = CSVUploadForm(request.POST, request.FILES)
        if forms.is_valid():
            archivo_csv = request.FILES['file']
            decoded_file = archivo_csv.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Saltar la cabecera si existe
            header = next(reader)  # Esto asume que la primera fila es la cabecera

            # Procesar cada fila
            for row in reader:
                nombre, cedula, edad, fecha_registro = row  # Ajusta según tu CSV

                # Convertir la fecha del registro en formato DateField
                fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()  # Ajusta el formato según tu CSV

                # Crear y guardar cada UsuarioAtendido
                usuario_atendido = UsuarioAtendido.objects.create(
                    nombre=nombre,
                    cedula='0'+cedula,
                    edad=int(edad),
                    fecha_registro=fecha_registro
                )

                # Agregar el usuario al registro diario correspondiente
                registro, creado = RegistroHoy.objects.get_or_create(fecha=fecha_registro)
                registro.usuarios.add(usuario_atendido)  # Asegúrate de que RegistroHoy acepta instancias de UsuarioAtendido
                registro.save()

            return redirect('ver_registros_diarios')  # Redirige a una página de éxito o a la página principal
    else:
        forms = CSVUploadForm()

    return render(request, 'cargar_csv.html', {'forms': forms})


@csrf_exempt
def buscar_usuario(request):
    filtro = request.GET.get('filtro')  # Obtiene el campo de filtro del formulario
    valor = request.GET.get('valor')    # Obtiene el valor a buscar
    lista_nodos = iniciar_nodos()
    resultados = lista_nodos.buscar(filtro, valor)

    return render(request, 'Resultado_busqueda.html', {'resultados': resultados})








