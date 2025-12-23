"""
Repositorio de Factura - Tier 3: Acceso a Datos
Encapsula todas las operaciones de acceso a datos para Factura
"""
from app.config.database import db
from app.models.factura import Factura

class FacturaRepository:
    """Repositorio para operaciones CRUD de Factura"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las facturas"""
        return Factura.query.all()
    
    @staticmethod
    def get_by_id(factura_id):
        """Obtiene una factura por su ID"""
        return Factura.query.get(factura_id)
    
    @staticmethod
    def get_by_empresa(empresa_id):
        """Obtiene todas las facturas de una empresa"""
        return Factura.query.filter_by(empresa_id=empresa_id).all()
    
    @staticmethod
    def create(factura_data):
        """Crea una nueva factura"""
        factura = Factura(
            empresa_id=factura_data['empresa_id'],
            empleado_id=factura_data['empleado_id'],
            servicio_id=factura_data['servicio_id'],
            fecha_factura=factura_data.get('fecha_factura'),
            fecha_vencimiento=factura_data['fecha_vencimiento'],
            descripcion=factura_data['descripcion'],
            cantidad=factura_data['cantidad'],
            precio_unitario=factura_data['precio_unitario'],
            subtotal=factura_data['subtotal'],
            impuesto=factura_data.get('impuesto', 0.0),
            total=factura_data['total'],
            estado=factura_data.get('estado', 'pendiente')
        )
        db.session.add(factura)
        db.session.commit()
        return factura
    
    @staticmethod
    def update(factura_id, factura_data):
        """Actualiza una factura existente"""
        factura = FacturaRepository.get_by_id(factura_id)
        if not factura:
            return None
        
        factura.empresa_id = factura_data.get('empresa_id', factura.empresa_id)
        factura.empleado_id = factura_data.get('empleado_id', factura.empleado_id)
        factura.servicio_id = factura_data.get('servicio_id', factura.servicio_id)
        factura.fecha_factura = factura_data.get('fecha_factura', factura.fecha_factura)
        factura.fecha_vencimiento = factura_data.get('fecha_vencimiento', factura.fecha_vencimiento)
        factura.descripcion = factura_data.get('descripcion', factura.descripcion)
        factura.cantidad = factura_data.get('cantidad', factura.cantidad)
        factura.precio_unitario = factura_data.get('precio_unitario', factura.precio_unitario)
        factura.subtotal = factura_data.get('subtotal', factura.subtotal)
        factura.impuesto = factura_data.get('impuesto', factura.impuesto)
        factura.total = factura_data.get('total', factura.total)
        factura.estado = factura_data.get('estado', factura.estado)
        
        db.session.commit()
        return factura
    
    @staticmethod
    def delete(factura_id):
        """Elimina una factura"""
        factura = FacturaRepository.get_by_id(factura_id)
        if not factura:
            return False
        
        db.session.delete(factura)
        db.session.commit()
        return True
