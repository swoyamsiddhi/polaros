import React, { createContext, useContext, useState } from 'react';

export type ViewState = 
  | 'LANDING' 
  | 'LOGIN' 
  | 'COMMAND_HOME' 
  | 'EXPEDITIONS' 
  | 'EXPEDITION_DETAIL' 
  | 'INVENTORY' 
  | 'SHIPMENTS' 
  | 'ASSETS' 
  | 'PERSONNEL' 
  | 'STATIONS' 
  | 'PLANNER'
  | 'MISSION_MODE' 
  | 'DEBRIEF' 
  | 'POLAR_EXPLORER';

export type Role = 'COMMANDER' | 'LOGISTICS' | 'TRAINER' | 'STUDENT';

interface AppState {
  currentView: ViewState;
  activeExpedition: string | null;
  activeRole: Role;
  setCurrentView: (view: ViewState) => void;
  setActiveExpedition: (id: string | null) => void;
  setActiveRole: (role: Role) => void;
}

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentView, setCurrentView] = useState<ViewState>('LANDING');
  const [activeExpedition, setActiveExpedition] = useState<string | null>(null);
  const [activeRole, setActiveRole] = useState<Role>('COMMANDER');

  return (
    <AppContext.Provider value={{ currentView, activeExpedition, activeRole, setCurrentView, setActiveExpedition, setActiveRole }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
