from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
from .models import Usuario,UsuarioAtendido,RegistroHoy
from .forms import UsuarioForm ,CSVUploadForm
from datetime import date,datetime
from .Nodos import Lista_nodos
import csv


def iniciar_nodos():
    usuarios = Usuario.objects.all() #obtenemos a todos los usuarios registrados
    lista_nodos = Lista_nodos() # inicializamos los nodos
    for usuario in usuarios: # iteramos la lista de todos los usuarios obtenida anteriormente
        lista_nodos.insertar_final_nodo(usuario)   # guardamos cada usuario en un nodo
    return lista_nodos  # retornamos todos los nodos




def index(request):
        lista_nodos=iniciar_nodos()  # llamos a la funcion iniciar_nodos la cual nos devuelve una lista de todos los nodos
        criterio = request.GET.get('criterio', 'nombre')
        ticket_actual = lista_nodos.obtener_y_eliminar_primero() # obtenemos el primer nodo para poder controlar el FIFO
        # Obtener la lista de datos sin alterar los nodos en la estructura
        lista_nodos_datos = lista_nodos.imprimir() # con esto obtenemos todos los nodos para poder enviarlo como contexto al HTML donde se van a presentar
        # Ordenar la lista extraída con Merge Sort basado en el criterio
        lista_nodos_datos = merge_sort(lista_nodos_datos, criterio)

        return render(request, 'Home.html',  {'lista_nodos_datos': lista_nodos_datos, 'ticket_actual': ticket_actual, 'criterio': criterio}) # haces la solicitud http , Renderizamos un template y enviamos los datos como contexto para poder visualizarlos en el HTML


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
        if criterio == 'nombre':
            if getattr(left[0], criterio).upper() <= getattr(right[0], criterio).upper():
               sorted_list.append(left.pop(0))
            else:
               sorted_list.append(right.pop(0))
        elif getattr(left[0], criterio) <= getattr(right[0], criterio):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))

    # Agregar elementos restantes
    sorted_list.extend(left if left else right)
    return sorted_list



def guardar_usuario(request): # resive como parametro una solicitud http
        if request.method == 'POST': # verificamos que el metodo de la solicitud se 'post' para seguir con el flujo en caso de no ser se presenta el formulario
            form = UsuarioForm(request.POST) #creamos una instancia del formulario y estamos pasando los datos del usuario
            if form.is_valid(): # si el formulario es valido
                form.save()  # guardamos la instancia del usuario
                return redirect('index') # redirigimos al index
        else:
            form = UsuarioForm() # presentamos el formulario
        return render(request, 'Registro.html', {'form': form}) # renderizamos el template y enviamos el formulario como contexto para presentarlo en el html


def eliminar_usuario(request,pk):  # recibe un solicitud http y un pk (clave primaria) o id
    usuario = get_object_or_404(Usuario,pk=pk) # buscamos el objeto en la clase usuario de acuerdo a su pk (clave primaria) si el objeto no existe django enviara un error 404
    usuario.delete() # eliminamos al usuario de la base de datos
    return redirect('index') # nos redirigimos al index una vez acabado el proceso


def atender_usuario(request):
    # Obtener el primer ticket no atendido (FIFO)
    usuario = Usuario.objects.all().first() # dentro de la tabla de la base de datos (Usuario) obtenemos al primer elemento

    if usuario: # si el usuario existe
        # Crear un registro en la tabla `UsuarioAtendido` con los mismos atributos que el usuario que hemos obtendido previamente
        UsuarioAtendido.objects.create(
            nombre=usuario.nombre,
            cedula=usuario.cedula,
            edad=usuario.edad,
            fecha_registro=usuario.fecha_registro,
        )
        usuario.delete()  # eliminamos al usuario y con esto controlaremos la data que los nodos obtengan
    return redirect('index') # redirigimos al index


def ver_registros_diarios(request):
        # Asegurarse de que haya un registro para hoy si se crea un objeto UsuarioAtendido hoy
        hoy = date.today()
        registro_hoy, created = RegistroHoy.objects.get_or_create(fecha=hoy)

        # Obtener todos los registros diarios, ordenados por fecha en orden descendente
        registros = RegistroHoy.objects.all().order_by('-fecha')
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=hoy)

        return render(request, 'Registros.html', {'registros': registros,'usuarios_atendidos': usuarios_atendidos})


def detalle_registro_diario(request,pk): # recibimos una solicitud http y un pk ( clave primaria ) o id para Obtener el registro diario específico
    registro = get_object_or_404(RegistroHoy,pk=pk) # obtenemos el registro de acuerdo a su pk ( clave primaria ) si el objeto no existe django nos devuelve un error 404
    usuarios_atendidos = UsuarioAtendido.objects.all() # obtenemos a todos los usuarios_atendidos para pasarlos como conexto y poder presentralos en el html
    return render(request, 'detalle_registro_diario.html', {'registro': registro, 'usuarios_atendidos': usuarios_atendidos}) # pasamos nuestra template(HTML) y nuestros contextos


