import { motion } from 'framer-motion';
import { Target, TrendingDown, GitBranch } from 'lucide-react';

export default function IntelligenceSection() {
  return (
    <section id="intelligence" className="bg-[#010205] py-32 border-y border-white/5 relative">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        
        <div className="text-center mb-24">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-4"
          >
            THE SYSTEM DOESN'T JUST TRACK.<br/>
            <span className="text-gray-500 font-light">IT THINKS AHEAD.</span>
          </motion.h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-24">
          
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="flex flex-col items-center text-center"
          >
            <div className="w-16 h-16 rounded-full border border-red-500/30 bg-red-950/20 flex items-center justify-center mb-6 text-red-500">
              <Target size={24} />
            </div>
            <h3 className="text-lg font-bold text-white tracking-widest mb-4">RISK PREDICTION</h3>
            <p className="text-gray-400 font-light text-sm">
              "Identify expedition risks before they become mission failures."
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col items-center text-center"
          >
            <div className="w-16 h-16 rounded-full border border-cyan-500/30 bg-cyan-950/20 flex items-center justify-center mb-6 text-cyan-400">
              <TrendingDown size={24} />
            </div>
            <h3 className="text-lg font-bold text-white tracking-widest mb-4">INVENTORY FORECASTING</h3>
            <p className="text-gray-400 font-light text-sm">
              "Know exactly when critical supplies will run out based on burn rates."
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
            className="flex flex-col items-center text-center"
          >
            <div className="w-16 h-16 rounded-full border border-emerald-500/30 bg-emerald-950/20 flex items-center justify-center mb-6 text-emerald-400">
              <GitBranch size={24} />
            </div>
            <h3 className="text-lg font-bold text-white tracking-widest mb-4">INTELLIGENT PLANNING</h3>
            <p className="text-gray-400 font-light text-sm">
              "Compare multiple logistics plans under real constraints instantly."
            </p>
          </motion.div>

        </div>

        {/* Example HUD */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto bg-black border border-gray-800 p-8 shadow-2xl relative"
        >
          <div className="absolute top-4 right-4 text-[10px] text-gray-600 font-mono">SIMULATED DEMONSTRATION DATA</div>
          
          <div className="text-red-500 font-mono tracking-widest text-sm mb-6 pb-4 border-b border-white/10">EXAMPLE ANALYSIS</div>
          
          <div className="flex justify-between items-end mb-8">
            <h4 className="text-2xl text-white font-bold">EXPEDITION RISK</h4>
            <div className="text-4xl text-white font-light">72%</div>
          </div>

          <div className="text-gray-500 font-mono text-xs mb-4">PRIMARY FACTORS:</div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center pb-2 border-b border-gray-900">
              <span className="text-gray-300">Weather deterioration</span>
              <span className="text-red-500 font-mono">+24%</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-gray-900">
              <span className="text-gray-300">Critical inventory</span>
              <span className="text-red-500 font-mono">+20%</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-gray-900">
              <span className="text-gray-300">Asset maintenance</span>
              <span className="text-amber-500 font-mono">+17%</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-gray-900">
              <span className="text-gray-300">Shipment delay</span>
              <span className="text-amber-500 font-mono">+11%</span>
            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
}
