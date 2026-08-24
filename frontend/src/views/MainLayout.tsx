import { useAppContext } from '../AppContext';
import { Terminal, Database as DbIcon, Activity, Target, Gamepad2, Navigation, AlertTriangle, Cpu, Rocket, Users, Box, Ship, Map, Settings, BarChart } from 'lucide-react';

import CommandHome from './CommandHome';
import ExpeditionsList from './ExpeditionsList';
import ExpeditionDetail from './ExpeditionDetail';
import Database from './Database'; 
import Planner from './Planner';
import MissionMode from './MissionMode';
import Debrief from './Debrief';
import PolarExplorer from './PolarExplorer';

export default function MainLayout() {
  const { currentView, setCurrentView, activeRole } = useAppContext();

  const handleNav = (view: any) => {
    setCurrentView(view);
  };

  const NavButton = ({ view, icon: Icon, label, alert = false }: any) => (
    <button 
      onClick={() => handleNav(view)}
      className={`flex items-center gap-3 px-4 py-3 w-full text-left font-pixel text-xs transition-none border-4 ${
        currentView === view 
          ? 'bg-blue-900 border-black text-white' 
          : alert 
            ? 'border-transparent text-pixel-danger hover:bg-red-900/50' 
            : 'border-transparent text-gray-800 hover:bg-gray-300 hover:text-black'
      }`}
    >
      <Icon size={16} className={alert ? 'animate-pulse' : ''} /> {label}
    </button>
  );

  return (
    <div className="flex h-screen bg-gray-200 text-black font-pixel overflow-hidden">
      
      {/* Sidebar */}
      <div className="w-64 bg-gray-300 border-r-4 border-black flex flex-col z-20">
        
        <div className="p-6 border-b-4 border-black bg-blue-900 text-white">
          <h1 className="font-bold text-xl flex items-center gap-2 text-3d m-0">
            <Terminal size={24} /> POLAR OPS
          </h1>
          <div className="text-[10px] mt-2 bg-black text-white inline-block px-2 py-1 border-2 border-white">
            ROLE: {activeRole}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto py-4 flex flex-col gap-4 custom-scrollbar">
          
          {/* COMMAND SECTION */}
          {activeRole !== 'STUDENT' && (
            <div>
              <div className="text-[10px] text-gray-500 mb-2 px-6 font-bold">COMMAND</div>
              <NavButton view="COMMAND_HOME" icon={Activity} label="Command Center" />
            </div>
          )}

          {/* OPERATIONS SECTION */}
          {activeRole !== 'STUDENT' && (
            <div>
              <div className="text-[10px] text-gray-500 mb-2 px-6 font-bold">OPERATIONS</div>
              <NavButton view="EXPEDITIONS" icon={Rocket} label="Expeditions" />
              <NavButton view="INVENTORY" icon={Box} label="Inventory" />
              <NavButton view="SHIPMENTS" icon={Ship} label="Shipments" />
              <NavButton view="ASSETS" icon={DbIcon} label="Assets" />
              <NavButton view="PERSONNEL" icon={Users} label="Personnel" />
              <NavButton view="STATIONS" icon={Map} label="Stations" />
            </div>
          )}

          {/* INTELLIGENCE SECTION */}
          {activeRole !== 'STUDENT' && (
            <div>
              <div className="text-[10px] text-gray-500 mb-2 px-6 font-bold">INTELLIGENCE</div>
              <NavButton view="PLANNER" icon={Navigation} label="Smart Planner" />
              <button className="flex items-center gap-3 px-4 py-3 w-full text-left font-pixel text-xs border-4 border-transparent text-gray-500 cursor-not-allowed">
                <Target size={16} /> Risk Center
              </button>
            </div>
          )}

          {/* MISSIONS SECTION */}
          <div>
            <div className="text-[10px] text-gray-500 mb-2 px-6 font-bold">MISSIONS</div>
            <NavButton view="MISSION_MODE" icon={Gamepad2} label="Mission Mode" />
          </div>

          {/* EXPLORE SECTION */}
          <div>
            <div className="text-[10px] text-gray-500 mb-2 px-6 font-bold">EXPLORE</div>
            <NavButton view="POLAR_EXPLORER" icon={Map} label="Polar Explorer" />
          </div>

          <div className="mt-auto pt-4 border-t-4 border-black">
            <NavButton view="EXPEDITION_DETAIL" icon={AlertTriangle} label="7 ALERTS ACTIVE" alert={true} />
            <button 
              onClick={() => setCurrentView('LANDING')}
              className="flex items-center gap-3 px-4 py-3 w-full text-left font-pixel text-xs text-gray-600 hover:text-black border-4 border-transparent hover:bg-gray-400"
            >
              <Settings size={16} /> LOGOUT
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-hidden flex flex-col relative bg-gray-200">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-10 pointer-events-none z-0"></div>
        
        {/* Global Snow Effect */}
        <div className="pixel-snow-layer pixel-snow-1"></div>
        <div className="pixel-snow-layer pixel-snow-2"></div>
        <div className="pixel-snow-layer pixel-snow-3"></div>

        <div className="h-full overflow-auto relative z-10 p-6 md:p-10 custom-scrollbar">
          {currentView === 'COMMAND_HOME' && <CommandHome />}
          {currentView === 'EXPEDITIONS' && <ExpeditionsList />}
          {currentView === 'EXPEDITION_DETAIL' && <ExpeditionDetail />}
          
          {(currentView === 'INVENTORY' || currentView === 'ASSETS' || currentView === 'PERSONNEL' || currentView === 'STATIONS' || currentView === 'SHIPMENTS') && <Database />}
          {currentView === 'PLANNER' && <Planner />}
          
          {currentView === 'MISSION_MODE' && <MissionMode />}
          {currentView === 'DEBRIEF' && <Debrief />}
          {currentView === 'POLAR_EXPLORER' && <PolarExplorer />}
        </div>
      </div>
    </div>
  );
}
