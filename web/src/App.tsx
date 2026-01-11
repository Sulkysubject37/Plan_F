import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import Home from './pages/Home';
import Story from './pages/Story';
import Calendar from './pages/Calendar';
import Simulator from './pages/Simulator';

function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <Navigation />
        <div className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/story" element={<Story />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/simulator" element={<Simulator />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
