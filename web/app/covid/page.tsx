import { CovidChart } from "@/components/CovidChart";
import { covid } from "@/lib/data";
import { formatPct, formatThousands } from "@/lib/format";

export default function CovidPage() {
  const snapshot = [...covid.snapshot].sort((a, b) => (a.pctChange ?? 0) - (b.pctChange ?? 0));
  const worst = snapshot[0];
  const best = snapshot[snapshot.length - 1];

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">COVID-19 impact by industry</h1>
        <p className="text-slate-600 mt-1">
          Private-sector wage employment, 2019 vs. 2021 vs. latest year ({covid.latestYear}).
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-5">
          <div className="text-xs uppercase tracking-wide text-rose-600 font-semibold">
            Hardest hit 2019→2021
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">{worst?.industry}</div>
          <div className="text-rose-700 font-medium">{formatPct(worst?.pctChange)}</div>
        </div>
        <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5">
          <div className="text-xs uppercase tracking-wide text-emerald-600 font-semibold">
            Most resilient 2019→2021
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">{best?.industry}</div>
          <div className="text-emerald-700 font-medium">+{formatPct(best?.pctChange)}</div>
        </div>
      </div>

      <section className="bg-white rounded-xl border border-slate-200 p-6 mb-10">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">
          Employment levels: pre-COVID vs. COVID vs. latest
        </h2>
        <CovidChart rows={covid.snapshot} latestYear={covid.latestYear} />
      </section>

      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">Detailed change</h2>
        <table className="w-full text-sm">
          <thead className="text-left text-slate-500 border-b border-slate-200">
            <tr>
              <th className="py-2">Industry</th>
              <th className="py-2 text-right">2019</th>
              <th className="py-2 text-right">2021</th>
              <th className="py-2 text-right">Latest</th>
              <th className="py-2 text-right">Δ 2019→2021</th>
            </tr>
          </thead>
          <tbody>
            {snapshot.map((r) => (
              <tr key={r.industry} className="border-b border-slate-100">
                <td className="py-2 font-medium text-slate-800">{r.industry}</td>
                <td className="py-2 text-right">{formatThousands(r.y2019)}</td>
                <td className="py-2 text-right">{formatThousands(r.y2021)}</td>
                <td className="py-2 text-right">{formatThousands(r.latest)}</td>
                <td
                  className={`py-2 text-right font-medium ${
                    (r.pctChange ?? 0) < 0 ? "text-rose-600" : "text-emerald-600"
                  }`}
                >
                  {formatPct(r.pctChange)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}