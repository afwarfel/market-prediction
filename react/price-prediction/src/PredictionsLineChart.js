import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const PredictionsLineChart = (data) => {

  data = data.data.map((d) => {
    return {
      date: d.date,
      prediction: d.prediction===null?null:(Math.round((d.prediction*100)*100)/100),
      nasdaq_percent_change: d.nasdaq_percent_change===null?null:(Math.round((d.nasdaq_percent_change*100)*100)/100)
    }})

    console.log('data',data)

    return (
      <ResponsiveContainer width={800} height={800}>
        <LineChart
          width={1500}
          height={1300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" dy={20}/>
          <YAxis tickFormatter={(tick) => {
            return `${tick}%`;
          }} dx={-10}/>
          <Tooltip formatter={(value) => `${value}%`}/>
          <Legend wrapperStyle={{
        paddingTop: "40px"
    }}/>
          <Line name='Predicted NASDAQ Return' type="monotone" dataKey="prediction" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line name='Actual NASDAQ Return' type="monotone" dataKey="nasdaq_percent_change" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    );};

export default PredictionsLineChart;