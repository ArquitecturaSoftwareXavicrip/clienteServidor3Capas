import React, { useState, useEffect } from 'react';
import { prestamosAPI } from '../services/api';

const PrestamoView = () => {
  const [prestamos, setPrestamos] = useState([]);
  const [editingId, setEditingId] = useState(null); // Para controlar la edición
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({ equipo: '', fecha_prestamo: '' });

  useEffect(() => { loadPrestamos(); }, []);

  const loadPrestamos = async () => {
    try {
      const response = await prestamosAPI.getAll();
      setPrestamos(response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar préstamos: Asegúrate de que el Backend esté corriendo.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await prestamosAPI.update(editingId, formData); // Operación de Editar
      } else {
        await prestamosAPI.create(formData); // Operación de Crear
      }
      setEditingId(null);
      setFormData({ equipo: '', fecha_prestamo: '' });
      loadPrestamos();
    } catch (err) { setError('Error al guardar datos'); }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Eliminar este préstamo?')) {
      await prestamosAPI.delete(id); // Operación de Eliminar
      loadPrestamos();
    }
  };

  const handleEdit = (p) => {
    setEditingId(p.id);
    setFormData({ equipo: p.equipo, fecha_prestamo: p.fecha_prestamo });
  };

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Préstamo' : 'Gestión de Préstamos'}</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Equipo" value={formData.equipo} 
                 onChange={(e) => setFormData({...formData, equipo: e.target.value})} required />
          <input type="date" value={formData.fecha_prestamo} 
                 onChange={(e) => setFormData({...formData, fecha_prestamo: e.target.value})} required />
          <button type="submit" className="btn btn-primary">{editingId ? 'Actualizar' : 'Registrar'}</button>
          {editingId && <button onClick={() => setEditingId(null)}>Cancelar</button>}
        </form>
      </div>

      <div className="card">
        <table>
          <thead><tr><th>Equipo</th><th>Fecha</th><th>Acciones</th></tr></thead>
          <tbody>
            {prestamos.map(p => (
              <tr key={p.id}>
                <td>{p.equipo}</td><td>{p.fecha_prestamo}</td>
                <td>
                  <button className="btn btn-edit" onClick={() => handleEdit(p)}>Editar</button>
                  <button className="btn btn-danger" onClick={() => handleDelete(p.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PrestamoView;