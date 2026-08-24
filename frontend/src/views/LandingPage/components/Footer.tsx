export default function Footer() {
  return (
    <footer className="bg-[#010205] border-t border-white/10 pt-20 pb-10 text-gray-500 font-mono text-xs">
      <div className="max-w-7xl mx-auto px-6">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          
          {/* Col 1 */}
          <div className="md:col-span-2">
            <h3 className="text-white font-bold tracking-widest text-lg mb-2">POLAR OPS COMMANDER</h3>
            <p className="mb-6 max-w-sm">
              Integrated Polar Expedition Logistics, Asset Management & Mission-Based Learning.
            </p>
            <div className="space-y-1 text-gray-600">
              <div>SIH2026</div>
              <div>Problem Statement: SIH26062</div>
              <div>NCPOR, Ministry of Earth Sciences</div>
            </div>
          </div>

          {/* Col 2 */}
          <div>
            <h4 className="text-white font-bold tracking-widest mb-4">TECHNOLOGY</h4>
            <ul className="space-y-2">
              <li>React + TypeScript</li>
              <li>FastAPI + PostgreSQL</li>
              <li>Framer Motion</li>
              <li>AI / ML Predictive Engine</li>
              <li>Event-Driven Simulation</li>
            </ul>
          </div>

          {/* Col 3 */}
          <div>
            <h4 className="text-white font-bold tracking-widest mb-4">LINKS</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-cyan-400 transition-colors">Command Center</a></li>
              <li><a href="#missions" className="hover:text-cyan-400 transition-colors">Mission Mode</a></li>
              <li><a href="#explorer" className="hover:text-cyan-400 transition-colors">Polar Explorer</a></li>
              <li><a href="#intelligence" className="hover:text-cyan-400 transition-colors">Intelligence</a></li>
              <li><a href="#" className="hover:text-cyan-400 transition-colors">About</a></li>
            </ul>
          </div>

        </div>

        {/* Disclaimer */}
        <div className="border-t border-white/5 pt-8 text-center text-gray-600 max-w-4xl mx-auto">
          <p>
            DISCLAIMER: Prototype demonstration. Operational values and scenarios shown in the interface are simulated unless explicitly identified as public reference information. This system does not connect to live government databases.
          </p>
        </div>

      </div>
    </footer>
  );
}
