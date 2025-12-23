/*
 * ServicioView.jsx (corregido)
 * Vista de Servicios + Asignación de Empleados
 * - Un único componente que maneja creación/edición/eliminación de servicios
 * - Gestión de asignación/desasignación de empleados al editar un servicio
 * - Manejo seguro de valores nulos/indefinidos y de inputs numéricos
 */

import React, { useEffect, useState } from 'react';
import { servicioService, empleadosAPI } from '../services/api';

const ServicioView = () => {
  const [servicios, setServicios] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [editingId, setEditingId] = useState(null);
  const [assignedEmployeeIds, setAssignedEmployeeIds] = useState([]);

  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio_base: '',
    duracion_horas: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [serviciosRes, empleadosRes] = await Promise.all([
        servicioService.getAll(),
        empleadosAPI.getAll(),
      ]);

      setServicios(serviciosRes?.data || []);
      setEmpleados(empleadosRes?.data || []);
    } catch (err) {
      setError(err?.response?.data?.error || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const resetForm = () => {
    setEditingId(null);
    setAssignedEmployeeIds([]);
    setFormData({ nombre: '', descripcion: '', precio_base: '', duracion_horas: '' });
    setError(null);
    setSuccess(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      setSuccess(null);

      const payload = {
        nombre: formData.nombre,
        descripcion: formData.descripcion || null,
        // Convertir a número cuando haya valor, sino null
        precio_base: formData.precio_base === '' ? null : parseFloat(formData.precio_base),
        duracion_horas: formData.duracion_horas === '' ? null : parseFloat(formData.duracion_horas),
      };

      if (editingId) {
        await servicioService.update(editingId, payload);
        setSuccess('Servicio actualizado correctamente');
      } else {
        await servicioService.create(payload);
        setSuccess('Servicio creado correctamente');
      }

      // Recargar lista completa para mantener consistencia
      await loadData();
      resetForm();
    } catch (err) {
      setError(err?.response?.data?.error || 'Error al guardar servicio');
    }
  };

  const handleEdit = (servicio) => {
    setEditingId(servicio.id);

    setFormData({
      nombre: servicio.nombre ?? '',
      descripcion: servicio.descripcion ?? '',
      precio_base: servicio.precio_base != null ? String(servicio.precio_base) : '',
      duracion_horas: servicio.duracion_horas != null ? String(servicio.duracion_horas) : '',
    });

    const currentIds = Array.isArray(servicio.empleados) ? servicio.empleados.map((e) => e.id) : [];
    setAssignedEmployeeIds(currentIds);

    // Llevar la vista al formulario (solo en cliente)
    if (typeof window !== 'undefined' && window.scrollTo) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const toggleEmpleado = async (empleadoId) => {
    if (!editingId) return; // Solo en modo edición

    const isAssigned = assignedEmployeeIds.includes(empleadoId);

    try {
      setError(null);
      if (isAssigned) {
        await servicioService.desasignarEmpleado(editingId, empleadoId);
        setAssignedEmployeeIds((prev) => prev.filter((id) => id !== empleadoId));
      } else {
        await servicioService.asignarEmpleado(editingId, empleadoId);
        setAssignedEmployeeIds((prev) => [...prev, empleadoId]);
      }

      // Actualizar la lista principal para reflejar el cambio (simplificado: recargar todo)
      const srvRes = await servicioService.getAll();
      setServicios(srvRes?.data || []);
    } catch (err) {
      setError(err?.response?.data?.error || 'Error al modificar asignación de empleado');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Está seguro de eliminar este servicio?')) return;

    try {
      setError(null);
      await servicioService.delete(id);
      setSuccess('Servicio eliminado correctamente');
      const srvRes = await servicioService.getAll();
      setServicios(srvRes?.data || []);
      // Si eliminamos el que estábamos editando, limpiar formulario
      if (editingId === id) resetForm();
    } catch (err) {
      setError(err?.response?.data?.error || 'Error al eliminar servicio');
    }
  };

  const formatCurrency = (v) => {
    if (v == null || Number.isNaN(Number(v))) return '-';
    try {
      return `$${Number(v).toFixed(2)}`;
    } catch {
      return '-';
    }
  };

  const formatDuration = (d) => {
    if (d == null || d === '') return '-';
    return `${d}h`;
  };

  if (loading) return <div className="loading">Cargando datos...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{editingId ? 'Editar Servicio' : 'Nuevo Servicio'}</h2>

        {error && <div className="error" role="alert">{error}</div>}
        {success && <div className="success" role="status">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre:</label>
            <input id="nombre" name="nombre" type="text" value={formData.nombre} onChange={handleInputChange} required />
          </div>

          <div className="form-group">
            <label htmlFor="descripcion">Descripción:</label>
            <textarea id="descripcion" name="descripcion" value={formData.descripcion} onChange={handleInputChange} />
          </div>

          <div className="form-group">
            <label htmlFor="precio_base">Precio Base:</label>
            <input
              id="precio_base"
              name="precio_base"
              type="number"
              inputMode="decimal"
              value={formData.precio_base}
              onChange={handleInputChange}
              step="0.01"
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="duracion_horas">Duración (horas):</label>
            <input
              id="duracion_horas"
              name="duracion_horas"
              type="number"
              value={formData.duracion_horas}
              onChange={handleInputChange}
              step="0.5"
              min="0.5"
              required
            />
          </div>

          {editingId && (
            <div className="form-group" style={{ marginTop: 20, borderTop: '1px solid #eee', paddingTop: 15 }}>
              <h3>Asignar Empleados</h3>
              <p className="small-text">Seleccione los empleados que realizan este servicio:</p>

              {empleados.length === 0 ? (
                <p>No hay empleados registrados.</p>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 10 }}>
                  {empleados.map((empleado) => (
                    <label key={empleado.id} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: 6, border: '1px solid #ddd', borderRadius: 4 }}>
                      <input
                        type="checkbox"
                        checked={assignedEmployeeIds.includes(empleado.id)}
                        onChange={() => toggleEmpleado(empleado.id)}
                        style={{ marginRight: 8 }}
                      />
                      <span>{empleado.nombre} {empleado.apellido ?? ''}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="button-group" style={{ marginTop: 20 }}>
            <button type="submit" className="btn btn-primary">{editingId ? 'Actualizar Datos' : 'Crear Servicio'}</button>
            {editingId && (
              <button type="button" className="btn btn-secondary" onClick={resetForm} style={{ marginLeft: 8 }}>Cancelar</button>
            )}
          </div>
        </form>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <h2>Lista de Servicios</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Precio Base</th>
              <th>Duración</th>
              <th>Empleados Asignados</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {servicios.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center' }}>No hay servicios registrados</td>
              </tr>
            ) : (
              servicios.map((servicio) => (
                <tr key={servicio.id}>
                  <td>{servicio.id}</td>
                  <td>{servicio.nombre}</td>
                  <td>{formatCurrency(servicio.precio_base)}</td>
                  <td>{formatDuration(servicio.duracion_horas)}</td>
                  <td>
                    {Array.isArray(servicio.empleados) && servicio.empleados.length > 0
                      ? servicio.empleados.map((e) => e.nombre).join(', ')
                      : <span style={{ color: '#888' }}>Sin asignar</span>}
                  </td>
                  <td>
                    <button className="btn btn-edit" onClick={() => handleEdit(servicio)} style={{ marginRight: 8 }}>Editar</button>
                    <button className="btn btn-danger" onClick={() => handleDelete(servicio.id)}>Eliminar</button>
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
