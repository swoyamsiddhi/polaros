import { motion } from 'framer-motion';
import { AlertTriangle, Cpu } from 'lucide-react';
import { useAppContext } from '../../../AppContext';

export default function LiveMissionPreview() {
  const { setCurrentView } = useAppContext();

  return (
    <section id="missions" className="bg-[#010205] py-32 relative overflow-hidden border-y border-white/5">
      
      {/* Background cinematic fog/particles */}
      <div className="absolute inset-0 z-0">
        <motion.div 
          animate={{ x: [0, -100, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]"
        ></motion.div>
        <div className="absolute top-0 right-0 w-1/2 h-full bg-red-900/10 blur-[150px]"></div>
      </div>

      <div className="max-w-7xl mx-auto px-6 relative z-10 flex flex-col lg:flex-row gap-16 items-center">
        
        {/* Left text */}
        <div className="w-full lg:w-1/2">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <div className="text-red-500 font-mono tracking-widest text-sm mb-4">LIVE MISSION PREVIEW</div>
            <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-8">MISSION 04 <br/><span className="text-gray-500 font-light">WHITEOUT RESUPPLY</span></h2>
            
            <div className="space-y-6 text-gray-400 font-mono text-sm max-w-md">
              <div>
                <span className="text-white block mb-1">Situation:</span>
                Field Camp Alpha has critically low fuel.
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-white block mb-1">Resources:</span>
                  1 Aircraft<br/>2 Snow Vehicles<br/>Limited Cargo<br/>Limited Fuel
                </div>
                <div>
                  <span className="text-white block mb-1">Weather:</span>
                  <span className="text-red-500">SEVERE</span>
                </div>
              </div>
            </div>
            
          </motion.div>
        </div>

        {/* Right UI Preview */}
        <div className="w-full lg:w-1/2">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-black border border-gray-800 p-8 shadow-2xl relative"
          >
            {/* The Game HUD Mockup */}
            <div className="flex justify-between items-start mb-12">
              <div className="font-mono text-sm space-y-1">
                <div className="text-cyan-400">FUEL <span className="text-white ml-2">2,800 L</span></div>
                <div className="text-cyan-400">TIME <span className="text-white ml-2">06:42</span></div>
              </div>
              <div className="border border-red-500 bg-red-950/30 px-3 py-1 font-mono text-red-500 text-sm animate-pulse">
                RISK 72%
              </div>
            </div>

            {/* Visual Route */}
            <div className="relative h-40 mb-12 flex flex-col justify-between items-center text-center font-mono">
              <div className="text-white">BHARATI</div>
              <motion.div 
                animate={{ y: [0, 10, 0] }} 
                transition={{ duration: 2, repeat: Infinity }}
                className="text-gray-500"
              >
                ↓<br/>🚁<br/>↓
              </motion.div>
              <div className="text-white bg-red-950/50 border border-red-900 px-4 py-1">
                🌨 WHITEOUT
              </div>
              <motion.div 
                animate={{ y: [0, 10, 0] }} 
                transition={{ duration: 2, repeat: Infinity }}
                className="text-gray-500"
              >
                ↓
              </motion.div>
              <div className="text-gray-400">🏕 CAMP ALPHA</div>
            </div>

            {/* Event Injection */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5 }}
              className="border-l-4 border-amber-500 bg-amber-950/30 p-4 mb-6"
            >
              <div className="flex items-center gap-2 text-amber-500 font-bold mb-1">
                <AlertTriangle size={16} /> EVENT DETECTED
              </div>
              <div className="text-white text-sm">"Aircraft delayed by 6 hours."</div>
            </motion.div>

            {/* AI Recommendation */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 1 }}
              className="border-l-4 border-cyan-500 bg-cyan-950/30 p-4 mb-8"
            >
              <div className="flex items-center gap-2 text-cyan-400 font-bold mb-1 font-mono text-xs">
                <Cpu size={14} /> SYSTEM RECOMMENDATION
              </div>
              <div className="text-white text-sm">"Dispatch Snow Vehicle B"</div>
            </motion.div>

            {/* Buttons */}
            <div className="grid grid-cols-2 gap-4">
              <button className="border border-white/20 text-white font-mono text-xs py-3 hover:bg-white/5 transition-colors">
                [ SIMULATE DECISION ]
              </button>
              <button 
                onClick={() => setCurrentView('LOGIN')}
                className="bg-white text-black font-mono font-bold text-xs py-3 hover:bg-gray-200 transition-colors"
              >
                [ ENTER MISSION MODE ]
              </button>
            </div>
          </motion.div>
        </div>

      </div>
    </section>
  );
}
