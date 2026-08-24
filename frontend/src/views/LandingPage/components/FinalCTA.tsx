import { motion } from 'framer-motion';
import { useAppContext } from '../../../AppContext';

export default function FinalCTA() {
  const { setCurrentView } = useAppContext();

  return (
    <section className="bg-black py-40 relative overflow-hidden flex items-center justify-center border-t border-white/10">
      
      {/* Background cinematic environment */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-t from-cyan-950/20 to-black/80 z-10"></div>
        {/* Subtle aurora */}
        <motion.div 
          animate={{ opacity: [0.1, 0.3, 0.1], scale: [1, 1.1, 1] }}
          transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
          className="absolute bottom-0 w-full h-[50vh] bg-cyan-600/20 blur-[100px]"
        ></motion.div>
        {/* Base snow particles */}
        <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]"></div>
      </div>

      <div className="max-w-4xl mx-auto px-6 relative z-20 text-center">
        
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-5xl md:text-7xl font-bold text-white tracking-tighter mb-8 leading-none"
        >
          READY TO COMMAND<br/>
          <span className="text-gray-500 font-light">THE EXPEDITION?</span>
        </motion.h2>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-xl text-cyan-100 font-mono tracking-widest max-w-2xl mx-auto mb-16 leading-relaxed"
        >
          Plan the mission. <br className="md:hidden"/>Track the resources. <br className="md:hidden"/>Predict the risks. <br/>
          Respond to the unexpected. <br className="md:hidden"/>Explore India's polar world.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="flex flex-col sm:flex-row justify-center gap-6"
        >
          <button 
            onClick={() => setCurrentView('LOGIN')}
            className="group relative px-10 py-5 bg-white text-black font-bold tracking-widest text-sm flex items-center justify-center gap-3 overflow-hidden"
          >
            <div className="absolute inset-0 bg-cyan-500 -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></div>
            <span className="relative z-10 group-hover:text-white transition-colors duration-300 flex items-center gap-2">
              [ ENTER COMMAND CENTER ]
            </span>
          </button>
          
          <button 
            onClick={() => setCurrentView('POLAR_EXPLORER')}
            className="px-10 py-5 bg-transparent border border-white/20 text-white font-bold tracking-widest text-sm hover:bg-white/5 transition-all duration-300"
          >
            [ EXPLORE POLAR WORLD ]
          </button>
        </motion.div>

      </div>
    </section>
  );
}
