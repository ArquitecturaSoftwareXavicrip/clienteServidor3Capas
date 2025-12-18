/**
 * Componente principal de la aplicación - Tier 1: Presentación
 * Maneja la navegación entre diferentes vistas (MVC)
 */
import React, { useState } from 'react';
import EmpresaView from './views/EmpresaView';
import ServicioView from './views/ServicioView';
import ContratoView from './views/ContratoView';
import PrestamoView from './views/PrestamoView';

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
      case 'prestamos':
        return <PrestamoView />;
      default:
        return <EmpresaView />;
    }
  };

  return (
    <div className="App">
      <div className="header">
        <h1>Servicios de Limpieza para Empresas</h1>
        <p>Sistema de gestión de servicios de limpieza - Arquitectura Cliente-Servidor y 3 Capas</p>
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
            className={currentView === 'prestamos' ? 'active' : ''} 
            onClick={() => setCurrentView('prestamos')}
          >
            Préstamos Equipos
          </button>
        </div>
      </div>
      {renderView()}
    </div>
  );
}

export default App;


