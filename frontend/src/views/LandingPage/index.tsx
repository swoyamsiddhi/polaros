import { useState } from 'react';
import { useAppContext } from '../../AppContext';
import { Terminal, Lock, Map, Database, Cpu, Navigation, Rocket } from 'lucide-react';

export default function LandingPage() {
  const { setCurrentView, setActiveRole } = useAppContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = (e: React.FormEvent, role: 'COMMANDER' | 'LOGISTICS' | 'TRAINER' | 'STUDENT') => {
    e.preventDefault();
    setLoading(true);
    setActiveRole(role);
    
    // Simulate auth
    setTimeout(() => {
      setLoading(false);
      setCurrentView('COMMAND_HOME');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-200 text-black font-pixel relative">
      
      {/* Global Snow Effect */}
      <div className="pixel-snow-layer pixel-snow-1"></div>
      <div className="pixel-snow-layer pixel-snow-2"></div>
      <div className="pixel-snow-layer pixel-snow-3"></div>

      {/* HEADER */}
      <header className="border-b-4 border-black bg-blue-900 p-4 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex justify-between items-center text-white">
          <div className="flex items-center gap-2">
            <Terminal size={24} />
            <span className="font-pixel-heading text-xl md:text-2xl tracking-wider text-3d m-0">POLAR OPS COMMANDER</span>
          </div>
          <div className="hidden md:flex gap-6 text-sm font-bold">
            <a href="#about" className="hover:text-pixel-primary">ABOUT</a>
            <a href="#network" className="hover:text-pixel-primary">NETWORK</a>
            <a href="#features" className="hover:text-pixel-primary">SYSTEMS</a>
          </div>
        </div>
      </header>

      {/* STATUS TICKER */}
      <div className="bg-black text-pixel-success py-2 border-b-4 border-black overflow-hidden relative z-10 font-bold border-t-4 border-gray-400">
        <div className="flex gap-12 whitespace-nowrap animate-[marquee_20s_linear_infinite]">
          <span>MAITRI: -24°C, WIND 45KNOTS</span>
          <span>•</span>
          <span>BHARATI: -12°C, CLEAR</span>
          <span>•</span>
          <span>SHIPMENT S-204: DELAYED</span>
          <span>•</span>
          <span>ACTIVE EXPEDITIONS: 08</span>
          <span>•</span>
          <span>SYSTEM LOAD: 14%</span>
          <span>•</span>
          <span>MAITRI: -24°C, WIND 45KNOTS</span>
          <span>•</span>
          <span>BHARATI: -12°C, CLEAR</span>
        </div>
      </div>

      {/* HERO SECTION */}
      <section className="py-20 px-4 relative overflow-hidden bg-gray-300 border-b-4 border-black">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-20 pointer-events-none"></div>
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center relative z-10">
          
          <div className="flex flex-col gap-6">
            <div className="inline-block bg-black text-white px-3 py-1 text-xs border-2 border-white w-max font-bold">
              SIH26062 — MoES / NCPOR
            </div>
            <h1 className="text-4xl md:text-6xl font-pixel-heading leading-tight text-3d m-0">
              PLAN. TRACK.<br/>PREDICT.<br/>RESPOND.<br/>
              <span className="text-pixel-primary">EXPLORE.</span>
            </h1>
            <p className="text-lg md:text-xl border-l-4 border-black pl-4 py-2 font-bold bg-white/50">
              Integrated Polar Expedition Logistics, Asset Management & Mission-Based Learning Platform.
            </p>
            <div className="flex flex-col gap-2 mt-4 text-sm font-bold bg-gray-200 p-4 border-2 border-black max-w-sm">
               <div className="text-pixel-danger flex items-center gap-2">► LIVE DATA SYNC: ACTIVE</div>
               <div className="text-pixel-primary flex items-center gap-2">► AI RISK ENGINE: ONLINE</div>
            </div>
          </div>

          {/* LOGIN PANEL */}
          <div className="pixel-panel bg-white p-8 border-black shadow-[8px_8px_0px_rgba(0,0,0,1)]">
            <div className="flex items-center gap-2 mb-6 border-b-2 border-black pb-2">
              <Lock size={20} />
              <h2 className="text-2xl font-bold m-0">SYSTEM ACCESS</h2>
            </div>
            
            <form className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-bold mb-1">AUTHORIZATION ID</label>
                <input 
                  type="text" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-gray-100 border-2 border-black p-3 font-pixel outline-none focus:border-pixel-primary"
                  placeholder="commander@ncpor.gov.in"
                />
              </div>
              <div>
                <label className="block text-sm font-bold mb-1">PASSCODE</label>
                <input 
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-gray-100 border-2 border-black p-3 font-pixel outline-none focus:border-pixel-primary"
                  placeholder="••••••••"
                />
              </div>
            </form>

            <div className="text-xs text-gray-500 font-bold mb-2">QUICK DEMO ACCESS (SELECT ROLE)</div>
            <div className="grid grid-cols-2 gap-2">
              <button 
                onClick={(e) => handleLogin(e, 'COMMANDER')}
                disabled={loading}
                className="pixel-btn pixel-btn-primary w-full text-xs py-2 hover:-translate-y-1"
              >
                {loading ? '...' : '[ COMMANDER ]'}
              </button>
              <button 
                onClick={(e) => handleLogin(e, 'LOGISTICS')}
                disabled={loading}
                className="pixel-btn bg-gray-200 w-full text-xs py-2 hover:-translate-y-1"
              >
                {loading ? '...' : '[ LOGISTICS ]'}
              </button>
              <button 
                onClick={(e) => handleLogin(e, 'TRAINER')}
                disabled={loading}
                className="pixel-btn bg-gray-200 w-full text-xs py-2 hover:-translate-y-1"
              >
                {loading ? '...' : '[ TRAINER ]'}
              </button>
              <button 
                onClick={(e) => {
                  e.preventDefault();
                  setActiveRole('STUDENT');
                  setCurrentView('POLAR_EXPLORER');
                }}
                disabled={loading}
                className="pixel-btn bg-black text-white w-full text-xs py-2 hover:-translate-y-1"
              >
                {loading ? '...' : '[ STUDENT ]'}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* NETWORK MAP PREVIEW */}
      <section id="network" className="py-20 px-4 bg-gray-300 relative z-10 border-b-4 border-black overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-20 pointer-events-none"></div>
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <h2 className="text-4xl font-pixel-heading mb-4 text-3d m-0">GLOBAL POLAR NETWORK</h2>
          <p className="max-w-2xl mx-auto mb-12 font-bold text-gray-700 text-lg">
            Real-time tracking of expeditions, stations, and cargo across Antarctica and the Himalayas.
          </p>

          <div className="pixel-panel bg-blue-900 border-black p-4 relative overflow-hidden h-[500px] flex flex-col items-center justify-center shadow-[12px_12px_0px_rgba(0,0,0,1)]">
             <div className="absolute inset-0 scanlines opacity-30 pointer-events-none"></div>
             
             {/* Fake Pixel Map */}
             <div className="relative w-full h-full flex flex-col items-center justify-center text-white">
                <div className="text-6xl md:text-8xl mb-4 opacity-30 font-bold tracking-[2rem] text-center">ANTARCTICA</div>
                
                <div className="absolute top-[20%] left-[20%] text-center">
                  <div className="w-6 h-6 bg-pixel-primary border-4 border-white mx-auto animate-pulse"></div>
                  <div className="text-xs font-bold mt-2 bg-black px-2 py-1 border-2 border-white">MAITRI STATION</div>
                  <div className="text-[10px] text-gray-300 mt-1">Schirmacher Oasis</div>
                </div>

                <div className="absolute bottom-[30%] right-[25%] text-center">
                  <div className="w-6 h-6 bg-pixel-success border-4 border-white mx-auto animate-pulse"></div>
                  <div className="text-xs font-bold mt-2 bg-black px-2 py-1 border-2 border-white">BHARATI STATION</div>
                  <div className="text-[10px] text-gray-300 mt-1">Larsemann Hills</div>
                </div>

                <div className="absolute top-[50%] left-[45%] text-center opacity-70">
                  <div className="w-4 h-4 bg-pixel-warning border-2 border-white mx-auto animate-bounce"></div>
                  <div className="text-[10px] font-bold mt-1 bg-black px-1 border border-white text-pixel-warning">EXP-2026-013</div>
                </div>
             </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="py-20 px-4 bg-gray-300 border-b-4 border-black relative z-10 overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-20 pointer-events-none"></div>
        <div className="max-w-6xl mx-auto relative z-10">
          <h2 className="text-4xl font-pixel-heading mb-12 text-center text-3d m-0">SYSTEM MODULES</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="pixel-panel bg-white p-8 border-black hover:-translate-y-2 transition-transform shadow-[8px_8px_0px_rgba(0,0,0,1)]">
              <Database size={48} className="mb-4 text-pixel-primary" />
              <h3 className="text-xl font-bold mb-4 border-b-2 border-black pb-2">INTEGRATED LOGISTICS</h3>
              <p className="text-sm text-gray-700 font-bold leading-relaxed mb-4">Track inventory, spare parts, and critical fuel across all stations with predictive burn-rate analysis.</p>
              <ul className="text-xs text-gray-500 font-bold space-y-2">
                 <li>► Automated Stock Alerts</li>
                 <li>► Asset Lifecycle Tracking</li>
                 <li>► Shipment Delay Propagation</li>
              </ul>
            </div>
            
            <div className="pixel-panel bg-white p-8 border-black hover:-translate-y-2 transition-transform shadow-[8px_8px_0px_rgba(0,0,0,1)]">
              <Cpu size={48} className="mb-4 text-pixel-danger" />
              <h3 className="text-xl font-bold mb-4 border-b-2 border-black pb-2">AI RISK ENGINE</h3>
              <p className="text-sm text-gray-700 font-bold leading-relaxed mb-4">Continuous analysis of weather, cargo delays, and asset health to predict and mitigate mission risks.</p>
              <ul className="text-xs text-gray-500 font-bold space-y-2">
                 <li>► Weather Impact Prediction</li>
                 <li>► Compound Risk Scoring</li>
                 <li>► Automated Threat Detection</li>
              </ul>
            </div>

            <div className="pixel-panel bg-white p-8 border-black hover:-translate-y-2 transition-transform shadow-[8px_8px_0px_rgba(0,0,0,1)]">
              <Navigation size={48} className="mb-4 text-pixel-warning" />
              <h3 className="text-xl font-bold mb-4 border-b-2 border-black pb-2">DECISION PLANNER</h3>
              <p className="text-sm text-gray-700 font-bold leading-relaxed mb-4">Generate alternate routes and strategies during critical events like whiteouts or fuel shortages.</p>
              <ul className="text-xs text-gray-500 font-bold space-y-2">
                 <li>► Plan A/B/C Comparisons</li>
                 <li>► Cost vs. Speed Analysis</li>
                 <li>► Mission Simulation Testing</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* GAMIFICATION CALLOUT */}
      <section className="py-20 px-4 bg-black text-white relative overflow-hidden border-t-4 border-black z-10">
         <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-30 pointer-events-none"></div>
         <div className="max-w-4xl mx-auto text-center relative z-10">
            <h2 className="text-3xl md:text-5xl font-pixel-heading mb-6 text-pixel-success">TRAIN THE NEXT GENERATION</h2>
            <p className="text-lg mb-8 text-gray-400 font-bold leading-relaxed">
              Polar Ops Commander isn't just an operational tool—it's a mission-based learning platform. 
              Students and trainees can enter "Mission Mode" to simulate real-world logistics crises, earn XP, and unlock badges based on their decisions.
            </p>
            <button 
              onClick={() => {
                setActiveRole('STUDENT');
                setCurrentView('POLAR_EXPLORER');
              }}
              className="pixel-btn pixel-btn-success text-xl px-8 py-4 animate-bounce"
            >
              [ ENTER STUDENT MODE ]
            </button>
         </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-gray-900 text-white py-12 px-4 border-t-4 border-gray-600 relative z-10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6 text-xs font-bold">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2 text-lg">
              <Terminal size={20} /> POLAR OPS COMMANDER v1.0
            </div>
            <div className="text-gray-500">
              Developed for Smart India Hackathon 2026
            </div>
          </div>
          <div className="text-right text-gray-500 flex flex-col gap-2">
            <div>Ministry of Earth Sciences (MoES)</div>
            <div>National Centre for Polar and Ocean Research (NCPOR)</div>
            <div>Problem Statement: SIH26062</div>
          </div>
        </div>
      </footer>
    </div>
  );
}
