import logo from './logo.svg';
import './App.css';
import LineChartW from './LineChartW'

function App() {
  return (
    <>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div>This is a deployment test</div>
        <h1>
          See daily predictions below:
        </h1>
      <LineChartW/>
      </header>
    </div>
    </>
  );
}

export default App;
