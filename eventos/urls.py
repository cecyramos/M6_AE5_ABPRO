from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.ListarEventosView.as_view(), name='listar_eventos'),
    path('evento/<int:pk>/', views.DetalleEventoView.as_view(), name='detalle_evento'),
    path('crear/', views.CrearEventoView.as_view(), name='crear_evento'),
    path('evento/<int:pk>/editar/', views.EditarEventoView.as_view(), name='editar_evento'),
    path('evento/<int:pk>/eliminar/', views.EliminarEventoView.as_view(), name='eliminar_evento'),
    path('evento/<int:pk>/registrarse/', views.RegistrarseEventoView.as_view(), name='registrarse_evento'),
]