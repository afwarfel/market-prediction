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
      experienced_cumulative_return_based_on_model:
        d.experienced_cumulative_return_based_on_model === null
          ? null
          : Math.round(d.experienced_cumulative_return_based_on_model * 100 * 100) / 100,
      experienced_cumulative_return_based_on_buy_hold:
        d.experienced_cumulative_return_based_on_buy_hold === null
          ? null
          : Math.round(d.experienced_cumulative_return_based_on_buy_hold * 100 * 100) / 100,
      outperformance:
        d.outperformance === null
          ? null
          : Math.round(d.outperformance * 100 * 100) / 100,
    };
  });

  console.log(data)

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
          name="Cumulative Return Based on Model"
          type="monotone"
          dataKey="experienced_cumulative_return_based_on_model"
          stroke="#C20114"
          activeDot={{ r: 8 }}
        />
        <Line
          name="Cumulative Return Based on Buy and Hold"
          type="monotone"
          dataKey="experienced_cumulative_return_based_on_buy_hold"
          stroke="#008DD5"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PredictionsLineChart;
