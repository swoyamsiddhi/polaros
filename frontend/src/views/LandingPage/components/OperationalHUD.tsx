import { motion } from 'framer-motion';

const stats = [
  { label: 'ACTIVE EXPEDITIONS', value: '08' },
  { label: 'REGISTERED ASSETS', value: '142' },
  { label: 'SHIPMENTS IN TRANSIT', value: '23' },
  { label: 'CRITICAL ALERTS', value: '07', isAlert: true },
  { label: 'POLAR STATIONS', value: '04' }
];

export default function OperationalHUD() {
  return (
    <div className="bg-[#030712] border-y border-white/10 relative z-30">
      <div className="max-w-7xl mx-auto px-6 py-8">
        
        <div className="text-center mb-6">
          <span className="text-[10px] font-mono tracking-[0.2em] text-gray-500 uppercase border border-gray-800 px-3 py-1 rounded-sm">
            SIMULATED OPERATIONS DATA
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 divide-x divide-white/5">
          {stats.map((stat, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className={`flex flex-col items-center justify-center text-center ${index !== 0 ? 'pl-8' : ''}`}
            >
              <div className={`text-4xl md:text-5xl font-light mb-2 font-mono ${stat.isAlert ? 'text-red-500 animate-pulse' : 'text-white'}`}>
                {stat.value}
              </div>
              <div className="text-xs font-bold tracking-widest text-gray-500 max-w-[120px]">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
