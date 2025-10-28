# 💈 Barbería Elite - Sistema de Gestión

Bienvenidos a **Barbería Elite**, un sistema web desarrollado con **Django** para la administración integral de una barbería.  
Permite a los clientes reservar citas en línea, a los barberos gestionar sus horarios y a los administradores controlar servicios, usuarios y disponibilidad desde un panel centralizado.

---

## 🌐 Descripción

**Barbería Elite** optimiza el proceso de agendamiento y gestión de servicios en barberías mediante una plataforma web dinámica con tres roles principales:

- **Cliente:** puede registrarse, iniciar sesión y reservar citas en tiempo real.  
- **Barbero:** administra su disponibilidad y confirma citas.  
- **Administrador:** controla usuarios, servicios, horarios y precios desde un panel de control.

---

### 🔧 Características principales

- Registro y autenticación de usuarios con distintos roles  
- Gestión de servicios y precios  
- Disponibilidad dinámica por barbero  
- Sistema de reservas en tiempo real  
- Envío automático de correos electrónicos al confirmar citas  
- Panel administrativo completo  
- Seguridad integrada mediante el sistema de autenticación de Django  

---

## 👥 Colaboradores

- **Diego Roa** – [@RoaStack](https://github.com/RoaStack)  
- **Gustavo Muñoz** – [@HTTPResponseG](https://github.com/HTTPResponseG)

Durante este proyecto se aplicaron metodologías colaborativas con **Git** y **GitHub**, incluyendo:

- Creación de ramas individuales por desarrollador  
- Uso de *Pull Requests (PR)* para revisión y aprobación de código  
- Integración controlada mediante *merge* a la rama principal (`main`)  
- Resolución de conflictos y comunicación constante en equipo  

---

## 📁 Estructura del proyecto
```
barberia/
├── core/                  # App principal (inicio, vistas generales)
├── usuarios/              # Gestión de usuarios, roles y autenticación
├── reservas/              # Lógica de reservas y disponibilidad
├── servicios/             # Modelos y vistas de servicios ofrecidos
├── templates/             # Plantillas HTML (base y secciones)
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── media/                 # Archivos subidos por usuarios
├── barberia/              # Configuración principal del proyecto Django
│   ├── settings.py        # Configuración general (BD, seguridad, correo)
│   ├── urls.py            # Enrutamiento global
│   └── wsgi.py            # Configuración para despliegue
├── manage.py              # Comando principal de Django
└── README.md              # Documentación del proyecto
```
---
## ⚙️ Instalación y ejecución local
1️⃣ Clonar el repositorio

git clone https://github.com/tuusuario/software-barberia.git
cd software-barberia


2️⃣ Crear y activar entorno virtual

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


3️⃣ Instalar dependencias

pip install -r requirements.txt


4️⃣ Configurar variables de entorno (.env)

SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=tu_correo@empresa.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_app


5️⃣ Aplicar migraciones

python manage.py migrate


6️⃣ Crear un superusuario

python manage.py createsuperuser


7️⃣ Ejecutar el servidor

python manage.py runserver

Luego accede a 👉 http://127.0.0.1:8000/

---
## 🔒 Seguridad

El sistema incluye múltiples medidas de seguridad integradas:

Contraseñas cifradas con hash seguro

Protección contra CSRF, XSS y SQL Injection

Sesiones seguras y validación de permisos

Encriptación de información sensible

Validación y saneamiento de formularios

---
## ✉️ Envío de correos electrónicos

El sistema utiliza SMTP configurado en settings.py para enviar notificaciones automáticas de reservas y confirmaciones.
Solo debes configurar tus credenciales en el archivo .env.

---
## 🖼️ Capturas de pantalla
---
## 🧰 Tecnologías utilizadas

Python 3.12+

Django 5

HTML5 / CSS3 / Bootstrap 5

SQLite3

Render (para despliegue en la nube)

---
## 📜 Licencia

MIT License

Copyright (c) 2025
Gustavo Muñoz y Diego Roa
