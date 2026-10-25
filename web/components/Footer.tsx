import kpis from "@/data/kpis.json";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 mt-16 py-8 text-sm text-slate-500">
      <div className="max-w-6xl mx-auto px-4 space-y-1">
        <p>
          Source: <strong>KNBS Economic Survey</strong> — Wage Employment by Industry.
          Latest year: <strong>{kpis.latestYear}</strong>.
        </p>
        <p>
          Note: figures reflect <em>formal wage employment</em>, not unemployment rates by industry.
        </p>
      </div>
    </footer>
  );
}