# 🎉 Plataforma de Gestión de Eventos - Django

Una aplicación web completa de gestión de eventos en Django con autenticación, autorización y sistema de roles.

## **📋 Características**

- ✅ Sistema de autenticación (registro, login, logout)
- ✅ Autorización basada en roles (3 tipos de usuarios)
- ✅ Gestión de eventos (crear, editar, eliminar)
- ✅ Eventos públicos y privados
- ✅ Sistema de registro de asistentes
- ✅ Panel de administración personalizado
- ✅ Interfaz responsiva con Bootstrap 5

---

## **👥 Tipos de Usuarios y Permisos**

| Tipo | Crear | Editar | Eliminar | Ver | Registrarse |
|------|:---:|:---:|:---:|:---:|:---:|
| **Asistente** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Organizador** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Administrador** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## **🚀 Instalación y Configuración**

### **Paso 1: Crear el proyecto**

```bash
django-admin startproject proyecto_eventos
cd proyecto_eventos
```

### **Paso 2: Crear la app**

```bash
python manage.py startapp eventos
```

### **Paso 3: Crear estructura de carpetas**

```
eventos/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── setup_roles.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── registro.html
│   ├── listar_eventos.html
│   ├── detalle_evento.html
│   ├── crear_evento.html
│   ├── editar_evento.html
│   └── confirmar_eliminar.html
├── models.py
├── views.py
├── forms.py
├── urls.py
├── admin.py
└── apps.py
```

### **Paso 4: Copiar archivos**

Copia los archivos Python (models.py, views.py, forms.py, admin.py, urls.py) y HTML (templates) desde los artifacts proporcionados.

### **Paso 5: Ejecutar migraciones**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **Paso 6: Crear superuser**

```bash
python manage.py createsuperuser
# Ingresa usuario, email y contraseña
```

### **Paso 7: Crear grupos y permisos**

```bash
python manage.py setup_roles
```

**Salida esperada:**
```
✅ Grupo "Administradores" creado
✅ Grupo "Organizadores" creado
✅ Grupo "Asistentes" creado
✅ Configuración de roles completada
```

### **Paso 8: Ejecutar servidor**

```bash
python manage.py runserver
```

Accede a: `http://127.0.0.1:8000/`

---

## **📖 Uso de la Plataforma**

### **1. Registro de Usuario**

1. Ve a `/registro/`
2. Completa el formulario con:
   - Usuario
   - Email
   - Contraseña (x2)
3. Click en "Registrarse"

### **2. Iniciar Sesión**

1. Ve a `/login/`
2. Ingresa usuario y contraseña
3. Serás redirigido a la lista de eventos

### **3. Gestión de Eventos**

#### **Crear Evento** (solo si tienes permiso)
- Click en "+ Nuevo Evento"
- Completa título, descripción, fecha, ubicación, tipo
- Marca "Privado" si es privado (solo tú lo ves)
- Click "Crear Evento"

#### **Ver Detalles del Evento**
- Click en "Ver Detalles" en cualquier evento
- Ver información completa y lista de asistentes

#### **Editar Evento** (solo organizador o admin)
- Ve a detalles del evento
- Click en "Editar"
- Modifica los campos
- Click "Guardar Cambios"

#### **Eliminar Evento** (solo admin)
- Ve a detalles del evento
- Click en "Eliminar"
- Confirma la acción

#### **Registrarse en Evento**
- Ve a detalles del evento
- Click en "Registrarse"
- Aparecerá en lista de asistentes

---

## **🔐 Panel de Administración**

Accede a `/admin/` con tu superuser

### **Gestionar Usuarios**

1. Ve a **Authentication and Authorization** → **Users**
2. Selecciona un usuario
3. En la sección **Groups**, marca el grupo:
   - **Asistentes:** Solo ven eventos
   - **Organizadores:** Crean y editan eventos
   - **Administradores:** Control total
4. Click "Save"

### **Ver Permisos**

