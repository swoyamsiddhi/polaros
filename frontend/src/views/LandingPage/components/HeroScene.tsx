import { motion } from 'framer-motion';
import { useAppContext } from '../../../AppContext';
import { ArrowRight, Activity, Crosshair, AlertTriangle } from 'lucide-react';

export default function HeroScene() {
  const { setCurrentView } = useAppContext();

  return (
    <div className="relative min-h-screen flex items-center overflow-hidden bg-[#02040a]">
      {/* Background Environment Layers */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-[#02040a] via-blue-950/20 to-[#02040a] z-10"></div>
        {/* Subtle grid */}
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 mix-blend-overlay"></div>
        {/* Aurora effect */}
        <motion.div 
          animate={{ opacity: [0.1, 0.3, 0.1], scale: [1, 1.1, 1] }}
          transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
          className="absolute -top-[20%] -left-[10%] w-[70%] h-[70%] bg-emerald-500/10 blur-[150px] rounded-full mix-blend-screen"
        ></motion.div>
        <motion.div 
          animate={{ opacity: [0.1, 0.2, 0.1], scale: [1, 1.2, 1] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear", delay: 2 }}
          className="absolute top-[10%] right-[10%] w-[50%] h-[50%] bg-cyan-600/10 blur-[150px] rounded-full mix-blend-screen"
        ></motion.div>
        
        {/* Stylized Terrain Map (CSS based) */}
        <div className="absolute bottom-0 w-full h-[50vh] bg-gradient-to-t from-cyan-950/20 to-transparent">
           <div className="absolute inset-0 opacity-20" style={{
             backgroundImage: 'linear-gradient(45deg, transparent 48%, rgba(6, 182, 212, 0.5) 49%, rgba(6, 182, 212, 0.5) 51%, transparent 52%)',
             backgroundSize: '40px 40px'
           }}></div>
        </div>
      </div>

      {/* Floating HUD Elements */}
      <div className="absolute inset-0 z-10 pointer-events-none hidden lg:block">
        
        {/* HUD 1: Live Simulation */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 1 }}
          className="absolute top-1/4 right-[15%] border border-cyan-500/30 bg-black/40 backdrop-blur-md p-4 font-mono text-xs text-cyan-500 max-w-[200px]"
        >
          <div className="flex items-center gap-2 border-b border-cyan-500/30 pb-2 mb-2">
            <Activity size={12} className="animate-pulse" />
            <span>LIVE SIMULATION</span>
          </div>
          <div className="text-white mb-1">Bharati Station</div>
          <div className="flex justify-between text-gray-400 mb-1"><span>Readiness</span> <span className="text-white">91%</span></div>
          <div className="flex justify-between text-gray-400"><span>Weather</span> <span className="text-amber-500">SEVERE</span></div>
        </motion.div>

        {/* HUD 2: Shipment */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="absolute bottom-1/3 right-[25%] border border-cyan-500/30 bg-black/40 backdrop-blur-md p-4 font-mono text-xs text-cyan-500 max-w-[200px]"
        >
          <div className="flex items-center gap-2 border-b border-cyan-500/30 pb-2 mb-2 text-white">
            <span>SHIPMENT S-204</span>
          </div>
          <div className="text-gray-400 mb-2">🚢 → ✈ → 🚙</div>
          <div className="flex justify-between text-gray-400 mb-1"><span>STATUS</span> <span className="text-amber-500">DELAYED</span></div>
          <div className="flex justify-between text-gray-400"><span>IMPACT</span> <span className="text-red-500">+06:00</span></div>
        </motion.div>

        {/* HUD 3: Risk */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2, duration: 1 }}
          className="absolute top-1/3 left-[45%] border border-red-500/30 bg-black/40 backdrop-blur-md p-4 font-mono text-xs text-red-500 max-w-[150px]"
        >
          <div className="flex items-center gap-2 border-b border-red-500/30 pb-2 mb-2">
            <AlertTriangle size={12} />
            <span>EXPEDITION RISK</span>
          </div>
          <div className="text-2xl font-bold text-white mb-1">72%</div>
          <div className="text-red-500 animate-pulse">HIGH PRIORITY</div>
        </motion.div>

        {/* Aim Crosshair */}
        <div className="absolute top-1/2 left-2/3 -translate-x-1/2 -translate-y-1/2 opacity-20">
          <Crosshair size={300} strokeWidth={0.5} className="text-cyan-500 animate-spin-slow" />
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 relative z-20 w-full pt-20">
        <div className="max-w-3xl">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <p className="text-cyan-400 font-mono text-xs font-bold tracking-[0.2em] mb-4 flex items-center gap-2">
              <span className="w-4 h-4 rounded-sm bg-cyan-500/20 flex items-center justify-center border border-cyan-500/50"></span>
              MINISTRY OF EARTH SCIENCES | NCPOR • SIH26062
            </p>
            
            <h1 className="text-6xl md:text-8xl lg:text-9xl font-bold text-white leading-[0.9] tracking-tighter mb-4">
              POLAR
              <br />
              <span className="text-4xl md:text-6xl lg:text-7xl text-gray-400 tracking-tight block mt-2">OPS COMMANDER</span>
            </h1>

            <p className="text-lg md:text-xl text-gray-300 font-light max-w-xl mb-6">
              Integrated Polar Expedition Logistics, <br/>Asset Management & Mission-Based Learning.
            </p>

            <div className="flex items-center gap-4 text-sm font-mono tracking-widest text-cyan-300 mb-12">
              <span>PLAN.</span>
              <span className="w-1 h-1 rounded-full bg-cyan-500/50"></span>
              <span>TRACK.</span>
              <span className="w-1 h-1 rounded-full bg-cyan-500/50"></span>
              <span>PREDICT.</span>
              <span className="w-1 h-1 rounded-full bg-cyan-500/50"></span>
              <span>RESPOND.</span>
              <span className="w-1 h-1 rounded-full bg-cyan-500/50"></span>
              <span>EXPLORE.</span>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <button 
              onClick={() => setCurrentView('LOGIN')}
              className="group relative px-8 py-4 bg-white text-black font-bold tracking-widest text-sm flex items-center justify-center gap-3 overflow-hidden"
            >
              <div className="absolute inset-0 bg-cyan-500 -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></div>
              <span className="relative z-10 group-hover:text-white transition-colors duration-300 flex items-center gap-2">
                [ ENTER COMMAND CENTER ] <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
              </span>
            </button>
            
            <button 
              onClick={() => setCurrentView('POLAR_EXPLORER')}
              className="px-8 py-4 bg-white/5 border border-white/20 text-white font-bold tracking-widest text-sm hover:bg-white/10 hover:border-white/40 transition-all duration-300"
            >
              [ EXPLORE POLAR WORLD ]
            </button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
