"use client";

import { useEffect, useState } from "react";
import { getDeviceHistory } from "@/lib/api";
import { RiskBadge } from "./RiskBadge";
import type { RepairOutput } from "@/types/repair";

interface Props {
  deviceId: string;
  onSelect: (output: RepairOutput) => void;
}

export function SessionHistory({ deviceId, onSelect }: Props) {
  const [history, setHistory] = useState<RepairOutput[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!deviceId) return;
    setLoading(true);
    getDeviceHistory(deviceId)
      .then(setHistory)
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, [deviceId]);

  if (loading) {
    return <p className="text-sm text-gray-400 px-1">Loading history…</p>;
  }

  if (history.length === 0) {
    return (
      <p className="text-sm text-gray-400 px-1">
        No repairs yet. Describe a problem above to get started.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {history.map((item, i) => (
        <button
          key={i}
          onClick={() => onSelect(item)}
          className="text-left rounded-xl border border-gray-100 bg-white p-3 hover:border-blue-200 hover:bg-blue-50 transition-colors"
        >
          <div className="flex items-center justify-between gap-2 flex-wrap">
            <span className="text-sm font-medium text-gray-800 truncate max-w-[180px]">
              {item.detected_item}
            </span>
            <RiskBadge level={item.risk_level} />
          </div>
          <p className="mt-1 text-xs text-gray-500 line-clamp-2">{item.problem_summary}</p>
        </button>
      ))}
    </div>
  );
}
