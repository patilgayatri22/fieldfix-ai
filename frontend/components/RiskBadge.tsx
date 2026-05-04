import type { RiskLevel } from "@/types/repair";

interface Props {
  level: RiskLevel;
}

const CONFIG: Record<RiskLevel, { label: string; className: string }> = {
  low: {
    label: "✓ Low Risk",
    className:
      "bg-green-100 text-green-800 border border-green-200",
  },
  medium: {
    label: "⚡ Medium Risk",
    className:
      "bg-amber-100 text-amber-800 border border-amber-200",
  },
  high: {
    label: "⚠️ High Risk",
    className:
      "bg-orange-100 text-orange-800 border border-orange-200",
  },
  critical: {
    label: "⛔ Do Not Attempt",
    className:
      "bg-red-100 text-red-800 border border-red-300 font-semibold",
  },
};

export function RiskBadge({ level }: Props) {
  const { label, className } = CONFIG[level];
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-0.5 text-sm ${className}`}
    >
      {label}
    </span>
  );
}
