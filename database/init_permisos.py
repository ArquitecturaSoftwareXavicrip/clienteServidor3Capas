"""
Script para inicializar datos de ejemplo para el módulo de Permisos
"""
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio backend al path para poder importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from app.config.database import db
from app.models.permiso import Permiso

def init_permisos():
    """Inicializa la base de datos con datos de ejemplo de permisos"""
    app = create_app()
    
    with app.app_context():
        print("Creando tablas de la base de datos...")
        db.create_all()
        
        # Verificar si ya existen permisos
        if Permiso.query.count() > 0:
            print(f"Ya existen {Permiso.query.count()} permisos en la base de datos.")
            respuesta = input("¿Desea eliminarlos y crear nuevos datos de ejemplo? (s/n): ")
            if respuesta.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Eliminar permisos existentes
            Permiso.query.delete()
            db.session.commit()
            print("Permisos existentes eliminados.")
        
        # Crear fecha base (hoy)
        hoy = datetime.now().date()
        
        # Datos de ejemplo
        permisos_ejemplo = [
            {
                'empleado': 'Juan Pérez',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy + timedelta(days=7),
                'fecha_fin': hoy + timedelta(days=14),
                'dias_solicitados': 7,
                'estado': 'pendiente',
                'observaciones': 'Vacaciones de verano planificadas'
            },
            {
                'empleado': 'María García',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy + timedelta(days=30),
                'fecha_fin': hoy + timedelta(days=44),
                'dias_solicitados': 14,
                'estado': 'pendiente',
                'observaciones': 'Viaje familiar'
            },
            {
                'empleado': 'Carlos Rodríguez',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy - timedelta(days=10),
                'fecha_fin': hoy - timedelta(days=5),
                'dias_solicitados': 5,
                'estado': 'aprobado',
                'observaciones': 'Aprobado por gerencia'
            },
            {
                'empleado': 'Ana Martínez',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy + timedelta(days=60),
                'fecha_fin': hoy + timedelta(days=74),
                'dias_solicitados': 14,
                'estado': 'aprobado',
                'observaciones': 'Vacaciones de fin de año - aprobadas con anticipación'
            },
            {
                'empleado': 'Luis Fernández',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy - timedelta(days=30),
                'fecha_fin': hoy - timedelta(days=23),
                'dias_solicitados': 7,
                'estado': 'rechazado',
                'observaciones': 'No hay cobertura disponible en el período solicitado'
            },
            {
                'empleado': 'Carmen López',
                'tipo': 'Vacaciones',
                'fecha_inicio': hoy + timedelta(days=15),
                'fecha_fin': hoy + timedelta(days=19),
                'dias_solicitados': 4,
                'estado': 'pendiente',
                'observaciones': 'Fin de semana largo'
            },
        ]
        
        print("\nCreando permisos de ejemplo...")
        for permiso_data in permisos_ejemplo:
            permiso = Permiso(**permiso_data)
            db.session.add(permiso)
            print(f"  ✓ Creado: {permiso.empleado} - {permiso.dias_solicitados} días ({permiso.estado})")
        
        db.session.commit()
        
        print(f"\n✅ ¡Base de datos inicializada correctamente!")
        print(f"   Se crearon {len(permisos_ejemplo)} permisos de ejemplo.")
        print("\n📊 Resumen:")
        print(f"   - Pendientes: {Permiso.query.filter_by(estado='pendiente').count()}")
        print(f"   - Aprobados: {Permiso.query.filter_by(estado='aprobado').count()}")
        print(f"   - Rechazados: {Permiso.query.filter_by(estado='rechazado').count()}")
        print(f"\n🚀 Puedes acceder a la aplicación en: http://localhost:3001")
        print(f"   Y navegar al módulo de Permisos para ver los datos.\n")

if __name__ == '__main__':
    init_permisos()

