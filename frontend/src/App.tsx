
import { AppProvider, useAppContext } from './AppContext';
import LandingPage from './views/LandingPage/index';
import Login from './views/Login';
import MainLayout from './views/MainLayout';

function AppRouter() {
  const { currentView } = useAppContext();

  if (currentView === 'LANDING') return <LandingPage />;
  if (currentView === 'LOGIN') return <Login />;
  return <MainLayout />;
}

export default function App() {
  return (
    <AppProvider>
      <AppRouter />
    </AppProvider>
  );
}
