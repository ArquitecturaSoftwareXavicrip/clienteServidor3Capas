import React, { useState, useEffect } from 'react';
import { asignacionesAPI, contratosAPI, serviciosAPI, empleadosAPI, espaciosAPI } from '../services/api';

const AsignacionView = () => {
    const [asignaciones, setAsignaciones] = useState([]);
    const [contratos, setContratos] = useState([]);
    const [servicios, setServicios] = useState([]);
    const [empleados, setEmpleados] = useState([]);
    const [espacios, setEspacios] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [editingId, setEditingId] = useState(null);

    const [formData, setFormData] = useState({
        contrato_id: '',
        servicio_id: '',
        empleado_id: '',
        espacio_id: '',
        fecha_inicio: '',
        fecha_fin: '',
        hora_inicio: '',
        hora_fin: '',
        frecuencia: 'DIARIO',
        estado: 'ACTIVO'
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [asigRes, contRes, servRes, emplRes, espRes] = await Promise.all([
                asignacionesAPI.getAll(),
                contratosAPI.getAll(),
                serviciosAPI.getAll(),
                empleadosAPI.getAll(),
                espaciosAPI.getAll()
            ]);

            setAsignaciones(asigRes.data);
            setContratos(contRes.data);
            setServicios(servRes.data);
            setEmpleados(emplRes.data);
            setEspacios(espRes.data);
            setError(null);
        } catch (err) {
            setError('Error al cargar datos. Asegúrate de que todos los recursos (contratos/servicios/empleados) existan.');
            console.error(err);
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

            const payload = { ...formData };

            // Convert select values to integers
            ['contrato_id', 'servicio_id', 'empleado_id', 'espacio_id'].forEach(field => {
                if (payload[field]) payload[field] = parseInt(payload[field]);
            });

            if (!payload.fecha_fin) delete payload.fecha_fin;

            if (editingId) {
                await asignacionesAPI.update(editingId, payload);
                setSuccess('Asignación actualizada correctamente');
            } else {
                await asignacionesAPI.create(payload);
                setSuccess('Asignación creada correctamente');
            }

            resetForm();
            const res = await asignacionesAPI.getAll();
            setAsignaciones(res.data);
        } catch (err) {
            // Backend overlap error messages usually come as strings in error field
            setError(err.response?.data?.error || 'Error al guardar asignación');
        }
    };

    const handleEdit = (asig) => {
        setEditingId(asig.id);
        // Parse times (HH:MM:SS -> HH:MM) for HTML time input
        const fmtTime = (t) => t ? t.substring(0, 5) : '';

        setFormData({
            contrato_id: asig.contrato_id,
            servicio_id: asig.servicio_id,
            empleado_id: asig.empleado_id,
            espacio_id: asig.espacio_id,
            fecha_inicio: asig.fecha_inicio.split('T')[0],
            fecha_fin: asig.fecha_fin ? asig.fecha_fin.split('T')[0] : '',
            hora_inicio: fmtTime(asig.hora_inicio),
            hora_fin: fmtTime(asig.hora_fin),
            frecuencia: asig.frecuencia,
            estado: asig.estado
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Eliminar asignación?')) return;
        try {
            await asignacionesAPI.delete(id);
            setSuccess('Eliminado correctamente');
            const res = await asignacionesAPI.getAll();
            setAsignaciones(res.data);
        } catch (err) {
            setError('Error al eliminar');
        }
    };

    const resetForm = () => {
        setEditingId(null);
        setFormData({
            contrato_id: '',
            servicio_id: '',
            empleado_id: '',
            espacio_id: '',
            fecha_inicio: '',
            fecha_fin: '',
            hora_inicio: '',
            hora_fin: '',
            frecuencia: 'DIARIO',
            estado: 'ACTIVO'
        });
    };

    if (loading) return <div className="loading">Cargando sistema de asignaciones...</div>;

    return (
        <div className="container">
            <div className="card">
                <h2>{editingId ? 'Editar Turno' : 'Nueva Asignación de Turno'}</h2>

                {error && <div className="error" style={{ whiteSpace: 'pre-line' }}>{error}</div>}
                {success && <div className="success">{success}</div>}

                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                        <div className="form-group">
                            <label>Contrato:</label>
                            <select name="contrato_id" value={formData.contrato_id} onChange={handleInputChange} required>
                                <option value="">Seleccione Contrato</option>
                                {contratos.map(c => <option key={c.id} value={c.id}>ID: {c.id} (Empresa {c.empresa?.nombre})</option>)}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Servicio:</label>
                            <select name="servicio_id" value={formData.servicio_id} onChange={handleInputChange} required>
                                <option value="">Seleccione Servicio</option>
                                {servicios.map(s => <option key={s.id} value={s.id}>{s.nombre}</option>)}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Empleado:</label>
                            <select name="empleado_id" value={formData.empleado_id} onChange={handleInputChange} required>
                                <option value="">Seleccione Empleado</option>
                                {empleados.map(e => <option key={e.id} value={e.id}>{e.nombre} {e.apellido}</option>)}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Espacio:</label>
                            <select name="espacio_id" value={formData.espacio_id} onChange={handleInputChange} required>
                                <option value="">Seleccione Espacio</option>
                                {espacios.map(esp => <option key={esp.id} value={esp.id}>{esp.nombre} ({esp.empresa_nombre})</option>)}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Fecha Inicio:</label>
                            <input type="date" name="fecha_inicio" value={formData.fecha_inicio} onChange={handleInputChange} required />
                        </div>

                        <div className="form-group">
                            <label>Fecha Fin (Opcional):</label>
                            <input type="date" name="fecha_fin" value={formData.fecha_fin} onChange={handleInputChange} />
                        </div>

                        <div className="form-group">
                            <label>Hora Inicio:</label>
                            <input type="time" name="hora_inicio" value={formData.hora_inicio} onChange={handleInputChange} required />
                        </div>

                        <div className="form-group">
                            <label>Hora Fin:</label>
                            <input type="time" name="hora_fin" value={formData.hora_fin} onChange={handleInputChange} required />
                        </div>

                        <div className="form-group">
                            <label>Frecuencia:</label>
                            <select name="frecuencia" value={formData.frecuencia} onChange={handleInputChange}>
                                <option value="DIARIO">Diario</option>
                                <option value="SEMANAL">Semanal</option>
                                <option value="UNICA">Única vez</option>
                            </select>
                        </div>
                    </div>

                    <div className="button-group" style={{ marginTop: '20px' }}>
                        <button type="submit" className="btn btn-primary">{editingId ? 'Actualizar' : 'Asignar Turno'}</button>
                        {editingId && <button type="button" className="btn btn-secondary" onClick={resetForm}>Cancelar</button>}
                    </div>
                </form>
            </div>

            <div className="card">
                <h2>Calendario de Asignaciones</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Empleado</th>
                            <th>Servicio/Espacio</th>
                            <th>Horario</th>
                            <th>Fechas</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {asignaciones.length === 0 ? (
                            <tr><td colSpan="7" style={{ textAlign: 'center' }}>No hay asignaciones registradas</td></tr>
                        ) : (
                            asignaciones.map((asig) => (
                                <tr key={asig.id}>
                                    <td>{asig.id}</td>
                                    <td>{asig.empleado_nombre}</td>
                                    <td>
                                        <strong>{asig.servicio_nombre}</strong><br />
                                        <small>{asig.espacio_nombre}</small>
                                    </td>
                                    <td>
                                        {asig.hora_inicio.substring(0, 5)} - {asig.hora_fin.substring(0, 5)}<br />
                                        <small>{asig.frecuencia}</small>
                                    </td>
                                    <td>
                                        Del: {asig.fecha_inicio.split('T')[0]}<br />
                                        {asig.fecha_fin ? `Al: ${asig.fecha_fin.split('T')[0]}` : '(Indefinido)'}
                                    </td>
                                    <td>{asig.estado}</td>
                                    <td>
                                        <button className="btn btn-edit" onClick={() => handleEdit(asig)}>Editar</button>
                                        <button className="btn btn-danger" onClick={() => handleDelete(asig.id)} style={{ marginLeft: '5px' }}>X</button>
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

export default AsignacionView;
