/**
 * Vista de Servicios - Tier 1: Presentación (MVC View)
 * Componente React que representa la vista de gestión de servicios
 */
import React, { useState, useEffect } from 'react';
import { serviciosAPI } from '../services/api';

const ServicioView = () => {
  const [servicios, setServicios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio_base: '',
    duracion_horas: '',
  });

  useEffect(() => {
    loadServicios();
  }, []);

  const loadServicios = async () => {
    try {
      setLoading(true);
      const response = await serviciosAPI.getAll();
      setServicios(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar servicios');
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
      
      const data = {
        ...formData,
        precio_base: parseFloat(formData.precio_base),
        duracion_horas: parseFloat(formData.duracion_horas),
      };
      
      if (editingId) {
        await serviciosAPI.update(editingId, data);
        setSuccess('Servicio actualizado correctamente');
      } else {
        await serviciosAPI.create(data);
        setSuccess('Servicio creado correctamente');
      }
      
      resetForm();
      loadServicios();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar servicio');
    }
  };

  const handleEdit = (servicio) => {
    setEditingId(servicio.id);
    setFormData({
      nombre: servicio.nombre,
      descripcion: servicio.descripcion || '',
      precio_base: servicio.precio_base.toString(),
      duracion_horas: servicio.duracion_horas.toString(),
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar este servicio?')) {
      return;
    }
    
    try {
      setError(null);
      await serviciosAPI.delete(id);
      setSuccess('Servicio eliminado correctamente');
      loadServicios();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar servicio');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      nombre: '',
      descripcion: '',
      precio_base: '',
      duracion_horas: '',
    });
  };

  if (loading) {
    return <div className="loading">Cargando servicios...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Servicio' : 'Nuevo Servicio'}</h2>
        
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nombre:</label>
            <input
              type="text"
              name="nombre"
              value={formData.nombre}
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
            />
          </div>
          
          <div className="form-group">
            <label>Precio Base:</label>
            <input
              type="number"
              name="precio_base"
              value={formData.precio_base}
              onChange={handleInputChange}
              step="0.01"
              min="0"
              required
            />
          </div>
          
          <div className="form-group">
            <label>Duración (horas):</label>
            <input
              type="number"
              name="duracion_horas"
              value={formData.duracion_horas}
              onChange={handleInputChange}
              step="0.5"
              min="0.5"
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
        <h2>Lista de Servicios</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio Base</th>
              <th>Duración (h)</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {servicios.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center' }}>
                  No hay servicios registrados
                </td>
              </tr>
            ) : (
              servicios.map((servicio) => (
                <tr key={servicio.id}>
                  <td>{servicio.id}</td>
                  <td>{servicio.nombre}</td>
                  <td>{servicio.descripcion || '-'}</td>
                  <td>${servicio.precio_base.toFixed(2)}</td>
                  <td>{servicio.duracion_horas}h</td>
                  <td>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(servicio)}
                      style={{ marginRight: '5px' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(servicio.id)}
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

export default ServicioView;



