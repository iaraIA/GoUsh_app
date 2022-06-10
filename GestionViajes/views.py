from django.shortcuts import render, redirect
from .forms import FormularioCargarViaje, FormularioVerViaje
from GestionViajes.models import Viaje 
from GestionViajes.models import PasajerosViaje
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.

def cargarViaje(request):
    formulario_cargarViaje = FormularioCargarViaje() 
    if request.user.is_authenticated:  
        if request.method=='POST':
            formulario_cargarViaje = FormularioCargarViaje(data=request.POST)
            if formulario_cargarViaje.is_valid():
                print(request.POST)
                origen = request.POST.get('origen')
                destino = request.POST.get('destino')
                fecha = request.POST.get('fecha')
                observaciones = request.POST.get('observaciones')
                conductor_id = request.POST.get('conductor_id')
                
                viaje = Viaje(origen=origen, destino=destino, fecha=fecha, observaciones=observaciones, conductor_id=conductor_id)
                viaje.save()
                
                return redirect("/GestionViajes/cargarViaje/?valido")
    else:
        return redirect("/login")

    return render(request, "GestionViajes/cargarViaje.html", {'formulario': formulario_cargarViaje})
    


def verViaje(request):
    if request.user.is_authenticated:
        fecha_actual = datetime.now()
        formulario_verViaje = FormularioVerViaje()
        viajes = Viaje.objects.filter(fecha__gte = fecha_actual).order_by('fecha')

        #viajesPasajero = PasajerosViaje.objects.filter(user_id=request.user.id)
        #viajesPasajero_list = []
        #for viaje in viajesPasajero:
        #    viajesPasajero_list.append(viaje.viaje_id)

        if request.method=='POST':
            viaje_id = request.POST.get('viaje_id')
            user_id = request.POST.get('user_id')
            viajeSolicitado = Viaje.objects.get(id = viaje_id)
            conductor_id = viajeSolicitado.conductor_id
            conductor = User.objects.get(id = conductor_id)

            #Registro en la tabla de pasajeros al nuevo pasajero
            nuevoPasajero = PasajerosViaje(viaje_id=viaje_id, user_id=user_id)
            nuevoPasajero.save()

            #Envio mail al conductor con el nuevo pasajero
            #email = conductor.email
            #send_mail('Tenés un nuevo pasajero!', 
            #        f'{request.user.username} quiere viajar con vos! contactate con el/ella para coordinar', 
            #        'flopezb@fi.uba.ar', 
            #        [email], 
            #        fail_silently=False)

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

    else:
        return redirect("/login")

    context = {
        'viajes': viajes, 
        'formulario': formulario_verViaje,
        'viajesPasajero': viajesPasajero_list
        }
    return render(request, "GestionViajes/verViaje.html", context)

def misViajes(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            viaje_id = request.POST.get('viaje_id')
            Viaje.objects.filter(id = viaje_id).delete()
            
        user_id = request.user.id
        viajesUser = Viaje.objects.filter(conductor_id = user_id).order_by('fecha')

    else:
        return redirect("/login")

    context = {
            'viajes': viajesUser
        }
    return render(request, "GestionViajes/misViajes.html", context)