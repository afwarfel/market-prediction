import logo from './logo.svg';
import './App.css';
import LineChartW from './LineChartW'

function App() {
  return (
    <>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          See daily predictions below:
        </p>
      <LineChartW/>
      </header>
    </div>
    </>
  );
}

export default App;
