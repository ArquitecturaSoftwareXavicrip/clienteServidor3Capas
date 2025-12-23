"""
Script de inicialización completo para Docker
Carga todos los datos de ejemplo: empresas, servicios, contratos, permisos y empleados
"""
from datetime import datetime, timedelta, date
from app import create_app
from app.config.database import db
from app.models import Empresa, Servicio, Contrato, Permiso, Empleado

def init_all():
    """Inicializa todas las tablas con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        print("Creando tablas de la base de datos...")
        db.create_all()
        print("✓ Tablas creadas")
        print("")
        
        # ========== EMPRESAS ==========
        print("Cargando empresas...")
        if Empresa.query.count() == 0:
            empresas_data = [
                Empresa(nombre="Tech Solutions S.A.", direccion="Av. Principal 123", 
                       telefono="0991234567", email="contacto@techsolutions.com"),
                Empresa(nombre="Comercial ABC Ltda.", direccion="Calle Comercio 456",
                       telefono="0987654321", email="info@comercialabc.com")
            ]
            for e in empresas_data:
                db.session.add(e)
            db.session.commit()
            print(f"  ✓ {len(empresas_data)} empresas creadas")
        else:
            print(f"  ⚠ Ya existen {Empresa.query.count()} empresas")
        
        # ========== SERVICIOS ==========
        print("Cargando servicios...")
        if Servicio.query.count() == 0:
            servicios_data = [
                Servicio(nombre="Limpieza General", descripcion="Limpieza completa de oficinas",
                        precio_base=150.00, duracion_horas=4.0),
                Servicio(nombre="Limpieza Profunda", descripcion="Limpieza profunda con productos especializados",
                        precio_base=300.00, duracion_horas=8.0),
                Servicio(nombre="Limpieza de Alfombras", descripcion="Limpieza y desinfección de alfombras",
                        precio_base=200.00, duracion_horas=3.0)
            ]
            for s in servicios_data:
                db.session.add(s)
            db.session.commit()
            print(f"  ✓ {len(servicios_data)} servicios creados")
        else:
            print(f"  ⚠ Ya existen {Servicio.query.count()} servicios")
        
        # ========== CONTRATOS ==========
        print("Cargando contratos...")
        if Contrato.query.count() == 0:
            contratos_data = [
                Contrato(empresa_id=1, servicio_id=1, fecha_inicio=date.today(),
                        fecha_fin=date.today() + timedelta(days=30), estado="activo", precio_final=150.00),
                Contrato(empresa_id=2, servicio_id=2, fecha_inicio=date.today(),
                        fecha_fin=None, estado="activo", precio_final=300.00)
            ]
            for c in contratos_data:
                db.session.add(c)
            db.session.commit()
            print(f"  ✓ {len(contratos_data)} contratos creados")
        else:
            print(f"  ⚠ Ya existen {Contrato.query.count()} contratos")
        
        # ========== PERMISOS ==========
        print("Cargando permisos...")
        if Permiso.query.count() == 0:
            hoy = date.today()
            permisos_data = [
                Permiso(empleado="Juan Pérez", tipo="Vacaciones", fecha_inicio=hoy + timedelta(days=7),
                       fecha_fin=hoy + timedelta(days=14), dias_solicitados=7, estado="pendiente",
                       observaciones="Vacaciones de verano planificadas"),
                Permiso(empleado="María García", tipo="Vacaciones", fecha_inicio=hoy + timedelta(days=30),
                       fecha_fin=hoy + timedelta(days=44), dias_solicitados=14, estado="pendiente",
                       observaciones="Viaje familiar"),
                Permiso(empleado="Carlos Rodríguez", tipo="Vacaciones", fecha_inicio=hoy - timedelta(days=10),
                       fecha_fin=hoy - timedelta(days=5), dias_solicitados=5, estado="aprobado",
                       observaciones="Aprobado por gerencia"),
                Permiso(empleado="Ana Martínez", tipo="Vacaciones", fecha_inicio=hoy + timedelta(days=60),
                       fecha_fin=hoy + timedelta(days=74), dias_solicitados=14, estado="aprobado",
                       observaciones="Vacaciones de fin de año"),
                Permiso(empleado="Luis Fernández", tipo="Vacaciones", fecha_inicio=hoy - timedelta(days=30),
                       fecha_fin=hoy - timedelta(days=23), dias_solicitados=7, estado="rechazado",
                       observaciones="No hay cobertura disponible"),
                Permiso(empleado="Carmen López", tipo="Vacaciones", fecha_inicio=hoy + timedelta(days=15),
                       fecha_fin=hoy + timedelta(days=19), dias_solicitados=4, estado="pendiente",
                       observaciones="Fin de semana largo")
            ]
            for p in permisos_data:
                db.session.add(p)
            db.session.commit()
            print(f"  ✓ {len(permisos_data)} permisos creados")
        else:
            print(f"  ⚠ Ya existen {Permiso.query.count()} permisos")
        
        # ========== EMPLEADOS ==========
        print("Cargando empleados...")
        if Empleado.query.count() == 0:
            empleados_data = [
                Empleado(nombre="Juan", apellido="Pérez García", email="juan.perez@limpieza.com",
                        telefono="0991234567", cargo="Gerente General"),
                Empleado(nombre="María", apellido="González López", email="maria.gonzalez@limpieza.com",
                        telefono="0987654321", cargo="Supervisor de Limpieza"),
                Empleado(nombre="Carlos", apellido="Rodríguez Sánchez", email="carlos.rodriguez@limpieza.com",
                        telefono="0998765432", cargo="Operario de Limpieza"),
                Empleado(nombre="Ana", apellido="Martínez Torres", email="ana.martinez@limpieza.com",
                        telefono="0992345678", cargo="Operario de Limpieza"),
                Empleado(nombre="Luis", apellido="Fernández Ruiz", email="luis.fernandez@limpieza.com",
                        telefono="0993456789", cargo="Supervisor de Área"),
                Empleado(nombre="Carmen", apellido="López Díaz", email="carmen.lopez@limpieza.com",
                        telefono="0994567890", cargo="Coordinador Administrativo"),
                Empleado(nombre="Pedro", apellido="Sánchez Morales", email="pedro.sanchez@limpieza.com",
                        telefono="0995678901", cargo="Operario de Limpieza"),
                Empleado(nombre="Laura", apellido="Torres Vega", email="laura.torres@limpieza.com",
                        telefono="0996789012", cargo="Jefe de Recursos Humanos")
            ]
            for e in empleados_data:
                db.session.add(e)
            db.session.commit()
            print(f"  ✓ {len(empleados_data)} empleados creados")
        else:
            print(f"  ⚠ Ya existen {Empleado.query.count()} empleados")
        
        print("")
        print("=" * 50)
        print("✅ BASE DE DATOS INICIALIZADA COMPLETAMENTE")
        print("=" * 50)
        print(f"  - Empresas:  {Empresa.query.count()}")
        print(f"  - Servicios: {Servicio.query.count()}")
        print(f"  - Contratos: {Contrato.query.count()}")
        print(f"  - Permisos:  {Permiso.query.count()}")
        print(f"  - Empleados: {Empleado.query.count()}")
        print("")
        print("🚀 Aplicación lista en: http://localhost:3001")
        print("")

if __name__ == '__main__':
    init_all()

