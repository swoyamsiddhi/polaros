import { useAppContext } from '../AppContext';
import { AlertTriangle, Activity, ArrowLeft } from 'lucide-react';

export default function ExpeditionDetail() {
  const { activeExpedition, setCurrentView } = useAppContext();

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto gap-6">
      
      {/* Header */}
      <div className="flex items-center gap-4 border-b-4 border-black pb-4 bg-white pixel-panel">
        <button 
          onClick={() => setCurrentView('EXPEDITIONS')}
          className="pixel-btn bg-gray-200 px-2 py-1"
        >
          <ArrowLeft size={20} />
        </button>
        <div>
          <h2 className="text-3xl font-pixel-heading text-3d m-0">Emergency Fuel Drop</h2>
          <div className="text-sm font-bold text-gray-500 mt-1">{activeExpedition || 'EXP-2026-014'}</div>
        </div>
        <div className="ml-auto text-right">
          <div className="text-sm font-bold text-gray-500 mb-1">READINESS</div>
          <div className="text-2xl font-pixel-heading text-pixel-danger">65%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 flex-grow">
        
        {/* Left Col: Core details */}
        <div className="md:col-span-2 flex flex-col gap-6">
          <div className="pixel-panel border-pixel-primary bg-white p-6">
            <h3 className="font-bold mb-4 border-b-2 border-black pb-2 text-xl">CRITICAL PATH</h3>
            <div className="flex items-center justify-between font-pixel text-sm text-black">
              <div className="text-center">
                <div>BHARATI</div>
                <div className="text-xs text-pixel-success mt-1">SECURE</div>
              </div>
              <div className="text-gray-400">------&gt;</div>
              <div className="text-center bg-red-100 border-2 border-pixel-danger px-4 py-2">
                <div>WHITEOUT</div>
                <div className="text-xs text-pixel-danger mt-1">SEVERE</div>
              </div>
              <div className="text-gray-400">------&gt;</div>
              <div className="text-center text-gray-500">
                <div>CAMP ALPHA</div>
                <div className="text-xs mt-1">PENDING</div>
              </div>
            </div>
          </div>

          <div className="pixel-panel border-black bg-white p-6 flex-grow">
            <h3 className="font-bold mb-4 border-b-2 border-black pb-2 text-xl">INVENTORY CHECKLIST</h3>
            
            <div className="space-y-6 font-pixel text-sm">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="font-bold">Aviation Fuel (ATF)</span>
                  <span className="text-pixel-danger font-bold">2,400L / 10,000L</span>
                </div>
                <div className="w-full bg-gray-200 border-2 border-black h-4">
                  <div className="bg-pixel-danger h-full w-[24%] border-r-2 border-black"></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="font-bold">Arctic Rations</span>
                  <span className="text-pixel-primary font-bold">140 / 150</span>
                </div>
                <div className="w-full bg-gray-200 border-2 border-black h-4">
                  <div className="bg-pixel-primary h-full w-[93%] border-r-2 border-black"></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="font-bold">Medical Kits</span>
                  <span className="text-pixel-success font-bold">10 / 10</span>
                </div>
                <div className="w-full bg-gray-200 border-2 border-black h-4">
                  <div className="bg-pixel-success h-full w-[100%] border-r-2 border-black"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: AI & Actions */}
        <div className="flex flex-col gap-6">
          
          {/* AI Risk Engine */}
          <div className="pixel-panel border-pixel-danger bg-red-50 p-6">
            <h3 className="font-bold mb-4 border-b-2 border-pixel-danger pb-2 text-pixel-danger flex items-center gap-2 text-xl">
              <Activity size={18} /> AI RISK ENGINE
            </h3>
            
            <div className="text-4xl font-pixel-heading text-pixel-danger mb-2">72% <span className="text-sm text-gray-500">RISK</span></div>
            <p className="text-sm text-gray-700 mb-4 font-bold">High probability of mission failure due to compounding weather and fuel delays.</p>
            
            <div className="space-y-2 text-sm font-pixel text-gray-600">
              <div className="flex justify-between">
                <span>Weather</span>
                <span className="text-pixel-danger font-bold">+24%</span>
              </div>
              <div className="flex justify-between">
                <span>Fuel Stock</span>
                <span className="text-pixel-danger font-bold">+20%</span>
              </div>
            </div>
          </div>

          <div className="pixel-panel border-black bg-white p-6">
            <h3 className="font-bold mb-4 border-b-2 border-black pb-2 text-xl">COMMAND ACTIONS</h3>
            <div className="space-y-4">
              <button className="pixel-btn w-full text-left pl-4 bg-gray-100">
                [EDIT MANIFEST]
              </button>
              <button className="pixel-btn pixel-btn-primary w-full text-left pl-4 bg-blue-100">
                [VIEW AI RECS]
              </button>
              <button 
                onClick={() => setCurrentView('MISSION_MODE')}
                className="pixel-btn bg-pixel-danger text-white w-full flex items-center justify-between px-4 animate-pulse transition-none"
              >
                <span>[SIMULATE MISSION]</span>
                <AlertTriangle size={16} />
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
