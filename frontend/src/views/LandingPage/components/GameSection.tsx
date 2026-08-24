import { motion } from 'framer-motion';

export default function GameSection() {
  return (
    <section className="bg-[#02040a] py-32 relative">
      
      {/* Visual background */}
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
      
      <div className="max-w-7xl mx-auto px-6 relative z-10 flex flex-col lg:flex-row gap-16 items-center">
        
        <div className="w-full lg:w-1/2 order-2 lg:order-1">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="border-2 border-amber-500/50 bg-[#050b14] p-8 shadow-[0_0_50px_rgba(245,158,11,0.1)]"
          >
            <div className="text-center mb-8">
              <div className="text-amber-500 font-bold tracking-widest text-sm mb-2">MISSION COMPLETE</div>
              <div className="text-5xl text-white font-bold font-mono">8,420 <span className="text-gray-500 text-xl">XP</span></div>
            </div>

            <div className="bg-amber-950/30 border border-amber-900 p-4 text-center mb-8">
              <div className="text-2xl mb-1">🏅</div>
              <div className="text-amber-500 font-bold tracking-widest">WEATHER COMMANDER</div>
            </div>

            <div className="space-y-4 font-mono text-sm">
              <div className="flex justify-between items-center pb-2 border-b border-gray-800">
                <span className="text-gray-400">Safety</span>
                <span className="text-emerald-500">96%</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-gray-800">
                <span className="text-gray-400">Efficiency</span>
                <span className="text-cyan-500">84%</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-gray-800">
                <span className="text-gray-400">Fuel Efficiency</span>
                <span className="text-emerald-500">91%</span>
              </div>
            </div>
            
            <div className="mt-8 text-center">
              <p className="text-gray-500 italic font-mono text-xs">"Every decision changes the mission."</p>
            </div>
          </motion.div>
        </div>

        <div className="w-full lg:w-1/2 order-1 lg:order-2">
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-4">THE GAME IS THE LOGISTICS.</h2>
            <h3 className="text-2xl text-cyan-400 font-light mb-8">
              Gamify the decisions. <br/>
              Never the data.
            </h3>
            
            <p className="text-gray-400 mb-8 font-light leading-relaxed">
              Mission Mode transforms real logistics decisions into interactive scenarios. It's not a simulation of physics, it's a simulation of operational consequences.
            </p>
            
            <div className="flex flex-wrap gap-3 font-mono text-xs tracking-widest text-white/80">
              <span className="border border-white/20 px-3 py-1">RESOURCE MANAGEMENT</span>
              <span className="text-gray-600 font-bold">+</span>
              <span className="border border-white/20 px-3 py-1">WEATHER EVENTS</span>
              <span className="text-gray-600 font-bold">+</span>
              <span className="border border-white/20 px-3 py-1">TIME PRESSURE</span>
              <span className="text-gray-600 font-bold">+</span>
              <span className="border border-white/20 px-3 py-1">RISK</span>
              <span className="text-gray-600 font-bold">=</span>
              <span className="bg-white text-black px-3 py-1 font-bold">MISSION</span>
            </div>
          </motion.div>
        </div>

      </div>
    </section>
  );
}
