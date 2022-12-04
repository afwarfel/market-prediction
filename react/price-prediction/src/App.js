import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import PredictionsLineChart from './PredictionsLineChart'

const App = () => {
  const [regressor_inferences, set_regressor_inferences] = useState([]);
  // fetch('https://stock-market-prediction-front-end.s3.us-west-2.amazonaws.com/data/regressor_inferences.json', { mode: 'no-cors' })
  //   .then(response => console.log(response))

    function getJson() {
      return fetch('https://stock-market-prediction-front-end.s3.us-west-2.amazonaws.com/data/regressor_inferences.json')
        .then(response => response.json())
        .catch(error => {
          console.error(error);
        });
    }

    useEffect(() => {
      getJson().then(regressor_inferences => set_regressor_inferences(regressor_inferences));
    }, []);


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
        <br/>
        <a style={{color:'lightblue',padding:'50px'}} href='https://github.com/afwarfel/market-prediction/blob/main/machine_learning/random_forest_regressor.ipynb'>Review details of the model here!</a>
      </header>
    </div>
    </>
  );
}

export default App;
