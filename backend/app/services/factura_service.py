"""
Servicio de Factura - Tier 2: Lógica de Negocio
Contiene la lógica de negocio y validaciones para Factura
"""
from app.repositories.factura_repository import FacturaRepository
from app.repositories.empresa_repository import EmpresaRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.servicio_repository import ServicioRepository
from datetime import datetime

class FacturaService:
    """Servicio que contiene la lógica de negocio para Factura"""
    
    @staticmethod
    def get_all_facturas():
        """Obtiene todas las facturas"""
        return FacturaRepository.get_all()
    
    @staticmethod
    def get_factura_by_id(factura_id):
        """Obtiene una factura por ID"""
        return FacturaRepository.get_by_id(factura_id)
    
    @staticmethod
    def get_facturas_by_empresa(empresa_id):
        """Obtiene todas las facturas de una empresa"""
        return FacturaRepository.get_by_empresa(empresa_id)
    
    @staticmethod
    def create_factura(factura_data):
        """Crea una nueva factura con validaciones"""
        errors = []
        
        # Validar empresa
        if not factura_data.get('empresa_id'):
            errors.append('La empresa es requerida')
        else:
            empresa = EmpresaRepository.get_by_id(factura_data['empresa_id'])
            if not empresa:
                errors.append('La empresa especificada no existe')
        
        # Validar empleado
        if not factura_data.get('empleado_id'):
            errors.append('El empleado es requerido')
        else:
            empleado = EmpleadoRepository.get_by_id(factura_data['empleado_id'])
            if not empleado:
                errors.append('El empleado especificado no existe')
        
        # Validar servicio
        if not factura_data.get('servicio_id'):
            errors.append('El servicio es requerido')
        else:
            servicio = ServicioRepository.get_by_id(factura_data['servicio_id'])
            if not servicio:
                errors.append('El servicio especificado no existe')
        
        # Validar descripción
        if not factura_data.get('descripcion') or len(factura_data['descripcion'].strip()) == 0:
            errors.append('La descripción es requerida')
        
        # Validar cantidad
        if not factura_data.get('cantidad') or factura_data['cantidad'] <= 0:
            errors.append('La cantidad debe ser mayor a 0')
        
        # Validar precio unitario
        if not factura_data.get('precio_unitario') or factura_data['precio_unitario'] < 0:
            errors.append('El precio unitario debe ser válido')
        
        # Validar fechas
        if not factura_data.get('fecha_vencimiento'):
            errors.append('La fecha de vencimiento es requerida')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        # Calcular subtotal y total
        cantidad = factura_data['cantidad']
        precio_unitario = factura_data['precio_unitario']
        subtotal = cantidad * precio_unitario
        impuesto = factura_data.get('impuesto', 0.0)
        total = subtotal + impuesto
        
        factura_data['subtotal'] = subtotal
        factura_data['total'] = total
        factura_data['fecha_factura'] = factura_data.get('fecha_factura', datetime.now().date())
        
        return FacturaRepository.create(factura_data)
    
    @staticmethod
    def update_factura(factura_id, factura_data):
        """Actualiza una factura con validaciones"""
        factura = FacturaRepository.get_by_id(factura_id)
        if not factura:
            raise ValueError('Factura no encontrada')
        
        # Validar empresa si se proporciona
        if 'empresa_id' in factura_data and factura_data['empresa_id']:
            empresa = EmpresaRepository.get_by_id(factura_data['empresa_id'])
            if not empresa:
                raise ValueError('La empresa especificada no existe')
        
        # Validar empleado si se proporciona
        if 'empleado_id' in factura_data and factura_data['empleado_id']:
            empleado = EmpleadoRepository.get_by_id(factura_data['empleado_id'])
            if not empleado:
                raise ValueError('El empleado especificado no existe')
        
        # Validar servicio si se proporciona
        if 'servicio_id' in factura_data and factura_data['servicio_id']:
            servicio = ServicioRepository.get_by_id(factura_data['servicio_id'])
            if not servicio:
                raise ValueError('El servicio especificado no existe')
        
        # Recalcular totales si es necesario
        if 'cantidad' in factura_data or 'precio_unitario' in factura_data:
            cantidad = factura_data.get('cantidad', factura.cantidad)
            precio_unitario = factura_data.get('precio_unitario', factura.precio_unitario)
            subtotal = cantidad * precio_unitario
            impuesto = factura_data.get('impuesto', factura.impuesto)
            total = subtotal + impuesto
            
            factura_data['subtotal'] = subtotal
            factura_data['total'] = total
        
        return FacturaRepository.update(factura_id, factura_data)
    
    @staticmethod
    def delete_factura(factura_id):
        """Elimina una factura"""
        factura = FacturaRepository.get_by_id(factura_id)
        if not factura:
            raise ValueError('Factura no encontrada')
        
        return FacturaRepository.delete(factura_id)
