"use client";

import { useState, useRef } from "react";
import { analyzeRepair } from "@/lib/api";
import type { Category, RepairOutput } from "@/types/repair";

interface Props {
  onResult: (output: RepairOutput) => void;
  deviceId: string;
}

const CATEGORIES: { label: string; value: Category | null }[] = [
  { label: "Auto-detect", value: null },
  { label: "Robotics", value: "robotics" },
  { label: "Electronics", value: "electronics" },
  { label: "Emergency", value: "emergency_equipment" },
  { label: "Household", value: "household" },
];

export function DiagnoseForm({ onResult, deviceId }: Props) {
  const [symptom, setSymptom] = useState("");
  const [category, setCategory] = useState<Category | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  function startListening() {
    const SR =
      (window as typeof window & { webkitSpeechRecognition?: typeof SpeechRecognition })
        .webkitSpeechRecognition ?? window.SpeechRecognition;
    if (!SR) {
      setError("Speech recognition not supported in this browser.");
      return;
    }
    const rec = new SR();
    recognitionRef.current = rec;
    rec.lang = "en-US";
    rec.continuous = false;
    rec.interimResults = false;
    rec.onstart = () => setListening(true);
    rec.onresult = (e: SpeechRecognitionEvent) => {
      const t = e.results[0][0].transcript;
      setSymptom((prev) => (prev ? `${prev} ${t}` : t));
    };
    rec.onerror = () => setListening(false);
    rec.onend = () => setListening(false);
    rec.start();
  }

  async function handleSubmit() {
    if (!symptom.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const output = await analyzeRepair({
        symptom: symptom.trim(),
        category: category ?? null,
        device_id: deviceId,
      });
      onResult(output);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <textarea
        value={symptom}
        onChange={(e) => setSymptom(e.target.value)}
        placeholder="Describe the problem — e.g. 'servo is buzzing at 90°'"
        rows={3}
        disabled={loading}
        className="w-full rounded-xl border border-gray-200 p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
      />

      {/* Category pills */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map(({ label, value }) => (
          <button
            key={label}
            onClick={() => setCategory(value)}
            disabled={loading}
            className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
              category === value
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            } disabled:opacity-50`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Action row */}
      <div className="flex gap-2">
        <button
          onClick={startListening}
          disabled={loading}
          className={`rounded-xl px-4 py-2 text-sm font-medium transition-colors ${
            listening
              ? "bg-red-500 text-white animate-pulse"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          } disabled:opacity-50`}
        >
          {listening ? "🔴 Listening…" : "🎤 Speak"}
        </button>
        <button
          onClick={handleSubmit}
          disabled={loading || !symptom.trim()}
          className="flex-1 rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              Analyzing with FieldFix AI…
            </span>
          ) : (
            "Analyze →"
          )}
        </button>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}
    </div>
  );
}
