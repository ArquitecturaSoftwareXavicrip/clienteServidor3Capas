import React, { useState, useEffect } from 'react';
import { empleadosAPI } from '../services/api';

const EmpleadoView = () => {
  const [empleados, setEmpleados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    cargo: '',
  });

  useEffect(() => { loadEmpleados(); }, []);

  const loadEmpleados = async () => {
    try {
      setLoading(true);
      const res = await empleadosAPI.getAll();
      setEmpleados(res.data || []);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error cargando empleados');
    } finally { setLoading(false); }
  };

  const handleInputChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError(null); setSuccess(null);
      if (editingId) {
        await empleadosAPI.update(editingId, formData);
        setSuccess('Empleado actualizado');
      } else {
        await empleadosAPI.create(formData);
        setSuccess('Empleado creado');
      }
      resetForm();
      loadEmpleados();
    } catch (err) { setError(err.response?.data?.error || 'Error guardando'); }
  };

  const handleEdit = (empleado) => {
    setEditingId(empleado.id);
    setFormData({
      nombre: empleado.nombre,
      apellido: empleado.apellido,
      email: empleado.email,
      telefono: empleado.telefono,
      cargo: empleado.cargo,
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Eliminar empleado?')) return;
    try { await empleadosAPI.delete(id); setSuccess('Empleado eliminado'); loadEmpleados(); }
    catch (err) { setError(err.response?.data?.error || 'Error eliminando'); }
  };

  const resetForm = () => { setEditingId(null); setFormData({ nombre:'', apellido:'', email:'', telefono:'', cargo:'' }); };

  if (loading) return <div>Cargando empleados...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Empleado' : 'Nuevo Empleado'}</h2>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <form onSubmit={handleSubmit}>
          <div>
            <label>Nombre:</label>
            <input name="nombre" value={formData.nombre} onChange={handleInputChange} required />
          </div>
          <div>
            <label>Apellido:</label>
            <input name="apellido" value={formData.apellido} onChange={handleInputChange} required />
          </div>
          <div>
            <label>Email:</label>
            <input name="email" type="email" value={formData.email} onChange={handleInputChange} required />
          </div>
          <div>
            <label>Teléfono:</label>
            <input name="telefono" value={formData.telefono} onChange={handleInputChange} required />
          </div>
          <div>
            <label>Cargo:</label>
            <input name="cargo" value={formData.cargo} onChange={handleInputChange} required />
          </div>
          <div>
            <button type="submit">{editingId ? 'Actualizar' : 'Crear'}</button>
            {editingId && <button type="button" onClick={resetForm}>Cancelar</button>}
          </div>
        </form>
      </div>

      <div className="card">
        <h2>Lista de Empleados</h2>
        <table>
          <thead>
            <tr><th>ID</th><th>Nombre</th><th>Apellido</th><th>Email</th><th>Teléfono</th><th>Cargo</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            {empleados.length === 0 ? (
              <tr><td colSpan="7">No hay empleados</td></tr>
            ) : (
              empleados.map(emp => (
                <tr key={emp.id}>
                  <td>{emp.id}</td>
                  <td>{emp.nombre}</td>
                  <td>{emp.apellido}</td>
                  <td>{emp.email}</td>
                  <td>{emp.telefono}</td>
                  <td>{emp.cargo}</td>
                  <td>
                    <button onClick={() => handleEdit(emp)}>Editar</button>
                    <button onClick={() => handleDelete(emp.id)}>Eliminar</button>
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
