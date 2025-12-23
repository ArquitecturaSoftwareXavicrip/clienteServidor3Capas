/**
 * Vista de Facturas - Tier 1: Presentación (MVC View)
 * Componente React que representa la vista de gestión de facturas
 */
import React, { useState, useEffect } from 'react';
import { facturasAPI, empresasAPI, empleadosAPI, serviciosAPI } from '../services/api';

const FacturaView = () => {
  const [facturas, setFacturas] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [servicios, setServicios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    empresa_id: '',
    empleado_id: '',
    servicio_id: '',
    fecha_factura: new Date().toISOString().split('T')[0],
    fecha_vencimiento: '',
    descripcion: '',
    cantidad: '',
    precio_unitario: '',
    impuesto: '0',
    estado: 'pendiente',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [facturasRes, empresasRes, empleadosRes, serviciosRes] = await Promise.all([
        facturasAPI.getAll(),
        empresasAPI.getAll(),
        empleadosAPI.getAll(),
        serviciosAPI.getAll(),
      ]);
      setFacturas(facturasRes.data);
      setEmpresas(empresasRes.data);
      setEmpleados(empleadosRes.data);
      setServicios(serviciosRes.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      setSuccess(null);
      
      const dataToSend = {
        ...formData,
        empresa_id: parseInt(formData.empresa_id),
        empleado_id: parseInt(formData.empleado_id),
        servicio_id: parseInt(formData.servicio_id),
        cantidad: parseInt(formData.cantidad),
        precio_unitario: parseFloat(formData.precio_unitario),
        impuesto: parseFloat(formData.impuesto),
      };
      
      if (editingId) {
        await facturasAPI.update(editingId, dataToSend);
        setSuccess('Factura actualizada correctamente');
      } else {
        await facturasAPI.create(dataToSend);
        setSuccess('Factura creada correctamente');
      }
      
      resetForm();
      loadData();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar factura');
    }
  };

  const handleEdit = (factura) => {
    setEditingId(factura.id);
    setFormData({
      empresa_id: factura.empresa_id.toString(),
      empleado_id: factura.empleado_id.toString(),
      servicio_id: factura.servicio_id.toString(),
      fecha_factura: factura.fecha_factura,
      fecha_vencimiento: factura.fecha_vencimiento,
      descripcion: factura.descripcion,
      cantidad: factura.cantidad.toString(),
      precio_unitario: factura.precio_unitario.toString(),
      impuesto: factura.impuesto.toString(),
      estado: factura.estado,
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar esta factura?')) {
      return;
    }
    
    try {
      setError(null);
      await facturasAPI.delete(id);
      setSuccess('Factura eliminada correctamente');
      loadData();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar factura');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      empresa_id: '',
      empleado_id: '',
      servicio_id: '',
      fecha_factura: new Date().toISOString().split('T')[0],
      fecha_vencimiento: '',
      descripcion: '',
      cantidad: '',
      precio_unitario: '',
      impuesto: '0',
      estado: 'pendiente',
    });
  };

  const getEmpresaNombre = (id) => {
    const empresa = empresas.find(e => e.id === id);
    return empresa ? empresa.nombre : 'N/A';
  };

  const getEmpleadoNombre = (id) => {
    const empleado = empleados.find(e => e.id === id);
    return empleado ? `${empleado.nombre} ${empleado.apellido}` : 'N/A';
  };

  const getServicioNombre = (id) => {
    const servicio = servicios.find(s => s.id === id);
    return servicio ? servicio.nombre : 'N/A';
  };

  if (loading) {
    return <div className="loading">Cargando facturas...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Factura' : 'Nueva Factura'}</h2>
        
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Empresa:</label>
            <select
              name="empresa_id"
              value={formData.empresa_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Seleccionar empresa...</option>
              {empresas.map((empresa) => (
                <option key={empresa.id} value={empresa.id}>
                  {empresa.nombre}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Empleado:</label>
            <select
              name="empleado_id"
              value={formData.empleado_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Seleccionar empleado...</option>
              {empleados.map((empleado) => (
                <option key={empleado.id} value={empleado.id}>
                  {empleado.nombre} {empleado.apellido}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Servicio:</label>
            <select
              name="servicio_id"
              value={formData.servicio_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Seleccionar servicio...</option>
              {servicios.map((servicio) => (
                <option key={servicio.id} value={servicio.id}>
                  {servicio.nombre}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Fecha de Factura:</label>
            <input
              type="date"
              name="fecha_factura"
              value={formData.fecha_factura}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Fecha de Vencimiento:</label>
            <input
              type="date"
              name="fecha_vencimiento"
              value={formData.fecha_vencimiento}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Descripción:</label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleInputChange}
              required
              rows="3"
            />
          </div>
          
          <div className="form-group">
            <label>Cantidad:</label>
            <input
              type="number"
              name="cantidad"
              value={formData.cantidad}
              onChange={handleInputChange}
              required
              min="1"
            />
          </div>
          
          <div className="form-group">
            <label>Precio Unitario:</label>
            <input
              type="number"
              name="precio_unitario"
              value={formData.precio_unitario}
              onChange={handleInputChange}
              required
              min="0"
              step="0.01"
            />
          </div>
          
          <div className="form-group">
            <label>Impuesto (%):</label>
            <input
              type="number"
              name="impuesto"
              value={formData.impuesto}
              onChange={handleInputChange}
              min="0"
              step="0.01"
            />
          </div>
          
          <div className="form-group">
            <label>Estado:</label>
            <select
              name="estado"
              value={formData.estado}
              onChange={handleInputChange}
            >
              <option value="pendiente">Pendiente</option>
              <option value="pagada">Pagada</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          
          <div className="button-group">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Actualizar' : 'Crear'}
            </button>
            {editingId && (
              <button type="button" className="btn btn-secondary" onClick={resetForm}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <h2>Lista de Facturas</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>Empleado</th>
              <th>Servicio</th>
              <th>Fecha</th>
              <th>Cantidad</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {facturas.length === 0 ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center' }}>
                  No hay facturas registradas
                </td>
              </tr>
            ) : (
              facturas.map((factura) => (
                <tr key={factura.id}>
                  <td>{factura.id}</td>
                  <td>{getEmpresaNombre(factura.empresa_id)}</td>
                  <td>{getEmpleadoNombre(factura.empleado_id)}</td>
                  <td>{getServicioNombre(factura.servicio_id)}</td>
                  <td>{factura.fecha_factura}</td>
                  <td>{factura.cantidad}</td>
                  <td>${factura.total.toFixed(2)}</td>
                  <td>
                    <span className={`status status-${factura.estado}`}>
                      {factura.estado}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(factura)}
                      style={{ marginRight: '5px' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(factura.id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FacturaView;
