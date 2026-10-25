"use client";
import { useMemo, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import type { TimeseriesPoint } from "@/lib/types";
import { pivotForChart, topIndustries, industriesList } from "@/lib/data";

const COLORS = ["#2563eb", "#10b981", "#f59e0b", "#ef4444",
                "#8b5cf6", "#ec4899", "#14b8a6", "#f97316"];

export function TrendChart({ data }: { data: TimeseriesPoint[] }) {
  const [selected, setSelected] = useState<string[]>(() => topIndustries(5));
  const all = useMemo(() => industriesList(), []);
  const chartData = useMemo(() => pivotForChart(selected), [selected]);

  const toggle = (industry: string) => {
    setSelected((s) =>
      s.includes(industry) ? s.filter((x) => x !== industry) : [...s, industry]
    );
  };

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-4">
        {all.map((industry) => {
          const active = selected.includes(industry);
          return (
            <button
              key={industry}
              onClick={() => toggle(industry)}
              className={`text-xs px-2.5 py-1 rounded-full border transition ${
                active
                  ? "bg-brand-600 text-white border-brand-600"
                  : "bg-white text-slate-600 border-slate-300 hover:border-brand-500"
              }`}
            >
              {industry}
            </button>
          );
        })}
      </div>
      <div style={{ width: "100%", height: 360 }}>
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="year" fontSize={12} />
            <YAxis fontSize={12} unit="K" />
            <Tooltip
              formatter={(v: number) => `${v.toLocaleString()}K`}
              labelFormatter={(l) => `Year ${l}`}
            />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            {selected.map((industry, i) => (
              <Line
                key={industry}
                type="monotone"
                dataKey={industry}
                stroke={COLORS[i % COLORS.length]}
                strokeWidth={2}
                dot={false}
                connectNulls
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}