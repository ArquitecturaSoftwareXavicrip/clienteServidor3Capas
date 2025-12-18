import React, { useState, useEffect } from 'react';
import { espaciosAPI, empresasAPI } from '../services/api';

const EspacioView = () => {
    const [espacios, setEspacios] = useState([]);
    const [empresas, setEmpresas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [editingId, setEditingId] = useState(null);
    const [formData, setFormData] = useState({
        nombre: '',
        tipo: '',
        empresa_id: '',
        observaciones: ''
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [espaciosRes, empresasRes] = await Promise.all([
                espaciosAPI.getAll(),
                empresasAPI.getAll()
            ]);
            setEspacios(espaciosRes.data);
            setEmpresas(empresasRes.data);
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
                empresa_id: parseInt(formData.empresa_id) // Ensure ID is int
            };

            if (editingId) {
                await espaciosAPI.update(editingId, dataToSend);
                setSuccess('Espacio actualizado correctamente');
            } else {
                await espaciosAPI.create(dataToSend);
                setSuccess('Espacio creado correctamente');
            }

            resetForm();
            // Reload only espacios to keep UI snappy, empresas rarely change
            const res = await espaciosAPI.getAll();
            setEspacios(res.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Error al guardar espacio');
        }
    };

    const handleEdit = (espacio) => {
        setEditingId(espacio.id);
        setFormData({
            nombre: espacio.nombre,
            tipo: espacio.tipo,
            empresa_id: espacio.empresa_id,
            observaciones: espacio.observaciones || ''
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Está seguro de eliminar este espacio?')) {
            return;
        }

        try {
            setError(null);
            await espaciosAPI.delete(id);
            setSuccess('Espacio eliminado correctamente');
            const res = await espaciosAPI.getAll();
            setEspacios(res.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Error al eliminar espacio');
        }
    };

    const resetForm = () => {
        setEditingId(null);
        setFormData({
            nombre: '',
            tipo: '',
            empresa_id: '',
            observaciones: ''
        });
    };

    if (loading) {
        return <div className="loading">Cargando espacios...</div>;
    }

    return (
        <div className="container">
            <div className="card">
                <h2>{editingId ? 'Editar Espacio' : 'Nuevo Espacio'}</h2>

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
                            {empresas.map(emp => (
                                <option key={emp.id} value={emp.id}>{emp.nombre}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Nombre del Espacio (ej. Piso 2):</label>
                        <input
                            type="text"
                            name="nombre"
                            value={formData.nombre}
                            onChange={handleInputChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Tipo (ej. Oficina, Hall, Baño):</label>
                        <input
                            type="text"
                            name="tipo"
                            value={formData.tipo}
                            onChange={handleInputChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Observaciones:</label>
                        <textarea
                            name="observaciones"
                            value={formData.observaciones}
                            onChange={handleInputChange}
                            rows="3"
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
                <h2>Lista de Espacios</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Empresa</th>
                            <th>Nombre</th>
                            <th>Tipo</th>
                            <th>Observaciones</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {espacios.length === 0 ? (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center' }}>
                                    No hay espacios registrados
                                </td>
                            </tr>
                        ) : (
                            espacios.map((espacio) => (
                                <tr key={espacio.id}>
                                    <td>{espacio.id}</td>
                                    <td>{espacio.empresa_nombre}</td>
                                    <td>{espacio.nombre}</td>
                                    <td>{espacio.tipo}</td>
                                    <td>{espacio.observaciones}</td>
                                    <td>
                                        <button
                                            className="btn btn-edit"
                                            onClick={() => handleEdit(espacio)}
                                            style={{ marginRight: '5px' }}
                                        >
                                            Editar
                                        </button>
                                        <button
                                            className="btn btn-danger"
                                            onClick={() => handleDelete(espacio.id)}
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

export default EspacioView;
