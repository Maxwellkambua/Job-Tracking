import timeseriesJson from "@/data/timeseries.json";
import kpisJson from "@/data/kpis.json";
import rankingsJson from "@/data/rankings.json";
import covidJson from "@/data/covid.json";
import type { Kpis, RankingRow, TimeseriesPoint, CovidPayload } from "./types";

export const kpis = kpisJson as Kpis;
export const timeseries = timeseriesJson as TimeseriesPoint[];
export const rankings = rankingsJson as RankingRow[];
export const covid = covidJson as CovidPayload;

export function industriesList(): string[] {
  return Array.from(new Set(timeseries.map((d) => d.industry))).sort();
}

export function yearsList(): number[] {
  return Array.from(new Set(timeseries.map((d) => d.year))).sort();
}

export function topIndustries(n = 5, sector: "Total" = "Total"): string[] {
  const latest = kpis.latestYear;
  return timeseries
    .filter((d) => d.year === latest && d.sector === sector && d.value != null)
    .sort((a, b) => (b.value ?? 0) - (a.value ?? 0))
    .slice(0, n)
    .map((d) => d.industry);
}

export function pivotForChart(selectedIndustries: string[]) {
  const rows = new Map<number, Record<string, number | string>>();
  for (const d of timeseries) {
    if (d.sector !== "Total" || !selectedIndustries.includes(d.industry)) continue;
    if (d.value == null) continue;
    if (!rows.has(d.year)) rows.set(d.year, { year: d.year });
    rows.get(d.year)![d.industry] = d.value;
  }
  return Array.from(rows.values()).sort((a, b) => Number(a.year) - Number(b.year));
}