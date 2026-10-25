"use client";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from "recharts";
import type { RankingRow } from "@/lib/types";

const MAX_ROWS = 12;

export function RankingChart({ data }: { data: RankingRow[] }) {
  const rows = data
    .filter((d) => d.employmentThousands != null)
    .slice(0, MAX_ROWS);

  return (
    <div style={{ width: "100%", height: Math.max(280, rows.length * 28) }}>
      <ResponsiveContainer>
        <BarChart
          data={rows}
          layout="vertical"
          margin={{ left: 20, right: 20 }}
        >
          <XAxis type="number" fontSize={12} unit="K" />
          <YAxis
            type="category"
            dataKey="industry"
            width={200}
            fontSize={12}
          />
          <Tooltip formatter={(v: number) => `${v.toLocaleString()}K`} />
          <Bar dataKey="employmentThousands" radius={[0, 4, 4, 0]}>
            {rows.map((_, i) => (
              <Cell key={i} fill={i < 3 ? "#2563eb" : "#93c5fd"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}