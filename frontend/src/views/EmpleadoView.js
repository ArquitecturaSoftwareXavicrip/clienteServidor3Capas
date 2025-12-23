/**
 * Vista de Empleados - Tier 1: Presentación (MVC View)
 * Componente React para la gestión y seguimiento de empleados
 */
import React, { useState, useEffect } from 'react';
// Asegúrate de haber exportado empleadosAPI en services/api.js como vimos antes
import { empleadosAPI } from '../services/api';

const EmpleadoView = () => {
  const [empleados, setEmpleados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  
  // Estado del formulario adaptado a la entidad Empleado
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    cargo: ''
  });

  useEffect(() => {
    loadEmpleados();
  }, []);

  const loadEmpleados = async () => {
    try {
      setLoading(true);
      const response = await empleadosAPI.getAll();
      setEmpleados(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar empleados');
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
      
      // La lógica sirve tanto para Crear como para Editar si el backend lo soporta
      // Si solo implementamos create en el paso anterior, aquí usaremos create.
      if (editingId) {
        // Asumiendo que implementaste update en el backend/API
        // await empleadosAPI.update(editingId, formData);
        // setSuccess('Empleado actualizado correctamente');
        console.warn("La actualización requiere implementar PUT en el backend");
      } else {
        await empleadosAPI.create(formData);
        setSuccess('Empleado registrado correctamente');
      }
      
      resetForm();
      loadEmpleados();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar empleado');
    }
  };

  const handleEdit = (empleado) => {
    setEditingId(empleado.id);
    setFormData({
      nombre: empleado.nombre,
      apellido: empleado.apellido,
      email: empleado.email,
      telefono: empleado.telefono || '',
      cargo: empleado.cargo || '',
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de dar de baja a este empleado?')) {
      return;
    }
    
    try {
      setError(null);
      await empleadosAPI.delete(id);
      setSuccess('Empleado eliminado correctamente');
      loadEmpleados();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar empleado');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      nombre: '',
      apellido: '',
      email: '',
      telefono: '',
      cargo: ''
    });
  };

  if (loading) {
    return <div className="loading">Cargando personal...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Empleado' : 'Nuevo Empleado'}</h2>
        
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
            <label>Apellido:</label>
            <input
              type="text"
              name="apellido"
              value={formData.apellido}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Teléfono:</label>
            <input
              type="text"
              name="telefono"
              value={formData.telefono}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Cargo:</label>
            <input
              type="text"
              name="cargo"
              value={formData.cargo}
              onChange={handleInputChange}
              placeholder="Ej: Supervisor, Limpieza..."
            />
          </div>
          
          <div className="button-group">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Actualizar' : 'Registrar'}
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
        <h2>Plantilla de Empleados</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre Completo</th>
              <th>Cargo</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center' }}>
                  No hay empleados registrados
                </td>
              </tr>
            ) : (
              empleados.map((empleado) => (
                <tr key={empleado.id}>
                  <td>{empleado.id}</td>
                  <td>{empleado.nombre} {empleado.apellido}</td>
                  <td>{empleado.cargo}</td>
                  <td>{empleado.email}</td>
                  <td>{empleado.telefono}</td>
                  <td>
                    {/* Simulamos estado activo ya que en el modelo pusimos activo=True por defecto */}
                    <span style={{ 
                      backgroundColor: '#e6fffa', 
                      color: '#047857', 
                      padding: '4px 8px', 
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      Activo
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(empleado)}
                      style={{ marginRight: '5px' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(empleado.id)}
                    >
                      Baja
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

export default EmpleadoView;