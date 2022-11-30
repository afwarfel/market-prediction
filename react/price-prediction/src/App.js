import logo from './logo.svg';
import './App.css';
import LineChartW from './LineChartW'
import data from 'inferences.csv'

function App() {
  return (
    <>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
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
