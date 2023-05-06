from django.shortcuts import render, redirect
from .forms import FormularioCargarViaje, FormularioVerViaje, FormularioMisViajes
from GestionViajes.models import Viaje 
from GestionViajes.models import PasajerosViaje
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect



# Create your views here.

def cargarViaje(request):
    formulario_cargar_viaje = FormularioCargarViaje()
    if request.user.is_authenticated:
        if request.method == 'POST':
            formulario_cargar_viaje = FormularioCargarViaje(data=request.POST)
            if formulario_cargar_viaje.is_valid():
                fecha = formulario_cargar_viaje.cleaned_data['fecha']
                observaciones = formulario_cargar_viaje.cleaned_data['observaciones']
                plazas_disponibles = formulario_cargar_viaje.cleaned_data['plazas_disponibles']
                origen_calle = formulario_cargar_viaje.cleaned_data['origen_calle']
                origen_altura = formulario_cargar_viaje.cleaned_data['origen_altura']
                destino_calle = formulario_cargar_viaje.cleaned_data['destino_calle']
                destino_altura = formulario_cargar_viaje.cleaned_data['destino_altura']
                conductor_id = request.user.id
                
                origen = f"{origen_calle} {origen_altura}"
                destino = f"{destino_calle} {destino_altura}"
                
                viaje = Viaje(
                    origen=origen,
                    destino=destino,
                    fecha=fecha,
                    observaciones=observaciones,
                    plazas_disponibles=plazas_disponibles,
                    conductor_id=conductor_id,
                )
                viaje.save()
                
                return redirect('/GestionViajes/cargarViaje/?valido')
    else:
        return redirect('/login')
    
    return render(request, 'GestionViajes/cargarViaje.html', {'formulario': formulario_cargar_viaje})


def verViaje(request):
    if request.user.is_authenticated:
        fecha_actual = datetime.now()
        formulario_verViaje = FormularioVerViaje()
        viajes = Viaje.objects.filter(fecha__gte = fecha_actual).order_by('fecha')

        viajesPasajero = PasajerosViaje.objects.filter(user_id=request.user.id)
        viajesPasajero_list = []
        for viaje in viajesPasajero:
            viajesPasajero_list.append(viaje.viaje_id)

        if request.method=='POST':
            viaje_id = request.POST.get('viaje_id')
            user_id = request.POST.get('user_id')
            viajeSolicitado = Viaje.objects.get(id = viaje_id)
            conductor_id = viajeSolicitado.conductor_id
            conductor = User.objects.get(id = conductor_id)

            # Registro en la tabla de pasajeros al nuevo pasajero
            nuevoPasajero = PasajerosViaje(viaje_id=viaje_id, user_id=user_id)
            nuevoPasajero.save()

           

            # Envío mail al conductor con el nuevo pasajero
            email = conductor.email
            send_mail('Tenés un nuevo pasajero!', 
                    f'{request.user.username} quiere viajar con vos! contactate con el/ella para coordinar Mail: {request.user.email}', 
                    'ushgotdf@gmail.com', 
                    [email], 
                    fail_silently=False)

        viajesPasajero = PasajerosViaje.objects.filter(user_id=request.user.id)
        viajesPasajero_list = []
        for viaje in viajesPasajero:
            viajesPasajero_list.append(viaje.viaje_id)

        origen = request.GET.get('origen')
        destino = request.GET.get('destino')
        fecha = request.GET.get('fecha')

        if origen != '' and origen is not None:
            if destino != '' and destino is not None:
                viajes = viajes.filter(origen=origen, destino=destino)
                if fecha != '' and fecha is not None:
                    viajes = viajes.filter(fecha=fecha).order_by('-fecha')

        # Calcular la cantidad de plazas disponibles en cada viaje
        for viaje in viajes:
            pasajeros = PasajerosViaje.objects.filter(viaje_id=viaje.id)
            

    else:
        return redirect("/login")

    context = {
        'viajes': viajes, 
        'formulario': formulario_verViaje,
        'viajesPasajero': viajesPasajero_list
        }
    return render(request, "GestionViajes/verViaje.html", context)


def misViajes(request):
    print("Llegó a la vista misViajes")

    if request.user.is_authenticated:
        fecha_actual = datetime.now()
        formulario_verViaje = FormularioVerViaje()
        viajes = Viaje.objects.filter(fecha__gte=fecha_actual).order_by('fecha')
        user_id = request.user.id
        viajesUser = Viaje.objects.filter(conductor_id=user_id).order_by('fecha')

        if request.method == 'POST':
            viaje_id = request.POST.get('viaje_id')
            viaje = get_object_or_404(Viaje, id=viaje_id)
            viaje.delete()
            return redirect('misViajes')

        for viaje in viajesUser:
            pasajeros = PasajerosViaje.objects.filter(viaje_id=viaje.id)
            plazas_ocupadas = pasajeros.count()
    else:
        return redirect("/login")

    context = {
        'viajes': viajesUser
    }
    return render(request, "GestionViajes/misViajes.html", context)
