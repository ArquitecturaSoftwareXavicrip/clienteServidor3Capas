/**
 * Configuración de la aplicación
 * Lee la URL de la API desde window.API_URL (cargado en tiempo de ejecución desde public/config.js)
 */

// URL de la API del Backend
// Se carga en tiempo de ejecución desde public/config.js
const API_URL = 
  (typeof window !== 'undefined' && window.API_URL) || 
  'http://localhost:5001/api';

console.log('API URL configurada:', API_URL);

export const config = {
  API_URL: API_URL,
};

export default config;
