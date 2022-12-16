import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export const PredictionsLineChart = (data) => {
  data = data.data.map((d) => {
    return {
      date: d.date,
      prediction:
        d.prediction === null
          ? null
          : Math.round(d.prediction * 100 * 100) / 100,
      actual_percent_change:
        d.actual_percent_change === null
          ? null
          : Math.round(d.actual_percent_change * 100 * 100) / 100,
    };
  });

  return (
    <ResponsiveContainer width={"95%"} height={800}>
      <LineChart
        data={data}
        margin={{
          top: 50,
          right: 55,
          left: 55,
          bottom: 50,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" dy={20} />
        <YAxis
          tickFormatter={(tick) => {
            return `${tick}%`;
          }}
          dx={-10}
        />
        <Tooltip formatter={(value) => `${value}%`} />
        <Legend
          wrapperStyle={{
            paddingTop: "40px",
          }}
        />
        <Line
          name="Predicted Return"
          type="monotone"
          dataKey="prediction"
          stroke="#C20114"
          activeDot={{ r: 8 }}
        />
        <Line
          name="Actual Observed Return"
          type="monotone"
          dataKey="actual_percent_change"
          stroke="#008DD5"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PredictionsLineChart;
