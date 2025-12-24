from app.repositories.pago_repository import PagoRepository

class PagoService:
    @staticmethod
    def registrar_pago(data):
        if data.get('monto_base', 0) <= 0:
            raise ValueError("El monto base debe ser mayor a cero")
        
        # Lógica de extras: supongamos que los extras no pueden superar el 50% del base
        if data.get('extras', 0) > (data['monto_base'] * 0.5):
            raise ValueError("Los extras no pueden exceder el 50% del sueldo base")
            
        return PagoRepository.create(data)