import { useState, useEffect } from 'react';
import { Gamepad2, Play, TerminalSquare, AlertTriangle, Shield, CheckCircle, Flame, Navigation, Clock } from 'lucide-react';

export default function MissionControl() {
  const [missions, setMissions] = useState<any[]>([]);
  const [activeInstance, setActiveInstance] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [debrief, setDebrief] = useState<any>(null);

  const fetchMissions = () => {
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/missions`)
      .then(res => res.json())
      .then(data => {
        setMissions(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMissions();
  }, []);

  const startMission = (missionId: number) => {
    setLoading(true);
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/simulation/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mission_id: missionId, user_id: 1 })
    })
    .then(res => res.json())
    .then(data => {
      fetchInstance(data.instance_id);
    });
  };

  const fetchInstance = (instanceId: number) => {
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/simulation/${instanceId}`)
      .then(res => res.json())
      .then(data => {
        setActiveInstance(data);
        setLoading(false);
        setActionLoading(false);
        
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          fetchDebrief(instanceId);
        }
      });
  };

  const fetchDebrief = (instanceId: number) => {
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/simulation/${instanceId}/debrief`)
      .then(res => res.json())
      .then(data => {
        setDebrief(data);
      });
  };

  const performAction = (action: string, choice?: string) => {
    setActionLoading(true);
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/simulation/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        instance_id: activeInstance.id,
        action,
        choice
      })
    })
    .then(() => {
      // Small delay to simulate processing
      setTimeout(() => {
        fetchInstance(activeInstance.id);
      }, 500);
    });
  };

  if (loading && !activeInstance) return <div className="text-2xl animate-pulse">INITIALIZING_SIMULATOR...</div>;

  // Render Mission Selection
  if (!activeInstance) {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-end border-b-4 border-black pb-2">
          <h2 className="text-4xl font-pixel-heading text-3d m-0 flex items-center gap-2 mb-4"><Gamepad2 size={32} /> SIMULATION_ENVIRONMENT</h2>
          <span className="text-sm bg-black text-pixel-success px-2 py-1 pixel-panel-inset animate-pulse">READY</span>
        </div>
        
        <p className="text-xl">Select a scenario to begin logistics training:</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
          {missions.map(mission => (
            <div key={mission.id} className="pixel-panel flex flex-col justify-between h-full hover:-translate-y-1 hover:-translate-x-1 transition-transform border-b-4 border-r-4 border-black active:translate-y-0 active:translate-x-0 cursor-pointer" onClick={() => startMission(mission.id)}>
              <div>
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs bg-black text-white px-2 py-1">{mission.code}</span>
                  <span className={`text-xs px-2 py-1 text-white ${
                    mission.difficulty === 'HARD' || mission.difficulty === 'EXTREME' ? 'bg-pixel-danger' : 
                    mission.difficulty === 'MEDIUM' ? 'bg-pixel-warning' : 'bg-pixel-success'
                  }`}>{mission.difficulty}</span>
                </div>
                <h3 className="text-lg font-pixel-heading mb-2 leading-tight">{mission.name}</h3>
                <p className="text-sm mb-4 leading-tight">{mission.description}</p>
                
                <div className="bg-[#dfdfdf] p-2 text-xs mb-4">
                  <div className="font-bold mb-1">OBJECTIVES:</div>
                  <ul className="list-disc pl-4">
                    {mission.objectives.map((obj: string, i: number) => <li key={i}>{obj}</li>)}
                  </ul>
                </div>
              </div>
              
              <button className="pixel-btn pixel-btn-primary w-full flex items-center justify-center gap-2">
                <Play size={16} /> LAUNCH_SCENARIO
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Render Debrief
  if (debrief) {
    return (
      <div className="flex flex-col gap-4 max-w-4xl mx-auto">
        <div className={`pixel-panel border-4 ${activeInstance.status === 'COMPLETED' ? 'border-pixel-success bg-[#eeffee]' : 'border-pixel-danger bg-[#ffeeee]'}`}>
          <h2 className="text-4xl text-3d font-pixel-heading text-center mb-4 mt-2">MISSION_{activeInstance.status}</h2>
          <div className="text-center text-4xl mb-6 font-bold">{debrief.score.total} PTS</div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 text-center">
            <div className="bg-white p-2 border-2 border-black">
              <div className="text-xs text-gray-500">SAFETY</div>
              <div className="text-xl">{debrief.score.safety}%</div>
            </div>
            <div className="bg-white p-2 border-2 border-black">
              <div className="text-xs text-gray-500">EFFICIENCY</div>
              <div className="text-xl">{debrief.score.efficiency}%</div>
            </div>
            <div className="bg-white p-2 border-2 border-black">
              <div className="text-xs text-gray-500">ACCURACY</div>
              <div className="text-xl">{debrief.score.accuracy}%</div>
            </div>
            <div className="bg-white p-2 border-2 border-black">
              <div className="text-xs text-gray-500">RESOURCES</div>
              <div className="text-xl">{debrief.score.resource_usage}%</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="border-b-2 border-black mb-2 text-pixel-success">SUCCESSES</h3>
              <ul className="list-none text-sm space-y-1">
                {debrief.successes.map((s: string, i: number) => (
                  <li key={i} className="flex gap-2"><CheckCircle size={16} className="text-pixel-success flex-shrink-0"/> {s}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="border-b-2 border-black mb-2 text-pixel-danger">AREAS_FOR_IMPROVEMENT</h3>
              <ul className="list-none text-sm space-y-1">
                {debrief.improvements.map((s: string, i: number) => (
                  <li key={i} className="flex gap-2"><AlertTriangle size={16} className="text-pixel-danger flex-shrink-0"/> {s}</li>
                ))}
              </ul>
            </div>
          </div>

          {debrief.badges_earned && debrief.badges_earned.length > 0 && (
            <div className="mt-6">
              <h3 className="border-b-2 border-black mb-2 text-center text-pixel-primary">BADGES_EARNED</h3>
              <div className="flex justify-center gap-4">
                {debrief.badges_earned.map((b: any, i: number) => (
                  <div key={i} className="pixel-panel text-center p-2 bg-[#fffbd1] border-yellow-500 animate-bounce">
                    <div className="text-3xl mb-1">{b.icon}</div>
                    <div className="text-xs font-bold">{b.name}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="mt-8 text-center">
            <button onClick={() => {setActiveInstance(null); setDebrief(null);}} className="pixel-btn">RETURN_TO_MENU</button>
          </div>
        </div>
      </div>
    );
  }

  // Active Mission Simulation
  const state = activeInstance.state;
  const currentEvent = activeInstance.events && activeInstance.events.length > 0 ? activeInstance.events[activeInstance.events.length - 1] : null;

  return (
    <div className="flex flex-col h-full gap-4 relative">
      {/* Top HUD */}
      <div className="pixel-panel flex justify-between items-center py-2 px-4 bg-black text-pixel-success border-4 border-black shadow-[inset_4px_4px_0_0_rgba(255,255,255,0.2)] font-pixel text-xl">
        <div className="flex gap-6">
          <div className="flex items-center gap-2"><Clock size={20} /> {state.time_remaining}H_REMAINING</div>
          <div className="flex items-center gap-2 text-yellow-400"><Flame size={20} /> FUEL: {state.fuel}L</div>
        </div>
        <div className="flex gap-6">
          <div className="flex items-center gap-2 text-blue-400"><Navigation size={20} /> CARGO: {state.cargo_delivered}/{state.cargo_target}</div>
          <div className="flex items-center gap-2 text-red-400"><Shield size={20} /> SAFETY: {state.safety}%</div>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 h-full min-h-0">
        
        {/* Main View Screen */}
        <div className="flex-grow pixel-panel relative flex items-center justify-center bg-[#8b8b8b] overflow-hidden">
          {/* Faux retro background effect */}
          <div className="absolute inset-0 scanlines opacity-50 pointer-events-none"></div>
          
          <div className="z-10 w-full max-w-2xl px-4">
            
            {/* Briefing Phase */}
            {activeInstance.phase === 'BRIEFING' && (
              <div className="bg-black text-green-400 p-6 border-4 border-green-600 shadow-2xl font-pixel text-xl">
                <div className="animate-pulse mb-4 text-center">--- INCOMING_TRANSMISSION ---</div>
                <h3 className="text-2xl text-white mb-4 text-center">{activeInstance.mission_name}</h3>
                <p className="mb-6 leading-relaxed typing-effect">Commander, we have a situation requiring your immediate attention. Review the parameters and begin resource allocation when ready.</p>
                <div className="text-center">
                  <button 
                    onClick={() => performAction('start')} 
                    disabled={actionLoading}
                    className="pixel-btn bg-green-700 text-white border-white hover:bg-green-600">
                    {actionLoading ? 'PROCESSING...' : 'ACKNOWLEDGE & START'}
                  </button>
                </div>
              </div>
            )}

            {/* Decision Event Phase */}
            {activeInstance.phase === 'DECISION' && currentEvent && !currentEvent.player_choice && (
              <div className="bg-[#aa0000] text-white p-4 border-4 border-black shadow-2xl">
                <div className="flex items-center gap-2 mb-2 text-yellow-300 font-pixel-heading text-lg">
                  <AlertTriangle className="animate-pulse"/> {currentEvent.title}
                </div>
                <p className="text-xl mb-6 font-pixel leading-snug">{currentEvent.description}</p>
                
                <div className="flex flex-col gap-3">
                  {currentEvent.options.map((opt: any) => (
                    <button 
                      key={opt.id}
                      disabled={actionLoading}
                      onClick={() => performAction('make_decision', opt.id)}
                      className="pixel-btn bg-[#c3c3c3] text-black text-left hover:bg-white active:bg-gray-400 p-3 font-pixel text-xl border-4 border-black shadow-[inset_-2px_-2px_0px_0px_rgba(0,0,0,0.3)]">
                      {opt.id}. {opt.text}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Normal Execution Phase */}
            {activeInstance.phase === 'EXECUTING' && (
              <div className="text-center">
                <div className="text-6xl mb-4 text-white font-pixel-heading animate-pulse">EN_ROUTE</div>
                <div className="text-xl text-black bg-[#dfdfdf] p-2 inline-block border-2 border-black">
                  TURN {activeInstance.turn} COMPLETE
                </div>
                <div className="mt-8">
                  <button 
                    disabled={actionLoading}
                    onClick={() => performAction('continue')}
                    className="pixel-btn pixel-btn-primary text-xl px-8 py-4 animate-bounce">
                    {actionLoading ? 'CALCULATING...' : 'PROCEED_TO_NEXT_TURN >>'}
                  </button>
                </div>
              </div>
            )}

          </div>
        </div>

        {/* Sidebar Event Log */}
        <div className="w-full lg:w-80 pixel-panel flex flex-col flex-shrink-0">
          <h3 className="text-sm font-bold border-b-2 border-black pb-1 flex items-center gap-2"><TerminalSquare size={16}/> EVENT_LOG</h3>
          <div className="flex-grow overflow-auto p-2 bg-black text-[#0f0] font-pixel text-lg mt-2 shadow-[inset_2px_2px_0px_0px_rgba(0,0,0,0.8)]">
            <div className="opacity-50 mb-2">INIT_SEQUENCE_START...</div>
            <div className="opacity-50 mb-2">MISSION_LOADED: {activeInstance.mission_name}</div>
            
            {activeInstance.events && activeInstance.events.map((e: any, i: number) => (
              <div key={i} className="mb-4">
                <div className="text-yellow-400">&gt; {e.title} [TURN {e.turn}]</div>
                {e.player_choice && (
                  <div className="pl-4 text-white opacity-80 mt-1">&gt; Action selected: {e.player_choice}</div>
                )}
                {e.outcome && e.player_choice && (
                  <div className="pl-4 text-cyan-400 mt-1">&gt; Impact: {Object.keys(e.outcome).map(k => `${k}(${e.outcome[k]})`).join(' ')}</div>
                )}
              </div>
            ))}
            {actionLoading && <div className="animate-pulse">&gt; PROCESSING...</div>}
            <div className="animate-blink font-bold mt-2">_</div>
          </div>
        </div>

      </div>
    </div>
  );
}
