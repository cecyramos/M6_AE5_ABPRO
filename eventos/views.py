from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Evento
from .forms import EventoForm, RegistroForm


# Vista de Registro
class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'registro.html', {'form': form})
    
    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, '¡Registro exitoso! Inicia sesión con tus credenciales.')
            return redirect('login')
        return render(request, 'registro.html', {'form': form})


# Vista de Login
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'¡Bienvenido {usuario.username}!')
            return redirect('listar_eventos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'login.html')


# Vista de Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('login')


# Vista para listar eventos (pública pero filtrada)
class ListarEventosView(ListView):
    model = Evento
    template_name = 'listar_eventos.html'
    context_object_name = 'eventos'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Mostrar eventos públicos + eventos privados donde es asistente/organizador
            from django.db.models import Q
            return Evento.objects.filter(
                Q(privado=False) | 
                Q(organizador=self.request.user) | 
                Q(asistentes=self.request.user)
            ).distinct()
        else:
            # Solo mostrar eventos públicos a usuarios no autenticados
            return Evento.objects.filter(privado=False)


# Vista para ver detalles de un evento
class DetalleEventoView(DetailView):
    model = Evento
    template_name = 'detalle_evento.html'
    context_object_name = 'evento'
    
    def get(self, request, *args, **kwargs):
        evento = self.get_object()
        
        # Validar acceso a eventos privados
        if evento.privado:
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para ver este evento.')
                return redirect('login')
            if request.user != evento.organizador and request.user not in evento.asistentes.all():
                messages.error(request, 'No tienes permiso para ver este evento.')
                return redirect('listar_eventos')
        
        return super().get(request, *args, **kwargs)


# Vista para crear evento (LoginRequiredMixin = solo autenticados)
class CrearEventoView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'crear_evento.html'
    success_url = reverse_lazy('listar_eventos')
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que tenga el permiso 'add_evento'
        if not request.user.has_perm('eventos.add_evento'):
            messages.error(request, 'No tienes permiso para crear eventos.')
            return redirect('listar_eventos')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.organizador = self.request.user
        messages.success(self.request, 'Evento creado exitosamente.')
        return super().form_valid(form)


# Vista para editar evento (solo organizador o admin)
class EditarEventoView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'editar_evento.html'
    success_url = reverse_lazy('listar_eventos')
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        evento = self.get_object()
        # Solo organizador del evento o superuser
        if evento.organizador != request.user and not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para editar este evento.')
            return redirect('listar_eventos')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Evento.objects.all()
        return Evento.objects.filter(organizador=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Evento actualizado exitosamente.')
        return super().form_valid(form)


# Vista para eliminar evento (solo admin/superuser)
class EliminarEventoView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'confirmar_eliminar.html'
    success_url = reverse_lazy('listar_eventos')
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        # Solo usuarios con permiso 'delete_evento' pueden ver esta vista
        if not request.user.has_perm('eventos.delete_evento'):
            messages.error(request, 'Solo administradores pueden eliminar eventos.')
            return redirect('listar_eventos')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Evento.objects.all()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Evento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vista para registrarse en un evento
class RegistrarseEventoView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        evento = get_object_or_404(Evento, pk=pk)
        
        if evento.privado and request.user != evento.organizador:
            messages.error(request, 'No puedes registrarte en eventos privados.')
            return redirect('listar_eventos')
        
        if request.user in evento.asistentes.all():
            evento.asistentes.remove(request.user)
            messages.info(request, 'Te has desregistrado del evento.')
        else:
            evento.asistentes.add(request.user)
            messages.success(request, '¡Te has registrado en el evento!')
        
        return redirect('detalle_evento', pk=evento.pk)