import { useState } from 'react';
import { Database as DbIcon, Search, Filter, Box, Users, Wrench, Fuel, BarChart } from 'lucide-react';
import { useAppContext } from '../AppContext';

// Mock Data
const inventoryData = [
  { id: 1, item: "Aviation Fuel (JET-A1)", station: "Bharati", category: "FUEL", qty: 3200, unit: "L", status: "NOMINAL", fill: 75, burnRate: "200L/day", criticalDay: 16 },
  { id: 2, item: "Diesel Fuel", station: "Maitri", category: "FUEL", qty: 12000, unit: "L", status: "NOMINAL", fill: 85, burnRate: "350L/day", criticalDay: 34 },
  { id: 3, item: "Aviation Fuel (JET-A1)", station: "Field Camp Alpha", category: "FUEL", qty: 400, unit: "L", status: "CRITICAL", fill: 15, burnRate: "120L/day", criticalDay: 3 },
  { id: 4, item: "Arctic Rations", station: "Himansh", category: "FOOD", qty: 25, unit: "packs", status: "CRITICAL", fill: 10, burnRate: "8 packs/day", criticalDay: 3 },
  { id: 5, item: "Generator Spare Parts", station: "Bharati", category: "SPARE_PARTS", qty: 5, unit: "sets", status: "LOW", fill: 25, burnRate: "1/month", criticalDay: 150 },
];

const personnelData = [
  { id: 1, name: "Dr. Priya Nair", role: "Station Commander", org: "NCPOR", station: "Bharati", status: "AT_STATION" },
  { id: 2, name: "Cmdr. Anil Sharma", role: "Logistics Officer", org: "Indian Navy", station: "Goa-WH", status: "AT_STATION" },
  { id: 3, name: "Tech. Sunil Mehra", role: "Field Technician", org: "NCPOR", station: "Field Camp Alpha", status: "AT_FIELD_CAMP" },
  { id: 4, name: "Dr. Mohan Das", role: "Research Scientist", org: "NCPOR", station: "In Transit", status: "DELAYED" },
];

const assetData = [
  { id: 'A-101', type: 'Diesel Generator', station: 'Bharati', status: 'ONLINE', condition: 95, lifecycle: 'IN USE' },
  { id: 'A-102', type: 'Snowcat Vehicle', station: 'Maitri', status: 'MAINTENANCE', condition: 45, lifecycle: 'MAINTENANCE REQUIRED' },
  { id: 'A-103', type: 'Sat-Com Dish', station: 'Field Camp Alpha', status: 'ONLINE', condition: 88, lifecycle: 'DEPLOYED' },
];

