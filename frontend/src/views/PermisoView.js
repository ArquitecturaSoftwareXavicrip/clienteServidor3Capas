/**
 * Vista de Permisos - Tier 1: Presentación (MVC View)
 * Componente React que representa la vista de gestión de permisos de vacaciones
 */
import React, { useState, useEffect, useCallback } from 'react';
import { permisosAPI } from '../services/api';

const PermisoView = () => {
  const [permisos, setPermisos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [filtroEstado, setFiltroEstado] = useState('todos');
  const [formData, setFormData] = useState({
    empleado: '',
    tipo: 'Vacaciones',
    fecha_inicio: '',
    fecha_fin: '',
    dias_solicitados: '',
    estado: 'pendiente',
    observaciones: '',
  });

  const loadPermisos = useCallback(async () => {
    try {
      setLoading(true);
      let response;
      if (filtroEstado === 'todos') {
        response = await permisosAPI.getAll();
      } else {
        response = await permisosAPI.getByEstado(filtroEstado);
      }
      setPermisos(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar permisos');
    } finally {
      setLoading(false);
    }
  }, [filtroEstado]);

  useEffect(() => {
    loadPermisos();
  }, [loadPermisos]);

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
      
      // Convertir dias_solicitados a número
      const dataToSend = {
        ...formData,
        dias_solicitados: parseInt(formData.dias_solicitados, 10),
      };
      
      if (editingId) {
        await permisosAPI.update(editingId, dataToSend);
        setSuccess('Permiso actualizado correctamente');
      } else {
        await permisosAPI.create(dataToSend);
        setSuccess('Permiso creado correctamente');
      }
      
      resetForm();
      loadPermisos();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar permiso');
    }
  };

  const handleEdit = (permiso) => {
    setEditingId(permiso.id);
    setFormData({
      empleado: permiso.empleado,
      tipo: permiso.tipo,
      fecha_inicio: permiso.fecha_inicio,
      fecha_fin: permiso.fecha_fin,
      dias_solicitados: permiso.dias_solicitados.toString(),
      estado: permiso.estado,
      observaciones: permiso.observaciones || '',
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar este permiso?')) {
      return;
    }
    
    try {
      setError(null);
      await permisosAPI.delete(id);
      setSuccess('Permiso eliminado correctamente');
      loadPermisos();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar permiso');
    }
  };

  const handleAprobar = async (id) => {
    if (!window.confirm('¿Está seguro de aprobar este permiso?')) {
      return;
    }
    
    try {
      setError(null);
      await permisosAPI.aprobar(id);
      setSuccess('Permiso aprobado correctamente');
      loadPermisos();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al aprobar permiso');
    }
  };

  const handleRechazar = async (id) => {
    const observaciones = window.prompt('Ingrese el motivo del rechazo (opcional):');
    if (observaciones === null) {
      return; // Usuario canceló
    }
    
    try {
      setError(null);
      await permisosAPI.rechazar(id, observaciones);
      setSuccess('Permiso rechazado correctamente');
      loadPermisos();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al rechazar permiso');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      empleado: '',
      tipo: 'Vacaciones',
      fecha_inicio: '',
      fecha_fin: '',
      dias_solicitados: '',
      estado: 'pendiente',
      observaciones: '',
    });
  };

  const getEstadoClass = (estado) => {
    switch (estado) {
      case 'aprobado':
        return 'estado-aprobado';
      case 'rechazado':
        return 'estado-rechazado';
      case 'pendiente':
        return 'estado-pendiente';
      default:
        return '';
    }
  };

  if (loading) {
    return <div className="loading">Cargando permisos...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Permiso' : 'Nuevo Permiso de Vacaciones'}</h2>
        
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Empleado:</label>
            <input
              type="text"
              name="empleado"
              value={formData.empleado}
              onChange={handleInputChange}
              placeholder="Nombre completo del empleado"
              required
            />
          </div>
          
          <div className="form-group">
            <label>Tipo:</label>
            <input
              type="text"
              name="tipo"
              value={formData.tipo}
              onChange={handleInputChange}
              readOnly
            />
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
            <label>Fecha de Fin:</label>
            <input
              type="date"
              name="fecha_fin"
              value={formData.fecha_fin}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Días Solicitados:</label>
            <input
              type="number"
              name="dias_solicitados"
              value={formData.dias_solicitados}
              onChange={handleInputChange}
              min="1"
              required
            />
          </div>
          
          {editingId && (
            <div className="form-group">
              <label>Estado:</label>
              <select
                name="estado"
                value={formData.estado}
                onChange={handleInputChange}
              >
                <option value="pendiente">Pendiente</option>
                <option value="aprobado">Aprobado</option>
                <option value="rechazado">Rechazado</option>
              </select>
            </div>
          )}
          
          <div className="form-group">
            <label>Observaciones:</label>
            <textarea
              name="observaciones"
              value={formData.observaciones}
              onChange={handleInputChange}
              rows="3"
              placeholder="Observaciones adicionales (opcional)"
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
        <h2>Lista de Permisos de Vacaciones</h2>
        
        <div className="filter-group" style={{ marginBottom: '15px' }}>
          <label>Filtrar por estado: </label>
          <select
            value={filtroEstado}
            onChange={(e) => setFiltroEstado(e.target.value)}
            style={{ padding: '5px', marginLeft: '10px' }}
          >
            <option value="todos">Todos</option>
            <option value="pendiente">Pendientes</option>
            <option value="aprobado">Aprobados</option>
            <option value="rechazado">Rechazados</option>
          </select>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Empleado</th>
              <th>Tipo</th>
              <th>Fecha Inicio</th>
              <th>Fecha Fin</th>
              <th>Días</th>
              <th>Estado</th>
              <th>Observaciones</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {permisos.length === 0 ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center' }}>
                  No hay permisos registrados
                </td>
              </tr>
            ) : (
              permisos.map((permiso) => (
                <tr key={permiso.id}>
                  <td>{permiso.id}</td>
                  <td>{permiso.empleado}</td>
                  <td>{permiso.tipo}</td>
                  <td>{permiso.fecha_inicio}</td>
                  <td>{permiso.fecha_fin}</td>
                  <td>{permiso.dias_solicitados}</td>
                  <td>
                    <span className={getEstadoClass(permiso.estado)}>
                      {permiso.estado.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {permiso.observaciones || '-'}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                      {permiso.estado === 'pendiente' && (
                        <>
                          <button
                            className="btn btn-success"
                            onClick={() => handleAprobar(permiso.id)}
                            style={{ fontSize: '0.85em', padding: '4px 8px' }}
                          >
                            Aprobar
                          </button>
                          <button
                            className="btn btn-warning"
                            onClick={() => handleRechazar(permiso.id)}
                            style={{ fontSize: '0.85em', padding: '4px 8px' }}
                          >
                            Rechazar
                          </button>
                        </>
                      )}
                      <button
                        className="btn btn-edit"
                        onClick={() => handleEdit(permiso)}
                        style={{ fontSize: '0.85em', padding: '4px 8px' }}
                      >
                        Editar
                      </button>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleDelete(permiso.id)}
                        style={{ fontSize: '0.85em', padding: '4px 8px' }}
                      >
                        Eliminar
                      </button>
                    </div>
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

export default PermisoView;

