"use client";

import { useState } from "react";
import { RiskBadge } from "./RiskBadge";
import type { RepairOutput } from "@/types/repair";

interface Props {
  output: RepairOutput;
}

function Section({
  title,
  defaultOpen = false,
  children,
}: {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="border border-gray-100 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 text-sm font-medium text-gray-700 hover:bg-gray-100 transition-colors"
      >
        {title}
        <span className="text-gray-400">{open ? "▲" : "▼"}</span>
      </button>
      {open && <div className="px-4 py-3">{children}</div>}
    </div>
  );
}

function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? "bg-green-500" : pct >= 40 ? "bg-amber-400" : "bg-red-400";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs text-gray-500 w-10 text-right">{pct}%</span>
    </div>
  );
}

export function RepairCard({ output }: Props) {
  const isCritical = output.risk_level === "critical";

  return (
    <div className="flex flex-col gap-3">
      {/* Header — always visible */}
      <div className="rounded-xl border border-gray-200 bg-white p-4 flex flex-col gap-2">
        <div className="flex items-start justify-between gap-2 flex-wrap">
          <h2 className="text-lg font-semibold text-gray-900">{output.detected_item}</h2>
          <RiskBadge level={output.risk_level} />
        </div>
        <p className="text-sm text-gray-600">{output.problem_summary}</p>
        <div className="flex gap-3 text-xs text-gray-400">
          <span className="capitalize">{output.category.replace("_", " ")}</span>
          <span>·</span>
          <span className="capitalize">{output.repair_difficulty.replace("_", " ")}</span>
        </div>
        <div className="mt-1">
          <p className="text-xs text-gray-400 mb-1">Confidence</p>
          <ConfidenceBar value={output.confidence_overall} />
        </div>
      </div>

      {/* Critical banner */}
      {isCritical && (
        <div className="rounded-xl border-2 border-red-300 bg-red-50 p-4 flex flex-col gap-2">
          <p className="font-semibold text-red-700">⛔ Do not attempt this repair</p>
          <ul className="text-sm text-red-600 list-disc list-inside space-y-1">
            {output.stop_conditions.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
          {output.next_best_test && (
            <p className="text-sm text-red-700 mt-1">
              <span className="font-medium">Next step:</span> {output.next_best_test}
            </p>
          )}
        </div>
      )}

      {/* Observations */}
      <Section title="👁 Observations" defaultOpen>
        <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
          {output.visible_observations.map((o, i) => <li key={i}>{o}</li>)}
        </ul>
      </Section>

      {/* Likely Causes */}
      <Section title="🔍 Likely Causes" defaultOpen>
        <div className="flex flex-col gap-2">
          {output.likely_causes.map((c, i) => (
            <div key={i} className="flex items-start gap-3">
              <span className="mt-1 inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700 whitespace-nowrap">
                {Math.round(c.confidence * 100)}%
              </span>
              <div>
                <p className="text-sm font-medium text-gray-800">{c.description}</p>
                <p className="text-xs text-gray-500">{c.evidence}</p>
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* Clarifying Questions */}
      {output.clarifying_questions.length > 0 && (
        <Section title="❓ Clarifying Questions" defaultOpen>
          <ol className="text-sm text-gray-700 list-decimal list-inside space-y-1">
            {output.clarifying_questions.map((q, i) => <li key={i}>{q}</li>)}
          </ol>
        </Section>
      )}

      {/* Tools Needed */}
      <Section title="🔧 Tools Needed">
        <div className="flex flex-wrap gap-2">
          {output.tools_needed.map((t, i) => (
            <span key={i} className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700">
              {t}
            </span>
          ))}
        </div>
      </Section>

      {/* Next Best Test */}
      {!isCritical && (
        <Section title="🧪 Next Best Test">
          <p className="text-sm text-indigo-700 bg-indigo-50 rounded-lg px-3 py-2">
            {output.next_best_test}
          </p>
        </Section>
      )}

      {/* Repair Steps */}
      {!isCritical && (
        <Section title="🛠 Repair Steps" defaultOpen>
          <div className="flex flex-col gap-3">
            {output.step_by_step_repair.map((s) => (
              <div key={s.step_number} className="flex gap-3">
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">
                  {s.step_number}
                </span>
                <div className="flex flex-col gap-1">
                  <p className="text-sm text-gray-800">{s.instruction}</p>
                  {s.warning && (
                    <p className="text-xs text-amber-700 bg-amber-50 rounded px-2 py-1">
                      ⚠ {s.warning}
                    </p>
                  )}
                  {s.expected_outcome && (
                    <p className="text-xs text-green-700 bg-green-50 rounded px-2 py-1">
                      ✓ {s.expected_outcome}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Stop Conditions */}
      {!isCritical && output.stop_conditions.length > 0 && (
        <Section title="🛑 Stop Conditions">
          <ul className="text-sm text-red-600 bg-red-50 rounded-lg p-3 list-disc list-inside space-y-1">
            {output.stop_conditions.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </Section>
      )}

      {/* Prevention */}
      <Section title="🛡 Prevention">
        <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
          {output.prevention.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </Section>

      {/* Sources */}
      <Section title="📚 Sources">
        <div className="flex flex-wrap gap-2">
          {output.retrieved_sources.map((src, i) => (
            <span key={i} className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-600">
              {src.title} · {Math.round(src.relevance_score * 100)}%
            </span>
          ))}
        </div>
      </Section>
    </div>
  );
}
