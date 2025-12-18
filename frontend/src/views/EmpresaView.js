/**
 * Vista de Empresas - Tier 1: Presentación (MVC View)
 * Componente React que representa la vista de gestión de empresas
 */
import React, { useState, useEffect } from 'react';
import { empresasAPI } from '../services/api';

const EmpresaView = () => {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
    telefono: '',
    email: '',
  });

  useEffect(() => {
    loadEmpresas();
  }, []);

  const loadEmpresas = async () => {
    try {
      setLoading(true);
      const response = await empresasAPI.getAll();
      setEmpresas(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al cargar empresas');
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
      
      if (editingId) {
        await empresasAPI.update(editingId, formData);
        setSuccess('Empresa actualizada correctamente');
      } else {
        await empresasAPI.create(formData);
        setSuccess('Empresa creada correctamente');
      }
      
      resetForm();
      loadEmpresas();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al guardar empresa');
    }
  };

  const handleEdit = (empresa) => {
    setEditingId(empresa.id);
    setFormData({
      nombre: empresa.nombre,
      direccion: empresa.direccion,
      telefono: empresa.telefono,
      email: empresa.email,
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar esta empresa?')) {
      return;
    }
    
    try {
      setError(null);
      await empresasAPI.delete(id);
      setSuccess('Empresa eliminada correctamente');
      loadEmpresas();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al eliminar empresa');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      nombre: '',
      direccion: '',
      telefono: '',
      email: '',
    });
  };

  if (loading) {
    return <div className="loading">Cargando empresas...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Empresa' : 'Nueva Empresa'}</h2>
        
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
            <label>Dirección:</label>
            <input
              type="text"
              name="direccion"
              value={formData.direccion}
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
        <h2>Lista de Empresas</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Dirección</th>
              <th>Teléfono</th>
              <th>Email</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empresas.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center' }}>
                  No hay empresas registradas
                </td>
              </tr>
            ) : (
              empresas.map((empresa) => (
                <tr key={empresa.id}>
                  <td>{empresa.id}</td>
                  <td>{empresa.nombre}</td>
                  <td>{empresa.direccion}</td>
                  <td>{empresa.telefono}</td>
                  <td>{empresa.email}</td>
                  <td>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(empresa)}
                      style={{ marginRight: '5px' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(empresa.id)}
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

export default EmpresaView;


