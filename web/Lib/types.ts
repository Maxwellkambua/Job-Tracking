export type TimeseriesPoint = {
  year: number;
  industry: string;
  sector: "Private" | "Public" | "Total";
  value: number | null;
};

export type Kpis = {
  latestYear: number;
  totalEmploymentThousands: number;
  yoyGrowthPct: number;
  unemploymentRate: number | null;
  informalSharePct: number | null;
  topIndustry: string;
  topIndustryValue: number;
};

export type RankingRow = {
  rank: number;
  industry: string;
  employmentThousands: number | null;
  sharePct: number | null;
};

export type CovidRow = {
  industry: string;
  y2019: number | null;
  y2020: number | null;
  y2021: number | null;
  latest: number | null;
  pctChange: number | null;
};

export type CovidPayload = {
  latestYear: number;
  snapshot: CovidRow[];
};