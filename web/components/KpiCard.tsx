type Props = {
  label: string;
  value: string;
  hint?: string;
  trend?: "up" | "down" | "flat";
};

export function KpiCard({ label, value, hint, trend }: Props) {
  const trendColor =
    trend === "up" ? "text-emerald-600" : trend === "down" ? "text-rose-600" : "text-slate-400";
  const trendSymbol = trend === "up" ? "▲" : trend === "down" ? "▼" : "";
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <div className="text-sm text-slate-500">{label}</div>
      <div className="mt-2 text-3xl font-bold text-slate-900 flex items-baseline gap-2">
        {value}
        {trendSymbol && <span className={`text-sm ${trendColor}`}>{trendSymbol}</span>}
      </div>
      {hint && <div className="text-xs text-slate-400 mt-1">{hint}</div>}
    </div>
  );
}