from asyncio import Task
from .models import Profile, Bitacora, User
from .forms import ProfileForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout  
from django.contrib.auth.decorators import login_required

# from apps.tasks.models import Task

#-- Dashboard -----------------------------------------------------
def dashboard(request):
    return render(request, 'dashboard.html')


#-- login and login up ------------------------------------------------------------------

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            Bitacora.objects.create(
                user=None,
                movimiento=f"intento de inicio fallido para el usuario: {username}"
            )
            return render(request, 'sign-in.html',{
                'error_match': 'Usuario o contraseña son incorrectos'
            })
        else:
            Bitacora.objects.create(
                user=None,
                movimiento=f"intento de inicio exitosa para el usuario: {username}"
            )
            login(request, user) 
            return redirect('profile')

#cerrar sesion
def close(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "Usuario desconocido"

    Bitacora.objects.create(
        user=request.user,
        movimiento=f" El usuario: {username} cerro sesion "
    )
    logout(request)
    return redirect('signin')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()          # Guardad objeto en db
                login(request, user) # Guardar sesion

                Bitacora.objects.create(
                    user=user,
                    movimiento=f"Registro exitoso para el usuario: {user.username}"
                )
                return redirect('profile')  # Asegúrate de tener esta ruta nombrada
            except:
                Bitacora.objects.create(
                    user= None,
                    movimiento=f"Intento fallido para el usuario: {request.POST['username']}, Usuario ya existe"
                )
                return render(request, 'sign-up.html', {
                    'error_exist': "Usuario ya existe"
                })
        else:
            Bitacora.objects.create(
                user= None,
                movimiento=f"Intento de registro fallido para el usuario: {request.POST['username']}, Las contraseñas no coinciden"
            )
            return render(request, 'sign-up.html', {
                'error_exist': "Las contraseñas no coinciden"
            })
            
@login_required
#-- tablas pero se cambiara a bitacora -----------------------------------------------------
def tables(request):
    # Obtener query params
    profile_filter = request.GET.get('profile_filter', '')
    bitacora_filter = request.GET.get('bitacora_filter', '')

    # Filtrar profiles
    profile_list = Profile.objects.filter(estatus=True).order_by('name')
    if profile_filter:
        profile_list = profile_list.filter(
            Q(name__icontains=profile_filter) |
            Q(email__icontains=profile_filter)
        )

    # Paginación profiles
    page_number_profiles = request.GET.get('page_profiles')
    paginator_profiles = Paginator(profile_list, 5)
    profiles = paginator_profiles.get_page(page_number_profiles)

    # Filtrar bitacoras
    bitacoras_list = Bitacora.objects.all()
    if bitacora_filter:
        bitacoras_list = bitacoras_list.filter(
            Q(fecha__icontains=bitacora_filter)
        )
    
    # Paginación bitacoras
    page_number_bitacoras = request.GET.get('page_bitacoras')
    paginator_bitacoras = Paginator(bitacoras_list, 5)
    bitacoras = paginator_bitacoras.get_page(page_number_bitacoras)

    context = {
        'profiles': profiles,
        'bitacoras': bitacoras,
        'profile_filter': profile_filter,
        'bitacora_filter': bitacora_filter,
    }

    return render(request, 'tables.html', context)
    

#-- Profile ---------------------------------------------------------------
#
@login_required
def profile(request):
    # Verifica si el perfil ya existe
    existing_profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if existing_profile:
            messages.error(request, 'Ya tienes un perfil creado.')
            return redirect('profile')

        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()

            messages.success(request, f'Se guardó el perfil {new_profile.name}.')

            # Registrar en bitácora
            Bitacora.objects.create(
                movimiento=f"Se creó el perfil: {new_profile.name} con el teléfono {new_profile.phone}"
            )

            return redirect('profile')
    else:
        form = ProfileForm()

    context = {
        'profile': existing_profile,
        'form': form,
        'bitacora': Bitacora.objects.all(),
    }

    return render(request, 'profile.html', context)

def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            print(request.POST)
            updated_profile.save()
            
            # Bitácora
            Bitacora.objects.create(
                movimiento=f"Se actualizó el perfil: {updated_profile.name} con el phone {updated_profile.phone}"
            )
            return redirect('tables')  # 
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)

def edit_user(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            updated_profile.save()

            # Bitácora
            Bitacora.objects.create(
                movimiento=f"Se actualizó el perfil: {updated_profile.name} con el phone {updated_profile.phone}"
            )
            return redirect('profile')
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_user.html', context)

def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.estatus = False
    profile.save()
    
    # Bitácora antes de eliminar
    Bitacora.objects.create(
        movimiento=f"Se dio de baja el perfil: {profile.name} con el phone {profile.phone}"
    )

    return redirect('tables')

#Ezportacion de la tabla de registros

def export_data(request):
    # Obtener todos los perfiles ordenados por nombre
    profiles = Profile.objects.all().order_by('name')

    # Crear una instancia de libro de Excel
    wb = Workbook()           # Instancia del libro
    ws = wb.active            # Hoja activa por defecto (ya creada)

    # Agregar los encabezados a la hoja de Excel
    ws.append(['Nombre Usuario', 'Nombre', 'Teléfono', 'Correo'])

    # Agregar los datos de cada perfil como una nueva fila en el Excel
    for profile in profiles:
        ws.append([
            profile.username,  # Nombre de usuario
            profile.name,      # Nombre completo
            profile.phone,     # Teléfono
            profile.email      # Correo electrónico
        ])

    # Preparar la respuesta HTTP con el tipo de contenido para archivos Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Indicar al navegador que es un archivo adjunto con nombre 'profiles.xlsx'
    response['Content-Disposition'] = 'attachment; filename=profiles.xlsx'

    # Guardar el contenido del libro en la respuesta HTTP
    wb.save(response)

    # Devolver la respuesta, lo que hace que el navegador descargue el archivo
    return response

#exportacion de la bitacora 

def export_data_bitacora(request):
    # Consultamos todos los registros del modelo Bitacora
    registros = Bitacora.objects.all()

    # Creamos un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active  # Hoja activa por defecto

    # Agregamos los encabezados de columna al archivo Excel
    ws.append(['Id', 'Movimiento', 'Fecha'])

    # Recorremos cada registro del modelo y lo agregamos como una fila al Excel
    for registro in registros:
        ws.append([
            registro.id,
            registro.movimiento,
            registro.fecha.strftime('%Y-%m-%d %H:%M:%S') if registro.fecha else ''
        ])

    # Creamos una respuesta HTTP con tipo de contenido para Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=bitacora.xlsx'

    # Guardamos el libro Excel directamente en la respuesta HTTP
    wb.save(response)

    # Retornamos la respuesta, lo que provoca la descarga del archivo en el navegador
    return response


#----------------------TASK-----------------------
# @login_required
# def task_list(request):
#     profile = request.user.profile_set.first()
#     task_list = Task.objects.filter(profile=profile)
    
#     search_query = request.GET.get('filter', '')
#     if search_query:
#         task_list = task_list.filter(
#             Q(nombre__icontains=search_query)
#         )
    
#     #paginator
#     paginator = Paginator(task_list, 5)
#     pague_number = request.GET.get('page')
#     task = paginator.get_page(pague_number)
    
#     context = {
#         'task' : task
#     }
    
#     return render(request, 'tasks/tasks_list.html', context)
