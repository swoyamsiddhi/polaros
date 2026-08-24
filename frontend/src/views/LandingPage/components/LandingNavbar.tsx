import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Hexagon } from 'lucide-react';
import { useAppContext } from '../../../AppContext';

export default function LandingNavbar() {
  const { setCurrentView } = useAppContext();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className={`fixed top-0 w-full z-50 transition-all duration-300 border-b border-white/5 ${
        scrolled ? 'bg-[#030712]/90 backdrop-blur-md py-3' : 'bg-transparent py-6'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        
        {/* Logo Section */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <Hexagon size={32} className="text-cyan-400 opacity-80" />
            <div className="absolute inset-0 bg-cyan-400 blur-md opacity-30"></div>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-white tracking-widest leading-none text-lg">POLAR OPS</span>
            <span className="text-cyan-400 tracking-[0.2em] text-[10px] font-bold">COMMANDER</span>
          </div>
          <div className="hidden md:block ml-4 pl-4 border-l border-white/10">
            <span className="text-gray-500 text-xs font-mono">SIH26062</span>
          </div>
        </div>

        {/* Links */}
        <div className="hidden md:flex items-center gap-8 text-xs font-semibold tracking-widest text-gray-400">
          <a href="#command" className="hover:text-white transition-colors">COMMAND</a>
          <a href="#missions" className="hover:text-white transition-colors">MISSIONS</a>
          <a href="#intelligence" className="hover:text-white transition-colors">INTELLIGENCE</a>
          <a href="#explorer" className="hover:text-white transition-colors">POLAR EXPLORER</a>
        </div>

        {/* CTA */}
        <div>
          <button 
            onClick={() => setCurrentView('LOGIN')}
            className="group relative px-6 py-2 bg-white/5 border border-white/10 hover:border-cyan-500/50 hover:bg-cyan-950/30 overflow-hidden transition-all duration-500"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/10 to-cyan-500/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
            <span className="relative text-xs font-bold tracking-widest text-white group-hover:text-cyan-100 flex items-center gap-2">
              [ ENTER COMMAND CENTER ]
            </span>
          </button>
        </div>

      </div>
    </motion.nav>
  );
}
