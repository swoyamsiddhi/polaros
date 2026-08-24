import { useState } from 'react';
import { Navigation, Cpu } from 'lucide-react';
import { useAppContext } from '../AppContext';

export default function Planner() {
  const { setCurrentView } = useAppContext();
  const [analyzing, setAnalyzing] = useState(false);
  const [showPlans, setShowPlans] = useState(false);

  const handleSimulate = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setShowPlans(true);
    }, 1500);
  };

  return (
    <div className="max-w-6xl mx-auto flex flex-col h-full gap-6">
      
      <div className="flex justify-between items-center border-b-4 border-black pb-4">
        <h2 className="text-3xl font-pixel-heading text-3d m-0 flex items-center gap-2">
          <Navigation size={32} /> AI PLANNER
        </h2>
      </div>

      {!showPlans && (
        <div className="pixel-panel border-black bg-white p-6 max-w-2xl mx-auto w-full mt-8">
          <h3 className="border-b-2 border-black pb-1 mb-6 text-xl font-bold flex items-center gap-2">
            <Cpu size={20} /> DECISION SUPPORT ENGINE
          </h3>
          
          <div className="space-y-6 font-pixel text-sm">
            <div>
              <label className="block mb-2 font-bold text-gray-700">DESTINATION</label>
              <select className="w-full bg-gray-100 border-2 border-black p-2 font-pixel">
                <option>Field Camp Alpha</option>
                <option>Field Camp Beta</option>
                <option>Bharati Station</option>
              </select>
            </div>
            
            <div>
              <label className="block mb-2 font-bold text-gray-700">CRITICAL CARGO (KG)</label>
              <input type="number" defaultValue={4200} className="w-full bg-gray-100 border-2 border-black p-2 font-pixel" />
            </div>

            <div>
              <label className="block mb-2 font-bold text-gray-700">CONSTRAINTS</label>
              <div className="flex flex-col gap-2">
                <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Severe Weather Warning</label>
                <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Strict Fuel Limit</label>
                <label className="flex items-center gap-2"><input type="checkbox" /> Personnel Transport Required</label>
              </div>
            </div>

            <button 
              onClick={handleSimulate}
              className={`pixel-btn pixel-btn-primary w-full text-lg mt-4 ${analyzing ? 'animate-pulse' : ''}`}
              disabled={analyzing}
            >
              {analyzing ? '[ ANALYZING CONSTRAINTS... ]' : '[ GENERATE PLANS ]'}
            </button>
          </div>
        </div>
      )}

      {showPlans && (
        <div className="flex flex-col gap-6 w-full animate-in fade-in duration-500">
           <div className="text-center font-pixel text-gray-600 mb-2">3 PLANS GENERATED BASED ON CURRENT OPERATIONAL CONSTRAINTS</div>
           
           <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             
             {/* Plan A */}
             <div className="pixel-panel border-pixel-success bg-white p-6 flex flex-col relative overflow-hidden">
               <div className="absolute top-0 right-0 bg-pixel-success text-white px-2 py-1 text-xs font-bold font-pixel">RECOMMENDED</div>
               <h3 className="text-2xl font-bold mb-1">PLAN A</h3>
               <div className="text-sm font-pixel text-gray-500 mb-6">LOWEST RISK</div>
               
               <div className="space-y-4 font-pixel text-sm mb-8 flex-grow">
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Risk</span><span className="text-pixel-success font-bold">12% LOW</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Duration</span><span className="font-bold">36 Hours</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Fuel Usage</span><span className="font-bold text-pixel-danger">8,200 L</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Assets</span><span className="font-bold text-gray-700">2x Snow Vehicle</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Weather Comp.</span><span className="text-pixel-success font-bold">HIGH</span>
                 </div>
               </div>

               <div className="flex gap-2">
                 <button onClick={() => setCurrentView('MISSION_MODE')} className="pixel-btn bg-gray-200 flex-1 text-xs px-2">[ SIMULATE ]</button>
                 <button className="pixel-btn bg-pixel-success text-white flex-1 text-xs px-2">[ APPLY PLAN ]</button>
               </div>
             </div>

             {/* Plan B */}
             <div className="pixel-panel border-pixel-primary bg-white p-6 flex flex-col relative">
               <h3 className="text-2xl font-bold mb-1">PLAN B</h3>
               <div className="text-sm font-pixel text-gray-500 mb-6">FASTEST DELIVERY</div>
               
               <div className="space-y-4 font-pixel text-sm mb-8 flex-grow">
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Risk</span><span className="text-pixel-danger font-bold">78% HIGH</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Duration</span><span className="text-pixel-success font-bold">4 Hours</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Fuel Usage</span><span className="font-bold text-gray-700">2,400 L</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Assets</span><span className="font-bold text-gray-700">1x Aircraft</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Weather Comp.</span><span className="text-pixel-danger font-bold">LOW</span>
                 </div>
               </div>

               <div className="flex gap-2">
                 <button className="pixel-btn bg-gray-200 flex-1 text-xs px-2">[ SIMULATE ]</button>
                 <button className="pixel-btn bg-pixel-primary text-white flex-1 text-xs px-2">[ APPLY PLAN ]</button>
               </div>
             </div>

             {/* Plan C */}
             <div className="pixel-panel border-pixel-warning bg-white p-6 flex flex-col relative">
               <h3 className="text-2xl font-bold mb-1">PLAN C</h3>
               <div className="text-sm font-pixel text-gray-500 mb-6">LOWEST COST</div>
               
               <div className="space-y-4 font-pixel text-sm mb-8 flex-grow">
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Risk</span><span className="text-pixel-warning font-bold">45% MED</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Duration</span><span className="text-pixel-danger font-bold">72 Hours</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Fuel Usage</span><span className="text-pixel-success font-bold">1,200 L</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Assets</span><span className="font-bold text-gray-700">1x Snow Vehicle</span>
                 </div>
                 <div className="flex justify-between border-b-2 border-gray-100 pb-1">
                   <span>Weather Comp.</span><span className="text-pixel-warning font-bold">MED</span>
                 </div>
               </div>

               <div className="flex gap-2">
                 <button className="pixel-btn bg-gray-200 flex-1 text-xs px-2">[ SIMULATE ]</button>
                 <button className="pixel-btn bg-yellow-500 text-black flex-1 text-xs px-2">[ APPLY PLAN ]</button>
               </div>
             </div>

           </div>
        </div>
      )}
    </div>
  );
}