def descargas(request,pk):
    if request.method == 'GET': # verificamos que la solicitud sea de tipo GET si lo es seguimos con el flujo
        # Obtener el registro del día
        registro = get_object_or_404(RegistroHoy,pk=pk) # obtenemos el objeto de acuerdo a su pk ( clave primaria ) o ID si no es encontrado django nos retornara un error 404

        # Filtrar usuarios atendidos por la fecha del registro
        usuarios_atendidos = UsuarioAtendido.objects.filter(fecha_registro=registro.fecha)

        # Configurar la respuesta como un archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="registro_{registro.fecha}.csv"' # sera el nombre con el que lo descargemos

        # Crear el escritor CSV y definir las columnas
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Cédula', 'Edad', 'Fecha de Registro']) # definimos las columnas dentro del archivo de acuerdo anuestros atributos dentro de la clase UsuariosAtendidos

        # Escribir la información de cada usuario en el CSV
        for usuario in usuarios_atendidos:
            writer.writerow([usuario.nombre, usuario.cedula, usuario.edad, usuario.fecha_registro]) # escribimos en cada fila la informacion o atributos de cada usuario que estan dentro del registro

        return response # devolvemos la respuesta como archivo CSV



def cargar_datos(request):
    if request.method == 'POST':  # verificamos que la solicitud http sea "POST" y seguimos con el flujo si no es el caso presentamos el Formulario de Cargar archivo
        forms = CSVUploadForm(request.POST, request.FILES) # esta línea crea el formulario y lo inicializa con los datos y archivos enviados por el usuario.
        if forms.is_valid():  # verifica que el formulario sea valido es decir que contenga algun archivo
            archivo_csv = request.FILES['file'] #Accede al archivo subido a través de request.FILES
            try:
                decoded_file = archivo_csv.read().decode('utf-8').splitlines() # archivo_csv.read() lee el contenido completo del archivo; decode('utf-8') convierte el contenido leído (en bytes) a una cadena de texto en formato UTF-8 ; splitlines() divide el contenido en una lista de líneas de texto, donde cada elemento de la lista es una línea del archivo.
                reader = csv.reader(decoded_file) # contiene todas las líneas del archivo CSV en formato de lista.
                # Saltar la cabecera si existe
                header = next(reader)
                # Procesar cada fila
                for fila in reader: #Inicia un bucle que itera sobre cada fila en reader, donde cada fila es una lista que representa una línea del CSV dividida en columnas.
                    nombre, cedula, edad, fecha_registro = fila # atributos de cada usuario
                    # Convertimos la fecha del registro en formato DateField
                    fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()
                    # Creamos y guardamos cada UsuarioAtendido
                    usuario_atendido = UsuarioAtendido.objects.create(
                        nombre=nombre,
                        cedula='0' + cedula,
                        edad=int(edad),
                        fecha_registro=fecha_registro
                    )
                    # Agregar el usuario al registro diario correspondiente
                    registro, creado = RegistroHoy.objects.get_or_create(fecha=fecha_registro)
                    registro.usuarios.add(usuario_atendido)
                    registro.save()
                return redirect('ver_registros_diarios') # retornamos a la pagina donde se encuentran todos los registros

            except Exception as e:
                # Si ocurre un error, puedes agregar un mensaje o manejarlo de otra forma
                forms.add_error('file', f"Error al procesar el archivo: {e}") #Agrega un mensaje de error al formulario forms bajo el campo file, explicando el problema encontrado.
        else:
            forms.add_error('file', "El archivo proporcionado no es válido.") # Agrega un mensaje de error al formulario forms bajo el campo file, explicando el problema encontrado.
    else:
        forms = CSVUploadForm() # creamos una instacia del formulario para subir el archivo , esto se ejecuta al ir hacia la pagina de carga siempre

    return render(request, 'cargar_csv.html', {'forms': forms}) # renderizamos el template(HTML) y enviamos nuestro contexto para mostralo dentro del HTML



def buscar_usuario(request):
    filtro = request.GET.get('filtro')  # Obtiene el campo de filtro del formulario
    valor = request.GET.get('valor')    # Obtiene el valor a buscar
    lista_nodos = iniciar_nodos()       # llamos a la funcion que contiene la lista de nodos
    resultados = lista_nodos.buscar(filtro, valor) # Buscamos al objeto dentro de los nodos deacuerdo a un filtro y valor

    return render(request, 'Resultado_busqueda.html', {'resultados': resultados}) # renderizamos el template(HTML) y nuestro contexto para poder visualizarlo en el HTML








