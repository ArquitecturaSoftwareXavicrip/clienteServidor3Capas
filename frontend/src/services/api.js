/**
 * Cliente API - Tier 1: Presentación
 * Servicio para comunicación HTTP con el backend (Tier 2)
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Empresas API
export const empresasAPI = {
  getAll: () => api.get('/empresas'),
  getById: (id) => api.get(`/empresas/${id}`),
  create: (data) => api.post('/empresas', data),
  update: (id, data) => api.put(`/empresas/${id}`, data),
  delete: (id) => api.delete(`/empresas/${id}`),
};

// Servicios API
export const serviciosAPI = {
  getAll: () => api.get('/servicios'),
  getById: (id) => api.get(`/servicios/${id}`),
  create: (data) => api.post('/servicios', data),
  update: (id, data) => api.put(`/servicios/${id}`, data),
  delete: (id) => api.delete(`/servicios/${id}`),
};

// Contratos API
export const contratosAPI = {
  getAll: () => api.get('/contratos'),
  getById: (id) => api.get(`/contratos/${id}`),
  create: (data) => api.post('/contratos', data),
  update: (id, data) => api.put(`/contratos/${id}`, data),
  delete: (id) => api.delete(`/contratos/${id}`),
};

// Empleados API
export const empleadosAPI = {
  getAll: () => api.get('/empleados'),
  getById: (id) => api.get(`/empleados/${id}`),
  create: (data) => api.post('/empleados', data),
  update: (id, data) => api.put(`/empleados/${id}`, data),
  delete: (id) => api.delete(`/empleados/${id}`),
};

// Espacios API
export const espaciosAPI = {
  getAll: () => api.get('/espacios'),
  getByEmpresa: (empresaId) => api.get(`/espacios?empresa_id=${empresaId}`),
  getById: (id) => api.get(`/espacios/${id}`),
  create: (data) => api.post('/espacios', data),
  update: (id, data) => api.put(`/espacios/${id}`, data),
  delete: (id) => api.delete(`/espacios/${id}`),
};

// Asignaciones API
export const asignacionesAPI = {
  getAll: () => api.get('/asignaciones'),
  getById: (id) => api.get(`/asignaciones/${id}`),
  create: (data) => api.post('/asignaciones', data),
  update: (id, data) => api.put(`/asignaciones/${id}`, data),
  delete: (id) => api.delete(`/asignaciones/${id}`),
};

export default api;


