# create_superuser.py
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barberia.settings')

# Asegurarnos de que el directorio del proyecto está en el path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError

def create_superuser():
    User = get_user_model()
    
    # Obtener credenciales de variables de entorno
    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('SUPERUSER_PASSWORD')
    
    if not password:
        print("❌ ERROR: No se proporcionó SUPERUSER_PASSWORD en las variables de entorno")
        return False
    
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"⚠️ El superusuario '{username}' ya existe")
            return True
        
        # Crear el superusuario
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superusuario '{username}' creado exitosamente")
        return True
        
    except IntegrityError as e:
        print(f"❌ Error de integridad: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == '__main__':
    create_superuser()