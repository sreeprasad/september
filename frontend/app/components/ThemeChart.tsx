"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const COLORS = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

export default function ThemeChart({ themes }: { themes: any }) {
  if (!themes || !themes.frequency_breakdown) return null;

  const data = Object.entries(themes.frequency_breakdown).map(([name, value], index) => ({
    name,
    value: (value as number) * 100, // Convert to percentage
  }));

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">Topic Distribution</h3>
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
                formatter={(value: number) => `${value.toFixed(1)}%`}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend verticalAlign="bottom" height={36}/>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 p-3 bg-indigo-50 rounded-lg">
          <p className="text-sm text-indigo-800">
              <strong>Insight:</strong> Primary focus is on <span className="capitalize">{themes.primary}</span>.
          </p>
      </div>
    </div>
  );
}
