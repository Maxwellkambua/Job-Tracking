import Link from "next/link";
import { kpis } from "@/lib/data";

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10 prose prose-slate">
      <h1 className="text-3xl font-bold text-slate-900 mb-6">About this dashboard</h1>

      <h2 className="text-xl font-semibold mt-8 mb-2">Data source</h2>
      <p className="text-slate-700">
        All figures come from the <strong>Kenya National Bureau of Statistics (KNBS)</strong>{" "}
        <em>Economic Survey</em>, Chapter 3 (<em>Employment, Earnings and Consumer Price Indices</em>),
        Table 3.2 — Wage Employment by Industry and Sector. The latest observation is from{" "}
        <strong>{kpis.latestYear}</strong>. Data is annual.
      </p>

      <h2 className="text-xl font-semibold mt-8 mb-2">What this measures</h2>
      <p className="text-slate-700">
        The figures show <strong>formal wage employment</strong> — the number of people
        in formal-sector jobs, in thousands — broken down by industry and sector
        (Private / Public / Total).
      </p>

      <h2 className="text-xl font-semibold mt-8 mb-2">What this does NOT measure</h2>
      <ul className="list-disc pl-5 text-slate-700 space-y-1">
        <li>
          It is <strong>not an unemployment rate</strong>. Kenya&apos;s unemployment rate
          is reported separately (currently ~{kpis.unemploymentRate?.toFixed(1) ?? "—"}%).
        </li>
        <li>
          The <strong>informal sector</strong> (~{kpis.informalSharePct?.toFixed(0) ?? "—"}% of
          total employment) is not included in these wage-employment tables.
        </li>
        <li>
          A shrinking industry may reflect formal job losses, but workers often move into
          informality rather than unemployment — so declining wage employment is not the
          same as rising unemployment.
        </li>
      </ul>

      <h2 className="text-xl font-semibold mt-8 mb-2">Update cadence</h2>
      <p className="text-slate-700">
        KNBS publishes a new Economic Survey roughly once a year (typically around May).
        This dashboard is rebuilt when a new survey is ingested.
      </p>

      <p className="mt-8">
        <Link href="/" className="text-brand-600 hover:underline">← Back to overview</Link>
      </p>
    </div>
  );
}