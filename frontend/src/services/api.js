/**
 * Cliente API - Tier 1: Presentación
 * Servicio para comunicación HTTP con el backend (Tier 2)
 */
import axios from 'axios';

// Lee la URL de la API en tiempo de ejecución desde window.API_URL (definido en public/config.js)
const getApiUrl = () => {
  if (typeof window !== 'undefined' && window.API_URL) {
    return window.API_URL;
  }
  return 'http://localhost:5001/api';
};

const api = axios.create({
  baseURL: getApiUrl(),
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

// Facturas API
export const facturasAPI = {
  getAll: () => api.get('/facturas'),
  getById: (id) => api.get(`/facturas/${id}`),
  getByEmpresa: (empresaId) => api.get(`/facturas/empresa/${empresaId}`),
  create: (data) => api.post('/facturas', data),
  update: (id, data) => api.put(`/facturas/${id}`, data),
  delete: (id) => api.delete(`/facturas/${id}`),
};

export default api;


