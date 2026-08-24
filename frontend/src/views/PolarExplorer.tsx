import { useState } from 'react';
import { useAppContext } from '../AppContext';
import { Map as MapIcon, GraduationCap } from 'lucide-react';

export default function PolarExplorer() {
  const { setCurrentView } = useAppContext();
  const [activeStation, setActiveStation] = useState<string | null>(null);

  return (
    <div className="flex flex-col h-full gap-6 max-w-5xl mx-auto w-full">
      <div className="flex justify-between items-center border-b-4 border-black pb-2">
        <h2 className="text-3xl font-pixel-heading text-3d m-0 flex items-center gap-2">
          <MapIcon size={32} /> POLAR EXPLORER
        </h2>
        <span className="bg-pixel-primary text-white px-2 py-1 text-xs">STUDENT MODE</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-grow">
        
        {/* Interactive Map */}
        <div className="pixel-panel bg-blue-900 border-4 border-black relative overflow-hidden flex flex-col items-center justify-center p-8 min-h-[400px]">
          <div className="absolute inset-0 scanlines opacity-30 pointer-events-none"></div>
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-20"></div>
          
          <h3 className="absolute top-4 left-4 text-white font-bold text-xl tracking-widest border-b-2 border-white">ANTARCTICA</h3>

          <div className="relative w-full max-w-sm aspect-square flex flex-col items-center justify-center">
            
            <button 
              onClick={() => setActiveStation('MAITRI')}
              className={`absolute top-1/4 left-1/3 flex flex-col items-center transform transition-transform hover:scale-110 ${activeStation === 'MAITRI' ? 'animate-bounce' : ''}`}
            >
              <div className="w-4 h-4 bg-white rounded-full border-2 border-black"></div>
              <span className="text-white font-bold text-sm mt-1 bg-black px-1">MAITRI</span>
            </button>

            <button 
              onClick={() => setActiveStation('BHARATI')}
              className={`absolute bottom-1/3 right-1/4 flex flex-col items-center transform transition-transform hover:scale-110 ${activeStation === 'BHARATI' ? 'animate-bounce' : ''}`}
            >
              <div className="w-4 h-4 bg-white rounded-full border-2 border-black"></div>
              <span className="text-white font-bold text-sm mt-1 bg-black px-1">BHARATI</span>
            </button>

          </div>
        </div>

        {/* Info Panel */}
        <div className="flex flex-col gap-4">
          {activeStation ? (
            <div className="pixel-panel flex-grow flex flex-col animate-fade-in">
              <h3 className="text-3xl font-pixel-heading text-pixel-primary mb-6">🧊 {activeStation}</h3>
              
              <div className="mb-6">
                <div className="text-xs text-gray-500 font-bold mb-1 tracking-widest">WHERE</div>
                <div className="text-lg">{activeStation === 'BHARATI' ? 'Larsemann Hills, Antarctica' : 'Schirmacher Oasis, Antarctica'}</div>
              </div>

              <div className="mb-6">
                <div className="text-xs text-gray-500 font-bold mb-1 tracking-widest">WHY IT MATTERS</div>
                <div className="text-lg">Indian scientific research in Antarctica.</div>
              </div>

              <div className="mb-6">
                <div className="text-xs text-gray-500 font-bold mb-1 tracking-widest">WHAT HAPPENS HERE</div>
                <ul className="text-lg flex flex-col gap-2">
                  <li>🔬 Science</li>
                  <li>🌨️ Weather observations</li>
                  <li>🧊 Cryosphere research</li>
                  <li>🌊 Ocean studies</li>
                </ul>
              </div>

              <div className="mt-auto bg-blue-50 border-2 border-pixel-primary p-4">
                <div className="text-sm font-bold text-pixel-primary mb-2 flex items-center gap-2">
                  <GraduationCap size={16} /> LEARNING MISSION
                </div>
                <p className="italic mb-4">"Prepare a 30-day research expedition to {activeStation}."</p>
                <button 
                  onClick={() => setCurrentView('MISSION_MODE')}
                  className="pixel-btn pixel-btn-primary w-full"
                >
                  [ START LEARNING MISSION ]
                </button>
              </div>
            </div>
          ) : (
            <div className="pixel-panel flex-grow flex items-center justify-center text-center text-gray-500 border-dashed">
              <div className="max-w-xs">
                <MapIcon size={48} className="mx-auto mb-4 opacity-50" />
                <p>Select a station on the map to explore its history, purpose, and logistics.</p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
