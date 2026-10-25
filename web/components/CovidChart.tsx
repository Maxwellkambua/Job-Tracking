"use client";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid,
} from "recharts";
import type { CovidRow } from "@/lib/types";

export function CovidChart({ rows, latestYear }: { rows: CovidRow[]; latestYear: number }) {
  const data = rows
    .filter((r) => r.y2019 != null)
    .sort((a, b) => (b.y2021 ?? 0) - (a.y2021 ?? 0));

  return (
    <div style={{ width: "100%", height: Math.max(400, data.length * 30) }}>
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis type="number" fontSize={12} unit="K" />
          <YAxis type="category" dataKey="industry" width={200} fontSize={12} />
          <Tooltip formatter={(v: number) => `${v?.toLocaleString() ?? "—"}K`} />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          <Bar dataKey="y2019" name="2019 (pre-COVID)" fill="#94a3b8" />
          <Bar dataKey="y2021" name="2021 (COVID)" fill="#f59e0b" />
          <Bar dataKey="latest" name={`${latestYear} (latest)`} fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}