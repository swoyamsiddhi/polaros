import { useAppContext } from '../AppContext';

const expeditions = [
  { id: 'EXP-2026-012', title: 'Summer Resupply S-1', status: 'COMPLETED', readiness: 100 },
  { id: 'EXP-2026-013', title: 'Winter Team Bravo', status: 'IN_TRANSIT', readiness: 92 },
  { id: 'EXP-2026-014', title: 'Emergency Fuel Drop', status: 'PLANNING', readiness: 65, alert: true },
  { id: 'EXP-2026-015', title: 'Maitri Equipment Swap', status: 'PLANNING', readiness: 42 }
];

export default function ExpeditionsList() {
  const { setCurrentView, setActiveExpedition } = useAppContext();

  const handleSelect = (id: string) => {
    setActiveExpedition(id);
    setCurrentView('EXPEDITION_DETAIL');
  };

  return (
    <div className="max-w-5xl mx-auto flex flex-col h-full gap-6">
      <div className="flex justify-between items-center border-b-4 border-black pb-4">
        <h2 className="text-3xl font-pixel-heading text-3d m-0">EXPEDITIONS</h2>
        <button className="pixel-btn pixel-btn-primary">
          [+ NEW EXPEDITION]
        </button>
      </div>

      <div className="flex flex-col gap-4">
        {expeditions.map(exp => (
          <div 
            key={exp.id} 
            className={`pixel-panel flex items-center justify-between p-4 cursor-pointer hover:bg-gray-100 ${
              exp.alert ? 'border-pixel-danger' : 'border-pixel-primary'
            }`}
            onClick={() => handleSelect(exp.id)}
          >
            <div className="flex flex-col">
              <span className="font-pixel text-xs text-gray-500 mb-1">{exp.id}</span>
              <span className="text-xl font-bold">{exp.title}</span>
            </div>
            <div className="flex items-center gap-8">
              <div className="flex flex-col items-end">
                <span className="font-pixel text-xs text-gray-500 mb-1">STATUS</span>
                <span className={`font-pixel font-bold text-xs ${
                  exp.status === 'COMPLETED' ? 'text-pixel-success' :
                  exp.status === 'IN_TRANSIT' ? 'text-pixel-primary' : 'text-pixel-warning'
                }`}>{exp.status}</span>
              </div>
              <div className="flex flex-col items-end">
                <span className="font-pixel text-xs text-gray-500 mb-1">READINESS</span>
                <span className={`font-pixel font-bold text-xs ${exp.alert ? 'text-pixel-danger' : 'text-black'}`}>
                  {exp.readiness}%
                </span>
              </div>
              <button className="pixel-btn bg-gray-200">
                [MANAGE]
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
