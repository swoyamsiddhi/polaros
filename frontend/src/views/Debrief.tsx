
import { useAppContext } from '../AppContext';
import { CheckCircle, AlertTriangle } from 'lucide-react';

export default function Debrief() {
  const { setCurrentView } = useAppContext();

  return (
    <div className="flex flex-col h-full gap-4 max-w-4xl mx-auto w-full">
      <h2 className="text-3xl font-pixel-heading text-3d mb-2 text-center">MISSION DEBRIEF</h2>
      <div className="text-center text-gray-500 font-bold tracking-widest mb-8">MISSION: WHITEOUT RESUPPLY</div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Score Panel */}
        <div className="pixel-panel flex flex-col items-center justify-center">
          <div className="text-sm text-gray-500 mb-2">FINAL SCORE</div>
          <div className="text-6xl font-pixel-heading text-pixel-primary mb-8">8,420</div>
          
          <div className="w-full">
            <div className="text-center text-sm font-bold mb-4 border-b-2 border-black pb-2">YOUR PERFORMANCE</div>
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-4"><span className="w-24 text-right">Safety</span><div className="flex-grow h-4 bg-gray-200 border-2 border-black"><div className="h-full bg-pixel-success" style={{width:'96%'}}></div></div><span className="w-12">96%</span></div>
              <div className="flex items-center gap-4"><span className="w-24 text-right">Efficiency</span><div className="flex-grow h-4 bg-gray-200 border-2 border-black"><div className="h-full bg-pixel-primary" style={{width:'84%'}}></div></div><span className="w-12">84%</span></div>
              <div className="flex items-center gap-4"><span className="w-24 text-right">Fuel Usage</span><div className="flex-grow h-4 bg-gray-200 border-2 border-black"><div className="h-full bg-pixel-success" style={{width:'91%'}}></div></div><span className="w-12">91%</span></div>
              <div className="flex items-center gap-4"><span className="w-24 text-right">Timing</span><div className="flex-grow h-4 bg-gray-200 border-2 border-black"><div className="h-full bg-pixel-warning" style={{width:'76%'}}></div></div><span className="w-12">76%</span></div>
              <div className="flex items-center gap-4"><span className="w-24 text-right">Inventory</span><div className="flex-grow h-4 bg-gray-200 border-2 border-black"><div className="h-full bg-pixel-success" style={{width:'98%'}}></div></div><span className="w-12">98%</span></div>
            </div>
          </div>
        </div>

        {/* Feedback Panel */}
        <div className="flex flex-col gap-6">
          <div className="pixel-panel border-pixel-success">
            <h3 className="text-lg font-bold mb-4 text-pixel-success flex items-center gap-2 border-b-2 border-gray-200 pb-2">
              <CheckCircle size={20} /> YOU SUCCEEDED BECAUSE
            </h3>
            <ul className="text-sm flex flex-col gap-2">
              <li>✓ Prioritised medical cargo</li>
              <li>✓ Maintained emergency fuel reserve</li>
              <li>✓ Switched transport mode during event</li>
              <li>✓ Avoided unsafe aircraft deployment</li>
            </ul>
          </div>

          <div className="pixel-panel border-pixel-warning">
            <h3 className="text-lg font-bold mb-4 text-pixel-warning flex items-center gap-2 border-b-2 border-gray-200 pb-2">
              <AlertTriangle size={20} /> YOU COULD IMPROVE
            </h3>
            <ul className="text-sm flex flex-col gap-2">
              <li>⚠ Asset utilisation (Snowcat was idle for 2h)</li>
              <li>⚠ Shipment scheduling</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap justify-center gap-4 mt-8">
        <button className="pixel-btn bg-gray-300">[ REPLAY MISSION ]</button>
        <button className="pixel-btn bg-gray-300">[ NEXT MISSION ]</button>
        <button 
          onClick={() => setCurrentView('COMMAND_HOME')}
          className="pixel-btn pixel-btn-primary"
        >
          [ RETURN TO COMMAND ]
        </button>
      </div>
    </div>
  );
}
