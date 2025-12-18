/**
 * Vista de Contratos - Tier 1: Presentación (MVC View)
 * Componente React que representa la vista de gestión de contratos
 */
import React, { useState, useEffect } from 'react';
import { contratosAPI, empresasAPI, serviciosAPI } from '../services/api';

const ContratoView = () => {
  const [contratos, setContratos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [servicios, setServicios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    empresa_id: '',
    servicio_id: '',
    fecha_inicio: '',
    fecha_fin: '',
    estado: 'activo',
    precio_final: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [contratosRes, empresasRes, serviciosRes] = await Promise.all([
        contratosAPI.getAll(),
        empresasAPI.getAll(),
        serviciosAPI.getAll(),
      ]);
      setContratos(contratosRes.data);
      setEmpresas(empresasRes.data);
      setServicios(serviciosRes.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    
    // Si cambia el servicio, actualizar el precio final automáticamente
    if (name === 'servicio_id' && value) {
      const servicio = servicios.find(s => s.id === parseInt(value));
      if (servicio) {
        setFormData(prev => ({
          ...prev,
          servicio_id: value,
          precio_final: servicio.precio_base.toString(),
        }));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      setSuccess(null);
      
      const data = {
        ...formData,
        empresa_id: parseInt(formData.empresa_id),
        servicio_id: parseInt(formData.servicio_id),
        precio_final: parseFloat(formData.precio_final),
        fecha_fin: formData.fecha_fin || null,
      };
      
      if (editingId) {
        await contratosAPI.update(editingId, data);
        setSuccess('Contrato actualizado correctamente');
      } else {
        await contratosAPI.create(data);
        setSuccess('Contrato creado correctamente');
      }
      
      resetForm();
      loadData();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar contrato');
    }
  };

  const handleEdit = (contrato) => {
    setEditingId(contrato.id);
    setFormData({
      empresa_id: contrato.empresa_id.toString(),
      servicio_id: contrato.servicio_id.toString(),
      fecha_inicio: contrato.fecha_inicio,
      fecha_fin: contrato.fecha_fin || '',
      estado: contrato.estado,
      precio_final: contrato.precio_final.toString(),
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar este contrato?')) {
      return;
    }
    
    try {
      setError(null);
      await contratosAPI.delete(id);
      setSuccess('Contrato eliminado correctamente');
      loadData();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar contrato');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      empresa_id: '',
      servicio_id: '',
      fecha_inicio: '',
      fecha_fin: '',
      estado: 'activo',
      precio_final: '',
    });
  };

  const getEmpresaNombre = (empresaId) => {
    const empresa = empresas.find(e => e.id === empresaId);
    return empresa ? empresa.nombre : 'N/A';
  };

  const getServicioNombre = (servicioId) => {
    const servicio = servicios.find(s => s.id === servicioId);
    return servicio ? servicio.nombre : 'N/A';
  };

  if (loading) {
    return <div className="loading">Cargando contratos...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Contrato' : 'Nuevo Contrato'}</h2>
        
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
              <option value="">Seleccione una empresa</option>
              {empresas.map((empresa) => (
                <option key={empresa.id} value={empresa.id}>
                  {empresa.nombre}
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
              <option value="">Seleccione un servicio</option>
              {servicios.map((servicio) => (
                <option key={servicio.id} value={servicio.id}>
                  {servicio.nombre} - ${servicio.precio_base.toFixed(2)}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Fecha de Inicio:</label>
            <input
              type="date"
              name="fecha_inicio"
              value={formData.fecha_inicio}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Fecha de Fin (opcional):</label>
            <input
              type="date"
              name="fecha_fin"
              value={formData.fecha_fin}
              onChange={handleInputChange}
            />
          </div>
          
          <div className="form-group">
            <label>Estado:</label>
            <select
              name="estado"
              value={formData.estado}
              onChange={handleInputChange}
              required
            >
              <option value="activo">Activo</option>
              <option value="finalizado">Finalizado</option>
              <option value="cancelado">Cancelado</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Precio Final:</label>
            <input
              type="number"
              name="precio_final"
              value={formData.precio_final}
              onChange={handleInputChange}
              step="0.01"
              min="0"
              required
            />
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
        <h2>Lista de Contratos</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>Servicio</th>
              <th>Fecha Inicio</th>
              <th>Fecha Fin</th>
              <th>Estado</th>
              <th>Precio Final</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {contratos.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center' }}>
                  No hay contratos registrados
                </td>
              </tr>
            ) : (
              contratos.map((contrato) => (
                <tr key={contrato.id}>
                  <td>{contrato.id}</td>
                  <td>{getEmpresaNombre(contrato.empresa_id)}</td>
                  <td>{getServicioNombre(contrato.servicio_id)}</td>
                  <td>{contrato.fecha_inicio}</td>
                  <td>{contrato.fecha_fin || '-'}</td>
                  <td>{contrato.estado}</td>
                  <td>${contrato.precio_final.toFixed(2)}</td>
                  <td>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(contrato)}
                      style={{ marginRight: '5px' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(contrato.id)}
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

export default ContratoView;


