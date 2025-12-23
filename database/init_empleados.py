"""
Script para inicializar datos de ejemplo para el módulo de Empleados
"""
import sys
import os

# Agregar el directorio backend al path para poder importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from app.config.database import db
from app.models.empleado import Empleado

def init_empleados():
    """Inicializa la base de datos con datos de ejemplo de empleados"""
    app = create_app()
    
    with app.app_context():
        print("Verificando tablas de la base de datos...")
        db.create_all()
        
        # Verificar si ya existen empleados
        if Empleado.query.count() > 0:
            print(f"Ya existen {Empleado.query.count()} empleados en la base de datos.")
            respuesta = input("¿Desea eliminarlos y crear nuevos datos de ejemplo? (s/n): ")
            if respuesta.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Eliminar empleados existentes
            Empleado.query.delete()
            db.session.commit()
            print("Empleados existentes eliminados.")
        
        # Datos de ejemplo
        empleados_ejemplo = [
            {
                'nombre': 'Juan',
                'apellido': 'Pérez García',
                'email': 'juan.perez@limpieza.com',
                'telefono': '0991234567',
                'cargo': 'Gerente General'
            },
            {
                'nombre': 'María',
                'apellido': 'González López',
                'email': 'maria.gonzalez@limpieza.com',
                'telefono': '0987654321',
                'cargo': 'Supervisor de Limpieza'
            },
            {
                'nombre': 'Carlos',
                'apellido': 'Rodríguez Sánchez',
                'email': 'carlos.rodriguez@limpieza.com',
                'telefono': '0998765432',
                'cargo': 'Operario de Limpieza'
            },
            {
                'nombre': 'Ana',
                'apellido': 'Martínez Torres',
                'email': 'ana.martinez@limpieza.com',
                'telefono': '0992345678',
                'cargo': 'Operario de Limpieza'
            },
            {
                'nombre': 'Luis',
                'apellido': 'Fernández Ruiz',
                'email': 'luis.fernandez@limpieza.com',
                'telefono': '0993456789',
                'cargo': 'Supervisor de Área'
            },
            {
                'nombre': 'Carmen',
                'apellido': 'López Díaz',
                'email': 'carmen.lopez@limpieza.com',
                'telefono': '0994567890',
                'cargo': 'Coordinador Administrativo'
            },
            {
                'nombre': 'Pedro',
                'apellido': 'Sánchez Morales',
                'email': 'pedro.sanchez@limpieza.com',
                'telefono': '0995678901',
                'cargo': 'Operario de Limpieza'
            },
            {
                'nombre': 'Laura',
                'apellido': 'Torres Vega',
                'email': 'laura.torres@limpieza.com',
                'telefono': '0996789012',
                'cargo': 'Jefe de Recursos Humanos'
            },
        ]
        
        print("\nCreando empleados de ejemplo...")
        for empleado_data in empleados_ejemplo:
            empleado = Empleado(**empleado_data)
            db.session.add(empleado)
            print(f"  ✓ Creado: {empleado.nombre} {empleado.apellido} - {empleado.cargo}")
        
        db.session.commit()
        
        print(f"\n✅ ¡Base de datos inicializada correctamente!")
        print(f"   Se crearon {len(empleados_ejemplo)} empleados de ejemplo.")
        print("\n📊 Resumen por cargo:")
        
        # Contar por cargo
        cargos = {}
        for empleado in Empleado.query.all():
            cargos[empleado.cargo] = cargos.get(empleado.cargo, 0) + 1
        
        for cargo, count in cargos.items():
            print(f"   - {cargo}: {count}")
        
        print(f"\n🚀 Puedes acceder a la aplicación en: http://localhost:3001")
        print(f"   Y navegar al módulo de Empleados para ver los datos.\n")

if __name__ == '__main__':
    init_empleados()

