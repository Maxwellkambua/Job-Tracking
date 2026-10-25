import { RankingChart } from "@/components/RankingChart";
import { TrendChart } from "@/components/TrendChart";
import { timeseries, rankings, kpis } from "@/lib/data";
import { formatThousands, formatPct } from "@/lib/format";

export default function IndustriesPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Industries</h1>
        <p className="text-slate-600 mt-1">
          Toggle industries below to compare their formal employment trajectories.
        </p>
      </header>

      <section className="bg-white rounded-xl border border-slate-200 p-6 mb-10">
        <TrendChart data={timeseries} />
      </section>

      <section className="bg-white rounded-xl border border-slate-200 p-6 mb-10">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">
          Ranking ({kpis.latestYear})
        </h2>
        <RankingChart data={rankings} />
      </section>

      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">All industries</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-slate-500 border-b border-slate-200">
              <tr>
                <th className="py-2">Rank</th>
                <th className="py-2">Industry</th>
                <th className="py-2 text-right">Employment ({kpis.latestYear})</th>
                <th className="py-2 text-right">Share</th>
              </tr>
            </thead>
            <tbody>
              {rankings.map((r) => (
                <tr key={r.industry} className="border-b border-slate-100">
                  <td className="py-2 text-slate-400">{r.rank}</td>
                  <td className="py-2 font-medium text-slate-800">{r.industry}</td>
                  <td className="py-2 text-right">{formatThousands(r.employmentThousands)}</td>
                  <td className="py-2 text-right">{formatPct(r.sharePct)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}