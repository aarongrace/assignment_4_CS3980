import { Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import './globals.css';
import Profile from './pages/profile/Profile';
import Welcome from './pages/welcome/Welcome';

function App() {

  return (
    <div className="App">
      <Navbar />
      <main className="App-main">
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
