#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "=== Iniciando proceso de build ==="

# Instalar dependencias
echo "1. Instalando dependencias..."
pip install -r requirements.txt

# Aplicar migraciones
echo "2. Aplicando migraciones..."
python manage.py migrate

# Crear superusuario (solo si las variables de entorno están configuradas)
echo "3. Verificando creación de superusuario..."
if [ -n "$SUPERUSER_PASSWORD" ]; then
    python create_superuser.py
else
    echo "⚠️ SUPERUSER_PASSWORD no configurada - omitiendo creación de superusuario"
fi

# Colectar archivos estáticos
echo "4. Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado exitosamente"