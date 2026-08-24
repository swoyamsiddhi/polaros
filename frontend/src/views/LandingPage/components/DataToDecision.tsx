import { motion } from 'framer-motion';
import { ArrowDown } from 'lucide-react';

const nodes = [
  { title: 'DATA', desc: 'Weather, Inventory, Assets, Personnel, Shipments', color: 'border-gray-700' },
  { title: 'INFORMATION', desc: 'Current operational picture', color: 'border-cyan-900' },
  { title: 'RISK', desc: 'Potential mission failure identification', color: 'border-amber-900' },
  { title: 'RECOMMENDATION', desc: 'AI-assisted response generation', color: 'border-emerald-900' },
  { title: 'DECISION', desc: 'Human-controlled action', color: 'border-cyan-500 bg-cyan-950/30' }
];

export default function DataToDecision() {
  return (
    <section className="bg-[#02040a] py-32 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        
        <div className="text-center mb-20">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-6"
          >
            FROM DATA TO DECISION
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-xl text-gray-400 max-w-2xl mx-auto font-light"
          >
            Polar logistics is not simply about knowing where an asset is. <br/>
            <span className="text-white">It is about understanding what happens next.</span>
          </motion.p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8 max-w-5xl mx-auto">
          {nodes.map((node, index) => (
            <div key={index} className="flex flex-col md:flex-row items-center gap-4 md:gap-8 w-full md:w-auto">
              
              <motion.div 
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.5 }}
                className={`flex flex-col items-center justify-center p-6 border-2 ${node.color} w-full md:w-48 aspect-square text-center relative group`}
              >
                <div className="text-lg font-bold text-white tracking-widest mb-2">{node.title}</div>
                <div className="text-xs text-gray-400">{node.desc}</div>
                
                {/* Glow effect */}
                <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              </motion.div>

              {index < nodes.length - 1 && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: (index * 0.2) + 0.1 }}
                  className="text-gray-600 md:rotate-[-90deg]"
                >
                  <ArrowDown size={24} />
                </motion.div>
              )}
            </div>
          ))}
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 1.2 }}
          className="text-center mt-24"
        >
          <div className="text-2xl md:text-3xl font-light text-cyan-100 italic">
            "One operational picture. <br className="md:hidden" /> One decision engine."
          </div>
        </motion.div>

      </div>
    </section>
  );
}
