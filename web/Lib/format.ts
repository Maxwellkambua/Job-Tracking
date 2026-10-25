export const formatThousands = (n: number | null) =>
  n == null ? "—" : `${n.toLocaleString("en-KE", { maximumFractionDigits: 1 })}K`;

export const formatMillions = (thousands: number | null) =>
  thousands == null ? "—" : `${(thousands / 1000).toFixed(2)}M`;

export const formatPct = (n: number | null, digits = 1) =>
  n == null ? "—" : `${n.toFixed(digits)}%`;