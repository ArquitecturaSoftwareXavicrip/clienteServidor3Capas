/**
 * Componente principal de la aplicación - Tier 1: Presentación
 * Maneja la navegación entre diferentes vistas (MVC)
 */
import React, { useState } from 'react';
// Asegúrate de que las rutas a los archivos sean correctas según tu estructura de carpetas
import EmpresaView from './views/EmpresaView';
import ServicioView from './views/ServicioView';
import ContratoView from './views/ContratoView';
import EmpleadoView from './views/EmpleadoView'; // <--- Tu nueva vista
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('empresas');

  const renderView = () => {
    switch (currentView) {
      case 'empresas':
        return <EmpresaView />;
      case 'servicios':
        return <ServicioView />;
      case 'contratos':
        return <ContratoView />;
      case 'empleados':   // <--- CORREGIDO: Ahora está antes del default
        return <EmpleadoView />;
      default:            // <--- El default siempre va al final
        return <EmpresaView />;
    }
  };

  return (
    <div className="App">
      <div className="header">
        <h1>Servicios de Limpieza para Empresas</h1>
        <p>Sistema de gestión de servicios de limpieza - Arquitectura Cliente-Servidor y 3 Capas</p>
        
        {/* Barra de Navegación */}
        <div className="nav">
          <button
            className={currentView === 'empresas' ? 'active' : ''}
            onClick={() => setCurrentView('empresas')}
          >
            Empresas
          </button>
          
          <button
            className={currentView === 'servicios' ? 'active' : ''}
            onClick={() => setCurrentView('servicios')}
          >
            Servicios
          </button>
          
          <button
            className={currentView === 'contratos' ? 'active' : ''}
            onClick={() => setCurrentView('contratos')}
          >
            Contratos
          </button>
          
          <button
            className={currentView === 'empleados' ? 'active' : ''}
            onClick={() => setCurrentView('empleados')}
          >
            Empleados
          </button>
        </div>
      </div>

      {/* Área de contenido dinámico */}
      <div className="content-area">
        {renderView()}
      </div>
    </div>
  );
}

export default App;