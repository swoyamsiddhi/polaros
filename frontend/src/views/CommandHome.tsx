import { useAppContext } from '../AppContext';
import { Rocket, AlertTriangle, Cpu } from 'lucide-react';

export default function CommandHome() {
  const { setCurrentView, setActiveExpedition } = useAppContext();

  const handleAlertClick = () => {
    setActiveExpedition('EXP-2026-014');
    setCurrentView('EXPEDITION_DETAIL');
  };

  return (
    <div className="flex flex-col h-full gap-6">

      {/* Header Stats */}
      <div className="flex justify-between items-center border-b-4 border-black pb-4">
        <div>
          <h2 className="text-3xl font-pixel-heading text-3d m-0">ACTIVE OPERATIONS</h2>
          <div className="text-sm font-bold flex gap-4 mt-2">
            <span>08 Expeditions</span>
            <span>23 Shipments</span>
            <span>142 Assets</span>
            <span className="text-pixel-danger animate-pulse">07 Critical Alerts</span>
          </div>
        </div>
        <div className="text-right">
          <h3 className="text-xl font-pixel-heading text-gray-400">SYSTEM STATUS</h3>
          <div className="text-pixel-success font-bold">NOMINAL</div>
        </div>
      </div>

      {/* Polar Map */}
      <div className="pixel-panel flex-grow flex flex-col relative overflow-hidden bg-blue-900 border-4 border-black min-h-[300px]">
        <h3 className="text-white z-10 mb-4 bg-black inline-block px-2 border-2 border-white">POLAR MAP</h3>
        <div className="absolute inset-0 scanlines opacity-30 pointer-events-none z-10"></div>
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-20"></div>

        <pre className="text-white font-pixel text-xs sm:text-sm md:text-base leading-relaxed z-10 p-4">
          {`             🧊 MAITRI
                 ●
                  ╲
                   ╲ 🚢
                    ╲
                 🧊 BHARATI ───────── 🚁 ───── 🏕️ CAMP ALPHA

                         🌨️ WEATHER ZONE`}
        </pre>
      </div>

      {/* Bottom Action Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="pixel-panel border-pixel-primary">
          <h3 className="border-b-2 border-black pb-1 mb-2 flex items-center gap-2 font-bold">
            <Rocket size={16} /> ACTIVE MISSION
          </h3>
          <div className="text-xl mb-1">WHITEOUT RESUPPLY</div>
          <div className="text-sm text-pixel-danger mb-4">Risk: 72%</div>
          <button
            onClick={() => setCurrentView('MISSION_MODE')}
            className="pixel-btn pixel-btn-primary w-full text-xs"
          >
            [CONTINUE MISSION]
          </button>
        </div>

        <div className="pixel-panel border-pixel-danger animate-pulse">
          <h3 className="border-b-2 border-black pb-1 mb-2 flex items-center gap-2 font-bold text-pixel-danger">
            <AlertTriangle size={16} /> CRITICAL ALERT
          </h3>
          <div className="text-xl mb-1">Fuel shortage</div>
          <div className="text-sm mb-4">S-204 delayed</div>
          <button
            onClick={handleAlertClick}
            className="pixel-btn bg-pixel-danger text-white hover:bg-red-700 w-full text-xs transition-none"
          >
            [VIEW ALERTS]
          </button>
        </div>

        <div className="pixel-panel border-pixel-warning">
          <h3 className="border-b-2 border-black pb-1 mb-2 flex items-center gap-2 font-bold text-yellow-700">
            <Cpu size={16} /> AI RECOMMENDATION
          </h3>
          <div className="text-xl mb-1">Bring shipment</div>
          <div className="text-sm mb-4">forward by 24h</div>
          <button
            onClick={() => setCurrentView('PLANNER')}
            className="pixel-btn bg-pixel-warning text-black w-full text-xs"
          >
            [ANALYZE]
          </button>
        </div>

      </div>

    </div>
  );
}
