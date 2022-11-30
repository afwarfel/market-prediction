import logo from './logo.svg';
import './App.css';
import LineChartW from './LineChartW'
import data from './data/inferences.json'

function App() {

  console.log(data)

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