1. Ve a **Authentication and Authorization** → **Permissions**
2. Verás los 4 permisos por modelo:
   - `Can add evento`
   - `Can change evento`
   - `Can delete evento`
   - `Can view evento`

### **Ver Grupos**

1. Ve a **Authentication and Authorization** → **Groups**
2. Ver qué permisos tiene cada grupo

---

## **📁 Estructura del Proyecto**

```
proyecto_eventos/
├── proyecto_eventos/
│   ├── settings.py          # Configuración de Django
│   └── urls.py              # URLs principales
│
├── eventos/
│   ├── templates/           # Archivos HTML
│   ├── models.py            # Modelo Evento
│   ├── views.py             # Lógica de vistas
│   ├── forms.py             # Formularios
│   ├── urls.py              # URLs de la app
│   ├── admin.py             # Admin personalizado
│   └── apps.py
│
├── manage.py
├── README.md
├── requirements.txt
└── db.sqlite3               # Base de datos
```

---

## **🗄️ Modelo de Datos**

### **Modelo: Evento**

```python
- titulo: CharField(200)
- descripcion: TextField
- fecha: DateTimeField
- ubicacion: CharField(200)
- tipo: Conferencia | Concierto | Seminario
- privado: Boolean (default: False)
- organizador: ForeignKey(User)
- asistentes: ManyToManyField(User)
- creado_en: DateTimeField(auto_now_add=True)
```

---

## **📝 Ejemplos de Uso**

### **Crear evento como Organizador**

```bash
1. Login como usuario en grupo "Organizadores"
2. Click "+ Nuevo Evento"
3. Completa información
4. Deja "Privado" sin marcar → evento público
5. Otros usuarios lo verán automáticamente
```

### **Restricción de permisos**

```bash
# Usuario Asistente intenta crear evento:
→ Mensaje: "No tienes permiso para crear eventos."
→ Redirige a lista de eventos

# Usuario Organizador intenta eliminar:
→ Mensaje: "Solo administradores pueden eliminar eventos."
```

---

## **🔒 Seguridad Implementada**

- ✅ Contraseñas hasheadas con `set_password()`
- ✅ Token CSRF en todos los formularios
- ✅ Cookies seguras (HTTPOnly)
- ✅ Sesiones autenticadas
- ✅ Validación de permisos en cada vista
- ✅ Validación en formularios

---

## **⚙️ Configuración Importante**

### **settings.py**

```python
LOGIN_URL = 'login'                          # Ruta de login
LOGIN_REDIRECT_URL = 'listar_eventos'        # Después de login
LOGOUT_REDIRECT_URL = 'login'                # Después de logout

SESSION_COOKIE_HTTPONLY = True               # Cookies seguras
CSRF_COOKIE_HTTPONLY = True
```

---

## **🐛 Troubleshooting**

### **Eventos no visibles para otros usuarios**

Verifica que el evento esté marcado como **Público** (checkbox sin marcar).

---

## **📚 Recursos Útiles**

- [Documentación Django](https://docs.djangoproject.com/)
- [Django Auth](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions)
- [Bootstrap 5](https://getbootstrap.com/)

---

## **✅ Cumplimiento de Requisitos**

Esta plataforma cumple con todos los requisitos del bootcamp:

- ✅ Configuración del Modelo Auth
- ✅ Enrutamiento Login/Logout
- ✅ Gestión de Roles y Permisos
- ✅ Uso de Mixins (LoginRequiredMixin)
- ✅ Redirección de accesos no autorizados
- ✅ Manejo de errores y mensajes
- ✅ Migraciones ejecutadas
- ✅ Exploración de auth_permission
- ✅ Configuración de seguridad

---

## **📄 Licencia**

Este proyecto es de código abierto bajo la licencia MIT.

---

## **👨‍💻 Autor**

Cecilia Ramos Alcatruz
Desarrollado como ejercicio del Bootcamp de Python - Módulo 6

---

**¡A disfrutar de la plataforma! 🚀**