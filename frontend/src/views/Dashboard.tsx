import { useEffect, useState } from 'react';
import { ShieldAlert, Ship, Anchor, Thermometer, CheckCircle2, AlertTriangle, AlertOctagon, Activity } from 'lucide-react';

interface DashboardData {
  active_expeditions: number;
  total_assets: number;
  critical_assets: number;
  active_shipments: number;
  delayed_shipments: number;
  critical_alerts: number;
  overall_readiness: number;
  stations: any[];
  recent_alerts: any[];
  expedition_summary: any[];
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboard = () => {
    fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/dashboard/summary`)
      .then(res => res.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError('MAINFRAME_CONNECTION_LOST');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchDashboard();
    const timer = setInterval(fetchDashboard, 10000);
    return () => clearInterval(timer);
  }, []);

  if (loading) return <div className="text-2xl animate-pulse">LOADING_MAINFRAME_DATA...</div>;
  if (error) return <div className="text-2xl text-pixel-danger animate-blink">{error}</div>;
  if (!data) return null;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end border-b-4 border-black pb-2">
        <h2 className="text-3xl text-3d font-pixel-heading m-0 flex items-center gap-2 mb-2"><ActivityIcon /> LIVE_OPERATIONS_FEED</h2>
        <span className="text-sm">AUTO-REFRESH: ENABLED</span>
      </div>

      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="pixel-panel flex flex-col justify-between">
          <div className="text-sm border-b-2 border-black pb-1 mb-2">READINESS_SCORE</div>
          <div className="text-4xl font-bold flex items-center justify-between">
            {data.overall_readiness}%
            {data.overall_readiness > 80 ? <CheckCircle2 size={32} className="text-pixel-success" /> : <AlertTriangle size={32} className="text-pixel-warning" />}
          </div>
        </div>

        <div className="pixel-panel flex flex-col justify-between">
          <div className="text-sm border-b-2 border-black pb-1 mb-2">ACTIVE_EXPEDITIONS</div>
          <div className="text-4xl font-bold flex items-center justify-between">
            {data.active_expeditions}
            <Anchor size={32} />
          </div>
        </div>

        <div className="pixel-panel bg-[#dfdfdf] flex flex-col justify-between">
          <div className="text-sm border-b-2 border-black pb-1 mb-2">SHIPMENTS_IN_TRANSIT</div>
          <div className="text-4xl font-bold flex items-center justify-between">
            {data.active_shipments}
            <Ship size={32} />
          </div>
          {data.delayed_shipments > 0 && (
            <div className="text-xs text-pixel-danger mt-1 animate-pulse">⚠ {data.delayed_shipments} DELAYED</div>
          )}
        </div>

        <div className={`pixel-panel flex flex-col justify-between ${data.critical_alerts > 0 ? 'bg-[#ffcccc]' : ''}`}>
          <div className="text-sm border-b-2 border-black pb-1 mb-2">CRITICAL_ALERTS</div>
          <div className="text-4xl font-bold flex items-center justify-between">
            <span className={data.critical_alerts > 0 ? "text-pixel-danger" : ""}>{data.critical_alerts}</span>
            <AlertOctagon size={32} className={data.critical_alerts > 0 ? "text-pixel-danger animate-pulse" : ""} />
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Stations Column */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <div className="pixel-panel h-full">
            <h3 className="text-lg border-b-4 border-black pb-2 mb-4 flex items-center gap-2">
              <Thermometer size={20}/> STATION_STATUS
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.stations.map((station: any) => (
                <div key={station.id} className="pixel-panel-inset text-white text-sm flex flex-col gap-2">
                  <div className="flex justify-between items-center border-b-2 border-white/20 pb-1">
                    <span className="font-pixel-heading text-xs text-pixel-primary">{station.code}</span>
                    <span className={`px-2 py-1 text-xs ${
                      station.status === 'OPERATIONAL' ? 'bg-pixel-success text-white' : 
                      station.status === 'LIMITED' ? 'bg-pixel-warning text-black' : 'bg-pixel-danger text-white'
                    }`}>
                      {station.status}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-x-2 gap-y-1 mt-1">
                    <div className="text-gray-400">Weather:</div>
                    <div className="flex items-center gap-1">
                      {station.temperature}°C 
                      {station.weather_severity === 'SEVERE' && <AlertTriangle size={14} className="text-pixel-danger animate-blink" />}
                    </div>
                    
                    <div className="text-gray-400">Capacity:</div>
                    <div>{station.occupancy} / {station.capacity}</div>
                    
                    <div className="text-gray-400">Comms:</div>
                    <div className={station.comm_status === 'ONLINE' ? 'text-pixel-success' : 'text-pixel-warning'}>{station.comm_status}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Alerts Column */}
        <div className="flex flex-col gap-4">
          <div className="pixel-panel h-full">
            <h3 className="text-lg border-b-4 border-black pb-2 mb-4 flex items-center gap-2">
              <ShieldAlert size={20}/> SYSTEM_ALERTS
            </h3>
            
            <div className="flex flex-col gap-3">
              {data.recent_alerts.length === 0 ? (
                <div className="text-center p-4 text-pixel-success">ALL_SYSTEMS_NOMINAL</div>
              ) : (
                data.recent_alerts.map((alert: any) => (
                  <div key={alert.id} className={`p-2 border-l-4 ${alert.severity === 'CRITICAL' ? 'border-pixel-danger bg-[#ffeeee]' : 'border-pixel-warning bg-[#ffffee]'}`}>
                    <div className="font-bold flex items-center gap-2 mb-1">
                      {alert.severity === 'CRITICAL' ? <AlertOctagon size={16} className="text-pixel-danger" /> : <AlertTriangle size={16} className="text-pixel-warning" />}
                      <span className="text-sm">{alert.title}</span>
                    </div>
                    <div className="text-xs">{alert.description}</div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

function ActivityIcon() {
  return <Activity size={24} className="text-pixel-primary" />;
}
