import { motion } from 'framer-motion';
import { Terminal, Gamepad2, Map } from 'lucide-react';
import { useAppContext } from '../../../AppContext';

export default function ModeCards() {
  const { setCurrentView } = useAppContext();

  return (
    <section id="command" className="bg-[#02040a] py-32 relative">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Card 1: COMMAND MODE */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            whileHover={{ y: -10 }}
            className="group relative border border-gray-800 bg-[#050b14] overflow-hidden flex flex-col h-[500px] transition-all duration-500 hover:border-cyan-500/50 hover:shadow-[0_0_30px_rgba(6,182,212,0.15)]"
          >
            {/* Background Image / Env */}
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10 group-hover:opacity-20 transition-opacity"></div>
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#050b14] z-10"></div>
            
            <div className="relative z-20 p-8 flex flex-col h-full">
              <Terminal size={48} className="text-gray-600 group-hover:text-cyan-400 transition-colors mb-6" />
              <h3 className="text-3xl font-bold text-white tracking-widest mb-2">COMMAND MODE</h3>
              <p className="text-cyan-400 font-mono text-sm tracking-[0.2em] mb-8">"Run the expedition."</p>
              
              <ul className="flex flex-col gap-3 text-gray-400 text-sm font-mono flex-grow">
                <li>[+] Expeditions</li>
                <li>[+] Inventory</li>
                <li>[+] Assets</li>
                <li>[+] Personnel</li>
                <li>[+] Shipments</li>
                <li>[+] Stations</li>
              </ul>

              <button 
                onClick={() => setCurrentView('LOGIN')}
                className="w-full py-4 border border-white/20 text-white font-bold tracking-widest text-sm hover:bg-white hover:text-black transition-colors"
              >
                ENTER COMMAND
              </button>
            </div>
          </motion.div>

          {/* Card 2: MISSION MODE */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            whileHover={{ y: -10 }}
            className="group relative border border-gray-800 bg-[#050b14] overflow-hidden flex flex-col h-[500px] transition-all duration-500 hover:border-red-500/50 hover:shadow-[0_0_30px_rgba(239,68,68,0.15)]"
          >
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-10 group-hover:opacity-30 transition-opacity"></div>
            <div className="absolute top-0 left-0 w-full h-1 bg-red-500/50 scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500"></div>
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#050b14] z-10"></div>
            
            <div className="relative z-20 p-8 flex flex-col h-full">
              <Gamepad2 size={48} className="text-gray-600 group-hover:text-red-400 transition-colors mb-6" />
              <h3 className="text-3xl font-bold text-white tracking-widest mb-2">MISSION MODE</h3>
              <p className="text-red-400 font-mono text-sm tracking-[0.2em] mb-8">"Test the decision."</p>
              
              <ul className="flex flex-col gap-3 text-gray-400 text-sm font-mono flex-grow">
                <li>[!] Time pressure</li>
                <li>[!] Weather events</li>
                <li>[!] Resource constraints</li>
                <li>[!] Replanning</li>
                <li>[!] Scoring</li>
                <li>[!] Badges</li>
              </ul>

              <button 
                onClick={() => setCurrentView('LOGIN')}
                className="w-full py-4 border border-white/20 text-white font-bold tracking-widest text-sm hover:bg-red-600 hover:border-red-500 transition-colors"
              >
                START MISSION
              </button>
            </div>
          </motion.div>

          {/* Card 3: POLAR EXPLORER */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            whileHover={{ y: -10 }}
            className="group relative border border-gray-800 bg-[#050b14] overflow-hidden flex flex-col h-[500px] transition-all duration-500 hover:border-emerald-500/50 hover:shadow-[0_0_30px_rgba(16,185,129,0.15)]"
          >
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-10 group-hover:opacity-40 transition-opacity"></div>
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#050b14] z-10"></div>
            
            <div className="relative z-20 p-8 flex flex-col h-full">
              <Map size={48} className="text-gray-600 group-hover:text-emerald-400 transition-colors mb-6" />
              <h3 className="text-3xl font-bold text-white tracking-widest mb-2">POLAR EXPLORER</h3>
              <p className="text-emerald-400 font-mono text-sm tracking-[0.2em] mb-8">"Learn the science."</p>
              
              <ul className="flex flex-col gap-3 text-gray-400 text-sm font-mono flex-grow">
                <li>[*] India's polar stations</li>
                <li>[*] Polar science</li>
                <li>[*] Expeditions</li>
                <li>[*] Interactive missions</li>
                <li>[*] Educational progression</li>
              </ul>

              <button 
                onClick={() => setCurrentView('LOGIN')}
                className="w-full py-4 border border-white/20 text-white font-bold tracking-widest text-sm hover:bg-emerald-600 hover:border-emerald-500 transition-colors"
              >
                EXPLORE
              </button>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
