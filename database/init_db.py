"""
Script de inicialización de base de datos - Tier 3: Acceso a Datos
Este script puede usarse para inicializar datos de prueba
"""
import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from app.config.database import db
from app.models import Empresa, Servicio, Contrato

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya hay datos
        if Empresa.query.count() > 0:
            print("La base de datos ya contiene datos. No se inicializará.")
            return
        
        # Crear empresas de ejemplo
        empresa1 = Empresa(
            nombre="Tech Solutions S.A.",
            direccion="Av. Principal 123",
            telefono="0991234567",
            email="contacto@techsolutions.com"
        )
        
        empresa2 = Empresa(
            nombre="Comercial ABC Ltda.",
            direccion="Calle Comercio 456",
            telefono="0987654321",
            email="info@comercialabc.com"
        )
        
        db.session.add(empresa1)
        db.session.add(empresa2)
        db.session.commit()
        
        # Crear servicios de ejemplo
        servicio1 = Servicio(
            nombre="Limpieza General",
            descripcion="Limpieza completa de oficinas y espacios comunes",
            precio_base=150.00,
            duracion_horas=4.0
        )
        
        servicio2 = Servicio(
            nombre="Limpieza Profunda",
            descripcion="Limpieza profunda con productos especializados",
            precio_base=300.00,
            duracion_horas=8.0
        )
        
        servicio3 = Servicio(
            nombre="Limpieza de Alfombras",
            descripcion="Limpieza y desinfección de alfombras",
            precio_base=200.00,
            duracion_horas=3.0
        )
        
        db.session.add(servicio1)
        db.session.add(servicio2)
        db.session.add(servicio3)
        db.session.commit()
        
        # Crear contratos de ejemplo
        from datetime import date, timedelta
        
        contrato1 = Contrato(
            empresa_id=empresa1.id,
            servicio_id=servicio1.id,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            estado="activo",
            precio_final=150.00
        )
        
        contrato2 = Contrato(
            empresa_id=empresa2.id,
            servicio_id=servicio2.id,
            fecha_inicio=date.today(),
            fecha_fin=None,
            estado="activo",
            precio_final=300.00
        )
        
        db.session.add(contrato1)
        db.session.add(contrato2)
        db.session.commit()
        
        print("Base de datos inicializada correctamente con datos de ejemplo.")
        print(f"- {Empresa.query.count()} empresas creadas")
        print(f"- {Servicio.query.count()} servicios creados")
        print(f"- {Contrato.query.count()} contratos creados")

if __name__ == '__main__':
    init_database()


