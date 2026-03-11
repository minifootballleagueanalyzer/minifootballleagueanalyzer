import { BrowserRouter } from 'react-router-dom';
import Header from './components/Header/Header';
import Home from './pages/Home';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Home />
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
