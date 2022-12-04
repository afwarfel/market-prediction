import logo from './logo.svg';
import './App.css';
import PredictionsLineChart from './PredictionsLineChart'
import regressor_inferences from './data/regressor_inferences.json';

const App = () => {

  const data = regressor_inferences

  return (
    <>
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
          <h1>
            See daily predictions below:
          </h1>
        <PredictionsLineChart data={data}/>
        <hr/>
        <a style={{color:'lightblue'}} href='https://github.com/afwarfel/market-prediction/blob/main/machine_learning/random_forest_regressor.ipynb'>Review details of the model here!</a>
      </header>
    </div>
    </>
  );
}

export default App;
