import { useState } from 'react';
import { useAppContext, type Role } from '../AppContext';

export default function Login() {
  const { setActiveRole, setCurrentView } = useAppContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleDemoLogin = (role: Role) => {
    setActiveRole(role);
    if (role === 'STUDENT') {
      setCurrentView('POLAR_EXPLORER');
    } else {
      setCurrentView('COMMAND_HOME');
    }
  };

  const handleStandardLogin = (e: React.FormEvent) => {
    e.preventDefault();
    handleDemoLogin('COMMANDER');
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-4">
      <div className="absolute inset-0 scanlines opacity-50 pointer-events-none z-10"></div>
      
      <div className="z-20 w-full max-w-md">
        <h1 className="text-4xl font-pixel-heading text-center mb-8 text-3d">POLAR OPS<br/><span className="text-pixel-success">COMMANDER</span></h1>
        
        <div className="pixel-panel mb-8">
          <form onSubmit={handleStandardLogin} className="flex flex-col gap-4">
            <div>
              <label className="block mb-2 font-pixel text-sm">Email</label>
              <input 
                type="email" 
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full bg-white text-black border-4 border-black p-2 font-pixel outline-none focus:border-pixel-primary"
              />
            </div>
            <div>
              <label className="block mb-2 font-pixel text-sm">Password</label>
              <input 
                type="password" 
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full bg-white text-black border-4 border-black p-2 font-pixel outline-none focus:border-pixel-primary"
              />
            </div>
            <button type="submit" className="pixel-btn pixel-btn-primary mt-2">
              [ LOGIN ]
            </button>
          </form>
        </div>

        <div className="border-t-2 border-gray-700 pt-6">
          <h3 className="text-center font-pixel text-sm text-gray-400 mb-4">DEMO ACCESS (SIH)</h3>
          <div className="grid grid-cols-2 gap-4">
            <button onClick={() => handleDemoLogin('LOGISTICS')} className="pixel-btn bg-blue-900 text-white text-xs py-2">
              [ Logistics Officer ]
            </button>
            <button onClick={() => handleDemoLogin('COMMANDER')} className="pixel-btn bg-red-900 text-white text-xs py-2">
              [ Expedition Cmdr ]
            </button>
            <button onClick={() => handleDemoLogin('TRAINER')} className="pixel-btn bg-green-900 text-white text-xs py-2">
              [ Trainer ]
            </button>
            <button onClick={() => handleDemoLogin('STUDENT')} className="pixel-btn bg-yellow-900 text-black text-xs py-2">
              [ Student ]
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
