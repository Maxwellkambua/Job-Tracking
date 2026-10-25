import Link from "next/link";
import { KpiCard } from "@/components/KpiCard";
import { TrendChart } from "@/components/TrendChart";
import { RankingChart } from "@/components/RankingChart";
import { kpis, timeseries, rankings } from "@/lib/data";
import { formatMillions, formatPct } from "@/lib/format";

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <header className="mb-10">
        <h1 className="text-4xl font-bold text-slate-900">
          Kenya Employment by Industry
        </h1>
        <p className="text-slate-600 mt-2 max-w-2xl">
          Formal wage employment trends from KNBS Economic Surveys.
          Updated through {kpis.latestYear}.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
        <KpiCard
          label="Formal Employment"
          value={formatMillions(kpis.totalEmploymentThousands)}
          hint={`as of ${kpis.latestYear}`}
        />
        <KpiCard
          label="YoY Growth"
          value={formatPct(kpis.yoyGrowthPct)}
          hint="year-over-year"
          trend={kpis.yoyGrowthPct >= 0 ? "up" : "down"}
        />
        <KpiCard
          label="Unemployment Rate"
          value={formatPct(kpis.unemploymentRate)}
          hint="national, all sectors"
        />
        <KpiCard
          label="Informal Sector"
          value={formatPct(kpis.informalSharePct)}
          hint="of total employment"
        />
      </div>

      <section className="bg-white rounded-xl border border-slate-200 p-6 mb-10">
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="text-xl font-semibold text-slate-900">Employment over time</h2>
          <Link href="/industries" className="text-sm text-brand-600 hover:underline">
            Explore all industries →
          </Link>
        </div>
        <TrendChart data={timeseries} />
      </section>

      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">
          Top industries ({kpis.latestYear})
        </h2>
        <RankingChart data={rankings} />
      </section>
    </div>
  );
}