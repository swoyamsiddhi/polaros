import { useState } from 'react';
import { useAppContext } from '../AppContext';
import { Trophy, Shield, Clock, Crosshair, CloudLightning } from 'lucide-react';

export default function MissionMode() {
  const { setCurrentView } = useAppContext();
  const [missionState, setMissionState] = useState<'HUB' | 'PLAYING' | 'EVENT' | 'SUCCESS'>('HUB');
  const [score, setScore] = useState(6420);
  const [time, setTime] = useState('18:42');

  const handleAction = (points: number, message: string) => {
    setScore(prev => prev + points);
    alert(`ACTION: ${message}. Score updated.`);
  };

  if (missionState === 'SUCCESS') {
    return (
      <div className="flex flex-col items-center justify-center h-full bg-gray-200 text-black p-4 font-pixel">
        <div className="border-4 border-black bg-white p-8 max-w-md w-full text-center relative shadow-[8px_8px_0px_rgba(0,0,0,1)]">
          <div className="absolute top-0 right-0 bg-pixel-success text-white px-2 py-1 text-xs font-bold font-pixel">GRADE A</div>
          <h2 className="text-3xl font-pixel-heading text-pixel-success mb-2">MISSION COMPLETE</h2>
          <div className="text-6xl font-pixel-heading mb-2">{score}</div>
          <div className="text-gray-500 mb-6 tracking-widest text-sm">TOTAL SCORE</div>
          
          <div className="text-pixel-warning text-2xl mb-6">⭐⭐⭐⭐⭐</div>

          <div className="text-sm text-left mx-auto flex flex-col gap-2 mb-8 bg-gray-100 p-4 border-2 border-black">
             <div className="font-bold border-b-2 border-black pb-1 mb-2 text-pixel-success">SUCCESSFUL DECISIONS</div>
             <div className="text-pixel-success flex justify-between"><span>Prioritised medical cargo</span> <span>+500</span></div>
             <div className="text-pixel-success flex justify-between"><span>Maintained fuel reserve</span> <span>+200</span></div>
             <div className="text-pixel-success flex justify-between"><span>Selected appropriate transport</span> <span>+150</span></div>
             
             <div className="font-bold border-b-2 border-black pb-1 mb-2 mt-4 text-pixel-danger">IMPROVEMENT AREAS</div>
             <div className="text-pixel-danger flex justify-between"><span>Asset utilisation</span> <span>-100</span></div>
          </div>

          <div className="border-4 border-pixel-warning bg-yellow-50 p-4 mb-8">
            <div className="text-pixel-warning font-bold text-sm mb-2 flex justify-center items-center gap-2">
              <Trophy size={16} /> BADGE UNLOCKED
            </div>
            <div className="text-xl font-bold">WEATHER COMMANDER</div>
          </div>

          <div className="flex gap-4">
            <button 
              onClick={() => setMissionState('HUB')}
              className="pixel-btn bg-gray-200 text-black w-full"
            >
              [ REPLAY ]
            </button>
            <button 
              onClick={() => setCurrentView('COMMAND_HOME')}
              className="pixel-btn pixel-btn-primary w-full"
            >
              [ RETURN TO COMMAND ]
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (missionState === 'EVENT') {
    return (
      <div className="flex flex-col items-center justify-center h-full bg-black text-white p-4 relative font-pixel">
        <div className="absolute inset-0 scanlines opacity-50 pointer-events-none"></div>
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20 pointer-events-none"></div>
        
        <div className="border-4 border-pixel-danger bg-red-950 p-8 max-w-lg w-full relative z-10 shadow-[8px_8px_0px_rgba(255,0,0,1)]">
          <h2 className="text-3xl font-pixel-heading text-pixel-danger mb-2 text-center flex justify-center items-center gap-4">
            <CloudLightning size={32} className="animate-pulse" /> WEATHER EVENT
          </h2>
          
          <h3 className="text-2xl font-bold mb-4 text-center bg-pixel-danger text-white py-1 border-2 border-white">WHITEOUT DETECTED</h3>
          
          <div className="bg-black border-2 border-gray-700 p-4 mb-8 text-center">
            <p className="text-pixel-warning mb-2 font-bold">Aircraft operations suspended for 6 hours.</p>
            <p className="text-sm text-gray-400">Current fuel burn rate indicates Camp Alpha will reach critical stockout before aircraft arrives.</p>
          </div>
          
          <div className="mb-4 text-sm text-white font-bold">CHOOSE RESPONSE:</div>
          <div className="flex flex-col gap-4">
            <button onClick={() => handleAction(-200, 'Waited for aircraft')} className="pixel-btn border-2 border-gray-500 text-left px-4 bg-gray-900 hover:bg-gray-800 flex justify-between">
              <span>[A] WAIT FOR AIRCRAFT</span>
              <span className="text-xs text-gray-400">Low cost, High delay</span>
            </button>
            <button 
              onClick={() => setMissionState('SUCCESS')}
              className="pixel-btn border-2 border-pixel-primary text-left px-4 bg-blue-900 hover:bg-blue-800 flex justify-between"
            >
              <span>[B] DEPLOY SNOW VEHICLE</span>
              <span className="text-xs text-cyan-300">Higher fuel, Faster delivery</span>
            </button>
            <button onClick={() => setMissionState('HUB')} className="pixel-btn border-2 border-pixel-danger text-left px-4 bg-red-900 hover:bg-red-800 flex justify-between">
              <span>[C] ABORT MISSION</span>
              <span className="text-xs text-red-300">Safest, Mission Failure</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (missionState === 'PLAYING') {
    return (
      <div className="flex flex-col h-full bg-black text-white font-pixel border-8 border-gray-800">
        
        {/* GAME HUD */}
        <div className="flex justify-between items-center border-b-4 border-gray-700 bg-gray-900 p-4">
          <div>
            <div className="text-gray-500 text-xs">MISSION:</div>
            <h2 className="text-xl font-bold text-pixel-primary">WHITEOUT RESUPPLY</h2>
          </div>
          
          <div className="flex gap-8 text-sm">
            <div className="flex flex-col items-center">
              <span className="text-gray-500 text-xs">SCORE</span>
              <span className="font-bold">{score}</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-gray-500 text-xs">XP</span>
              <span className="font-bold text-pixel-success">+850</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-gray-500 text-xs">TIME</span>
              <span className="font-bold">{time}</span>
            </div>
            <div className="flex flex-col items-center bg-red-950 px-4 border border-pixel-danger">
              <span className="text-pixel-danger text-xs">RISK</span>
              <span className="font-bold text-pixel-danger animate-pulse">HIGH</span>
            </div>
          </div>
        </div>

        {/* MISSION MAP */}
        <div className="flex-grow flex flex-col items-center justify-center relative bg-[#050b14]">
          <div className="absolute inset-0 scanlines opacity-30 pointer-events-none"></div>
          
          <div className="absolute top-1/3 text-center w-full bg-red-900/20 py-8 border-y-2 border-pixel-danger/30">
            <div className="text-4xl mb-2 animate-pulse">🌨️ 🌨️ 🌨️</div>
            <div className="text-pixel-danger tracking-widest font-bold">SEVERE WEATHER ZONE</div>
          </div>

          <pre className="font-pixel text-xs sm:text-sm md:text-base leading-loose text-center z-10 text-cyan-100">
{`          🏢 BHARATI STATION
               |
               |  (Route A)
               |
           [ 🚁 AIRCRAFT ]
               |
               X  (Blocked)
               |
          🏕️ FIELD CAMP ALPHA`}
          </pre>
          
          {/* Action Trigger */}
          <button 
            onClick={() => setMissionState('EVENT')} 
            className="absolute right-10 top-1/2 -translate-y-1/2 pixel-btn bg-pixel-danger text-white animate-pulse"
          >
            [ FAST FORWARD TIME ]
          </button>
        </div>

        {/* RESOURCE PANEL */}
        <div className="border-t-4 border-gray-700 bg-gray-900 p-4">
          <div className="flex justify-between text-lg mb-4 px-4 bg-black border-2 border-gray-800 p-2">
            <span className="flex items-center gap-2"><span className="text-gray-500">FUEL:</span> ⛽ 2,800L</span>
            <span className="flex items-center gap-2"><span className="text-gray-500">VEHICLES:</span> 🚙 2</span>
            <span className="flex items-center gap-2"><span className="text-gray-500">AIRCRAFT:</span> 🚁 1</span>
            <span className="flex items-center gap-2"><span className="text-gray-500">CARGO:</span> 📦 4,200kg</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <button className="pixel-btn border-2 border-gray-600 bg-black hover:bg-gray-800 transition-colors">[ DEPLOY AIRCRAFT ]</button>
            <button className="pixel-btn border-2 border-gray-600 bg-black hover:bg-gray-800 transition-colors">[ DEPLOY SNOW VEHICLE ]</button>
            <button className="pixel-btn border-2 border-gray-600 bg-black hover:bg-gray-800 transition-colors">[ TRANSFER FUEL ]</button>
            <button className="pixel-btn border-2 border-pixel-danger bg-red-950 text-pixel-danger hover:bg-pixel-danger hover:text-white transition-colors">[ ABORT MISSION ]</button>
          </div>
        </div>
      </div>
    );
  }

  // HUB STATE
  return (
    <div className="flex flex-col h-full gap-6 font-pixel">
      <div className="flex justify-between items-center border-b-4 border-black pb-4">
        <h2 className="text-3xl font-pixel-heading text-3d m-0">MISSION COMMAND</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Player Profile */}
        <div className="pixel-panel border-black bg-white md:col-span-1 flex flex-col gap-6">
          <div className="text-center border-b-2 border-gray-200 pb-4">
            <div className="w-24 h-24 bg-gray-200 border-4 border-black mx-auto mb-4 flex items-center justify-center overflow-hidden">
               {/* Pixel art avatar placeholder */}
               <div className="w-16 h-16 bg-blue-900 rounded-full relative">
                 <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-white"></div>
                 <div className="absolute top-1/4 right-1/4 w-3 h-3 bg-white"></div>
                 <div className="absolute bottom-1/4 left-1/4 right-1/4 h-2 bg-white"></div>
               </div>
            </div>
            <h3 className="font-bold text-xl">COMMANDER LEVEL 05</h3>
            <div className="flex justify-between items-center mt-4 bg-gray-100 p-2 border-2 border-black">
              <span className="font-bold">XP:</span>
              <span className="text-pixel-primary">4,820 / 6,000</span>
            </div>
            <div className="w-full bg-gray-300 h-2 mt-1 border border-black">
              <div className="bg-pixel-primary h-full w-[80%]"></div>
            </div>
          </div>

          <div>
            <h4 className="font-bold mb-4 flex items-center gap-2 border-b-2 border-black pb-1"><Shield size={16} /> EARNED BADGES</h4>
            <div className="flex flex-col gap-3 text-sm">
              <div className="flex items-center gap-3 bg-green-50 border-2 border-pixel-success p-2">
                <Trophy size={20} className="text-pixel-success" />
                <div>
                  <div className="font-bold text-pixel-success">Zero Stockout</div>
                  <div className="text-xs text-gray-600">No critical shortages.</div>
                </div>
              </div>
              <div className="flex items-center gap-3 bg-blue-50 border-2 border-pixel-primary p-2">
                <Shield size={20} className="text-pixel-primary" />
                <div>
                  <div className="font-bold text-pixel-primary">Asset Guardian</div>
                  <div className="text-xs text-gray-600">Protected all equipment.</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mission Selection */}
        <div className="md:col-span-2 flex flex-col gap-6">
          <h3 className="font-bold text-xl">AVAILABLE CAMPAIGNS</h3>
          
          <div className="pixel-panel border-black bg-blue-900 text-white relative overflow-hidden group">
            <div className="absolute inset-0 scanlines opacity-30 pointer-events-none"></div>
            <div className="absolute top-0 right-0 bg-pixel-danger px-4 py-1 font-bold border-b-4 border-l-4 border-black">HARD</div>
            
            <h4 className="text-2xl font-bold mb-2 relative z-10">WHITEOUT RESUPPLY</h4>
            <div className="flex items-center gap-4 text-sm text-cyan-300 mb-6 relative z-10 font-bold">
              <span className="flex items-center gap-1"><Clock size={14} /> 15 MINS</span>
              <span className="flex items-center gap-1"><Crosshair size={14} /> ANTARCTICA</span>
            </div>
            
            <div className="bg-black/50 border-2 border-black p-4 mb-6 relative z-10">
              <div className="text-gray-400 text-xs mb-1">OBJECTIVE</div>
              <p>Deliver critical fuel to Field Camp Alpha before stockout occurs during severe weather event.</p>
            </div>
            
            <div className="flex justify-between items-center relative z-10">
              <div className="font-bold text-pixel-success">REWARD: +1200 XP</div>
              <button 
                onClick={() => setMissionState('PLAYING')}
                className="pixel-btn bg-white text-black border-4 border-black group-hover:bg-pixel-primary group-hover:text-white group-hover:border-white transition-colors"
              >
                [ BEGIN MISSION ]
              </button>
            </div>
          </div>

          <div className="pixel-panel border-gray-400 bg-gray-200 text-gray-500 relative cursor-not-allowed">
            <div className="absolute top-0 right-0 bg-gray-400 text-white px-4 py-1 font-bold">LOCKED</div>
            <h4 className="text-xl font-bold mb-2">GLACIER CREVASSE RESCUE</h4>
            <p className="text-sm mb-4">Requires Commander Level 06</p>
            <div className="bg-gray-300 border-2 border-gray-400 p-4 opacity-50">
              <p>Emergency medical evacuation under extreme terrain constraints.</p>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