export default function Database() {
  const { currentView } = useAppContext();
  
  // Default to inventory if coming from a generic route, otherwise use the specific view
  let initialTab = 'inventory';
  if (currentView === 'ASSETS') initialTab = 'assets';
  if (currentView === 'PERSONNEL') initialTab = 'personnel';
  if (currentView === 'SHIPMENTS') initialTab = 'shipments';
  if (currentView === 'STATIONS') initialTab = 'stations';

  const [activeTab, setActiveTab] = useState(initialTab);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredInventory = inventoryData.filter(row => 
    row.item.toLowerCase().includes(searchQuery.toLowerCase()) || 
    row.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
    row.station.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col h-full gap-4 max-w-7xl mx-auto w-full">
      <div className="flex justify-between items-end border-b-4 border-black pb-2">
        <h2 className="text-3xl font-pixel-heading text-3d m-0 flex items-center gap-2 mb-2">
          <DbIcon size={32} /> {activeTab.toUpperCase()}_REGISTRY
        </h2>
        <div className="flex gap-2">
          <button onClick={() => setActiveTab('inventory')} className={`pixel-btn ${activeTab === 'inventory' ? 'pixel-btn-primary' : ''}`}>INVENTORY</button>
          <button onClick={() => setActiveTab('assets')} className={`pixel-btn ${activeTab === 'assets' ? 'pixel-btn-primary' : ''}`}>ASSETS</button>
          <button onClick={() => setActiveTab('personnel')} className={`pixel-btn ${activeTab === 'personnel' ? 'pixel-btn-primary' : ''}`}>PERSONNEL</button>
          <button onClick={() => setActiveTab('shipments')} className={`pixel-btn ${activeTab === 'shipments' ? 'pixel-btn-primary' : ''}`}>SHIPMENTS</button>
        </div>
      </div>

      {activeTab === 'inventory' && (
        <div className="flex flex-col gap-6">
          {/* Charts Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div className="pixel-panel border-black bg-white">
              <h3 className="border-b-2 border-black pb-1 mb-4 flex items-center gap-2 text-xl font-bold">
                <BarChart size={20} /> INVENTORY FORECAST
              </h3>
              
              <div className="bg-gray-100 border-2 border-gray-300 p-4 font-pixel text-sm relative h-48 flex flex-col justify-end">
                <div className="absolute top-2 left-2 text-gray-500">Field Camp Alpha - Aviation Fuel</div>
                <div className="absolute top-2 right-2 text-pixel-danger animate-pulse font-bold">CRITICAL: DAY 3</div>
                
                {/* Pixel art forecast graph */}
                <div className="flex items-end h-32 gap-1 w-full border-b-2 border-l-2 border-black p-1 relative">
                  <div className="absolute bottom-4 w-full border-t-2 border-pixel-danger border-dashed"></div>
                  <div className="bg-pixel-primary w-1/6 h-[90%] border-2 border-black"></div>
                  <div className="bg-pixel-primary w-1/6 h-[75%] border-2 border-black"></div>
                  <div className="bg-pixel-warning w-1/6 h-[40%] border-2 border-black"></div>
                  <div className="bg-pixel-danger w-1/6 h-[10%] border-2 border-black animate-pulse"></div>
                  <div className="bg-gray-300 w-1/6 h-0 border-b-2 border-black relative">
                     <span className="absolute -top-6 text-2xl">❌</span>
                  </div>
                  <div className="bg-pixel-success w-1/6 h-[80%] border-2 border-black relative">
                     <span className="absolute -top-8 text-xs font-bold text-pixel-success">RESUPPLY ARRIVES</span>
                  </div>
                </div>
                <div className="flex justify-between text-xs mt-2 text-gray-500">
                  <span>TODAY</span>
                  <span>DAY 2</span>
                  <span>DAY 3</span>
                  <span>DAY 4</span>
                  <span>DAY 5</span>
                  <span>DAY 6</span>
                </div>
              </div>
            </div>

            <div className="pixel-panel border-black bg-white">
              <h3 className="border-b-2 border-black pb-1 mb-4 flex items-center gap-2 text-xl font-bold">
                <Box size={20} /> CRITICAL STOCK OUTS
              </h3>
              <div className="flex flex-col gap-4">
                <div className="border-l-4 border-pixel-danger pl-4 bg-red-50 p-2">
                  <div className="font-bold text-pixel-danger">Aviation Fuel (JET-A1)</div>
                  <div className="text-sm">Location: Field Camp Alpha</div>
                  <div className="text-sm font-bold mt-2 text-gray-700">Burn Rate: 120L/day | Zero Stock: 3 days</div>
                </div>
                <div className="border-l-4 border-pixel-danger pl-4 bg-red-50 p-2">
                  <div className="font-bold text-pixel-danger">Arctic Rations</div>
                  <div className="text-sm">Location: Himansh</div>
                  <div className="text-sm font-bold mt-2 text-gray-700">Burn Rate: 8 packs/day | Zero Stock: 3 days</div>
                </div>
              </div>
            </div>
          </div>

          {/* Table Section */}
          <div className="pixel-panel flex-grow flex flex-col bg-white border-black">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">INVENTORY REGISTRY</h3>
              <div className="flex gap-2">
                <div className="bg-white border-4 border-black flex items-center px-2">
                  <Search size={16} />
                  <input 
                    type="text" 
                    placeholder="Search items..." 
                    className="outline-none px-2 font-pixel text-lg" 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
                <button className="pixel-btn bg-gray-200 text-black"><Filter size={16} /> CATEGORY</button>
                <button className="pixel-btn bg-gray-200 text-black"><Filter size={16} /> STATION</button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse font-pixel">
                <thead>
                  <tr className="bg-black text-white text-sm border-b-4 border-black">
                    <th className="p-2">ITEM</th>
                    <th className="p-2">LOCATION</th>
                    <th className="p-2">CURRENT</th>
                    <th className="p-2">BURN RATE</th>
                    <th className="p-2">STATUS</th>
                  </tr>
                </thead>
                <tbody className="bg-white">
                  {filteredInventory.map(row => (
                    <tr key={row.id} className="border-b-2 border-gray-300 hover:bg-gray-100 text-sm">
                      <td className="p-2 font-bold">{row.item}</td>
                      <td className="p-2">{row.station}</td>
                      <td className="p-2 font-bold">{row.qty} {row.unit}</td>
                      <td className="p-2">{row.burnRate}</td>
                      <td className="p-2">
                        <span className={`px-2 py-1 text-xs text-white ${
                          row.status === 'NOMINAL' ? 'bg-pixel-success' : 
                          row.status === 'LOW' ? 'bg-pixel-warning text-black' : 'bg-pixel-danger animate-pulse'
                        }`}>
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'assets' && (
        <div className="pixel-panel flex-grow border-black bg-white">
          <h3 className="border-b-2 border-black pb-1 mb-4 flex items-center gap-2 text-xl font-bold">
            <Wrench size={20} /> ASSET LIFECYCLE MANAGEMENT
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse font-pixel">
              <thead>
                <tr className="bg-black text-white text-sm border-b-4 border-black">
                  <th className="p-2">ID</th>
                  <th className="p-2">TYPE</th>
                  <th className="p-2">STATION</th>
                  <th className="p-2">LIFECYCLE STAGE</th>
                  <th className="p-2">CONDITION</th>
                </tr>
              </thead>
              <tbody className="bg-white">
                {assetData.map(row => (
                  <tr key={row.id} className="border-b-2 border-gray-300 hover:bg-gray-100 text-sm">
                    <td className="p-2 font-bold">{row.id}</td>
                    <td className="p-2">{row.type}</td>
                    <td className="p-2">{row.station}</td>
                    <td className="p-2 font-bold text-gray-700">{row.lifecycle}</td>
                    <td className="p-2">
                      <div className="flex items-center gap-2">
                        <span className={`font-bold ${row.condition > 50 ? 'text-pixel-success' : 'text-pixel-danger'}`}>{row.condition}%</span>
                        <div className="h-2 w-24 bg-gray-300 border border-black">
                          <div className={`h-full ${row.condition > 50 ? 'bg-pixel-success' : 'bg-pixel-danger'}`} style={{ width: `${row.condition}%` }}></div>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'personnel' && (
        <div className="pixel-panel flex-grow border-black bg-white">
          <h3 className="border-b-2 border-black pb-1 mb-4 flex items-center gap-2 text-xl font-bold">
            <Users size={20} /> PERSONNEL ROSTER
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse font-pixel">
              <thead>
                <tr className="bg-black text-white text-sm border-b-4 border-black">
                  <th className="p-2">NAME</th>
                  <th className="p-2">ROLE</th>
                  <th className="p-2">ORG</th>
                  <th className="p-2">LOCATION</th>
                  <th className="p-2">STATUS</th>
                </tr>
              </thead>
              <tbody className="bg-white">
                {personnelData.map(row => (
                  <tr key={row.id} className="border-b-2 border-gray-300 hover:bg-gray-100 text-sm">
                    <td className="p-2 font-bold">{row.name}</td>
                    <td className="p-2">{row.role}</td>
                    <td className="p-2">{row.org}</td>
                    <td className="p-2">{row.station}</td>
                    <td className="p-2">
                      <span className={`px-2 py-1 text-xs text-white ${
                        row.status === 'AT_STATION' ? 'bg-pixel-success' : 
                        row.status === 'AT_FIELD_CAMP' ? 'bg-pixel-primary' : 'bg-pixel-danger animate-pulse'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'shipments' && (
        <div className="flex flex-col gap-6">
          <div className="pixel-panel border-pixel-danger bg-white p-6 relative overflow-hidden">
             <h3 className="border-b-2 border-pixel-danger pb-1 mb-4 flex items-center gap-2 text-xl font-bold text-pixel-danger">
                DELAYED SHIPMENT: S-204
              </h3>
              
              <div className="flex items-center justify-between font-pixel text-sm text-black mb-6">
                <div className="text-center">
                  <div>INDIA</div>
                  <div className="text-xs text-pixel-success mt-1">COMPLETED</div>
                </div>
                <div className="text-gray-400">──────&gt;</div>
                <div className="text-center">
                  <div>GATEWAY PORT</div>
                  <div className="text-xs text-pixel-success mt-1">COMPLETED</div>
                </div>
                <div className="text-gray-400">──────&gt;</div>
                <div className="text-center bg-red-100 border-2 border-pixel-danger px-4 py-2">
                  <div>BHARATI</div>
                  <div className="text-xs text-pixel-danger mt-1 font-bold animate-pulse">DELAYED</div>
                </div>
                <div className="text-gray-400">──────&gt;</div>
                <div className="text-center text-gray-500">
                  <div>CAMP ALPHA</div>
                  <div className="text-xs mt-1">PENDING</div>
                </div>
              </div>

              <div className="bg-red-50 border-l-4 border-pixel-danger p-4">
                <div className="font-bold text-pixel-danger mb-2">IMPACT ANALYSIS</div>
                <div className="text-sm font-pixel text-gray-700">Expedition EXP-2026-014 Affected. Fuel reserve at Field Camp Alpha at risk of stockout.</div>
              </div>
          </div>
        </div>
      )}
    </div>
  );
}
