/**
 * Componente principal de la aplicación - Tier 1: Presentación
 * Maneja la navegación entre diferentes vistas (MVC)
 */
import React, { useState } from 'react';
import EmpresaView from './views/EmpresaView';
import ServicioView from './views/ServicioView';
import ContratoView from './views/ContratoView';
import EmpleadoView from './views/EmpleadoView';
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
      case 'empleados':
        return <EmpleadoView />;
      default:
        return <EmpresaView />;
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Servicios de Limpieza para Empresas</h1>
        <p>Sistema de gestión de servicios de limpieza - Arquitectura Cliente-Servidor y 3 Capas</p>

        <nav className="nav" aria-label="Navegación principal">
          <button
            type="button"
            className={currentView === 'empresas' ? 'active' : ''}
            onClick={() => setCurrentView('empresas')}
          >
            Empresas
          </button>

          <button
            type="button"
            className={currentView === 'servicios' ? 'active' : ''}
            onClick={() => setCurrentView('servicios')}
          >
            Servicios
          </button>

          <button
            type="button"
            className={currentView === 'contratos' ? 'active' : ''}
            onClick={() => setCurrentView('contratos')}
          >
            Contratos
          </button>

          <button
            type="button"
            className={currentView === 'empleados' ? 'active' : ''}
            onClick={() => setCurrentView('empleados')}
          >
            Empleados
          </button>
        </nav>
      </header>

      <main>
        {renderView()}
      </main>
    </div>
  );
}

export default App;
