import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const stations = [
  { id: 'maitri', name: 'MAITRI', region: 'Antarctica', desc: 'India\'s second permanent research station in Antarctica. Serves as a gateway for deep field expeditions.', top: '65%', left: '35%' },
  { id: 'bharati', name: 'BHARATI', region: 'Antarctica', desc: 'India\'s third Antarctic research facility. Focuses on oceanographic and continental studies.', top: '75%', left: '60%' },
  { id: 'himadri', name: 'HIMADRI', region: 'Arctic', desc: 'India\'s first permanent Arctic research station located at Spitsbergen, Svalbard.', top: '15%', left: '45%' },
  { id: 'himansh', name: 'HIMANSH', region: 'Himalayas', desc: 'High-altitude research station located in Spiti, Himachal Pradesh.', top: '35%', left: '70%' }
];

export default function PolarNetworkMap() {
  const [activeStation, setActiveStation] = useState<typeof stations[0] | null>(null);

  return (
    <section id="explorer" className="bg-[#02040a] py-32 relative">
      <div className="max-w-7xl mx-auto px-6">
        
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-4">INDIA'S POLAR PRESENCE</h2>
          <p className="text-gray-400 max-w-2xl mx-auto font-light">
            Explore the verified environments where India's polar research takes place.
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* The Map */}
          <div className="w-full lg:w-2/3 bg-[#050b14] border border-gray-800 p-4 relative min-h-[500px] overflow-hidden">
            {/* Grid overlay */}
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/grid-me.png')] opacity-10"></div>
            
            {/* Stylized World Map silhouette (CSS placeholder for the pitch) */}
            <div className="absolute inset-0 flex items-center justify-center opacity-10">
              <svg viewBox="0 0 1000 500" className="w-full h-full text-cyan-500 fill-current">
                {/* Extremely rough abstraction of continents */}
                <path d="M100,100 Q150,50 200,150 T300,100 T400,200 T500,150 T600,250 T700,200 T800,300 T900,250 L900,500 L100,500 Z" />
              </svg>
            </div>

            {/* Nodes */}
            {stations.map(station => (
              <button
                key={station.id}
                onClick={() => setActiveStation(station)}
                className="absolute flex flex-col items-center group -translate-x-1/2 -translate-y-1/2 z-20"
                style={{ top: station.top, left: station.left }}
              >
                <div className={`w-4 h-4 rounded-full border-2 border-black transition-all duration-300 ${activeStation?.id === station.id ? 'bg-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.8)] scale-125' : 'bg-gray-400 group-hover:bg-white'}`}></div>
                <div className="mt-2 text-xs font-mono font-bold tracking-widest bg-black/80 px-2 py-1 text-white opacity-0 group-hover:opacity-100 transition-opacity">
                  {station.name}
                </div>
              </button>
            ))}

            <div className="absolute bottom-4 left-4 text-[10px] text-gray-600 font-mono max-w-xs">
              VERIFIED PUBLIC INFORMATION. Geographic positioning is approximate for demonstration purposes.
            </div>
          </div>

          {/* Info Panel */}
          <div className="w-full lg:w-1/3 min-h-[300px]">
            <AnimatePresence mode="wait">
              {activeStation ? (
                <motion.div
                  key={activeStation.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="bg-black border border-cyan-900 p-8 h-full flex flex-col relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-900/20 blur-3xl rounded-full"></div>
                  
                  <h3 className="text-3xl font-bold text-white mb-2 relative z-10">{activeStation.name}</h3>
                  <div className="text-cyan-500 font-mono text-sm tracking-widest mb-6 relative z-10">{activeStation.region.toUpperCase()}</div>
                  
                  <div className="text-gray-400 mb-8 font-light leading-relaxed relative z-10">
                    {activeStation.desc}
                  </div>

                  <div className="mt-auto relative z-10">
                    <div className="text-xs text-gray-500 mb-2 font-mono">STATUS</div>
                    <div className="text-white font-mono border-l-2 border-emerald-500 pl-3 mb-6">OPERATIONAL</div>
                    
                    <button className="w-full py-3 border border-white/20 text-white font-mono text-xs hover:bg-white/10 transition-colors">
                      [ EXPLORE STATION ]
                    </button>
                  </div>
                </motion.div>
              ) : (
                <div className="bg-[#050b14] border border-gray-800 p-8 h-full flex items-center justify-center text-center">
                  <div className="text-gray-600 font-mono text-sm tracking-widest">
                    SELECT A STATION TO<br/>VIEW INTELLIGENCE
                  </div>
                </div>
              )}
            </AnimatePresence>
          </div>

        </div>
      </div>
    </section>
  );
}
