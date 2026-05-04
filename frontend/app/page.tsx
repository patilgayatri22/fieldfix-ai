"use client";

import { useEffect, useRef, useState } from "react";
import { DiagnoseForm } from "@/components/DiagnoseForm";
import { RepairCard } from "@/components/RepairCard";
import { SessionHistory } from "@/components/SessionHistory";
import type { RepairOutput } from "@/types/repair";

const DEMO_PILLS = [
  { label: "Servo buzzing", symptom: "servo motor is buzzing at 90 degrees" },
  { label: "Pi not booting", symptom: "raspberry pi not booting, no display" },
  { label: "Dead flashlight", symptom: "flashlight completely dead, new batteries installed" },
  { label: "Loose hinge", symptom: "cabinet door hinge is loose and squeaking" },
];

export default function HomePage() {
  const [deviceId, setDeviceId] = useState<string>("");
  const [result, setResult] = useState<RepairOutput | null>(null);
  const [historyKey, setHistoryKey] = useState(0);
  const formRef = useRef<{ setSymptom?: (s: string) => void }>(null);

  // SSR-safe localStorage device ID
  useEffect(() => {
    let id = localStorage.getItem("fieldfix_device_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("fieldfix_device_id", id);
    }
    setDeviceId(id);
  }, []);

  function handleResult(output: RepairOutput) {
    setResult(output);
    setHistoryKey((k) => k + 1); // refresh history
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-gray-200 bg-white px-4 py-3">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-gray-900">🔧 FieldFix AI</h1>
            <p className="text-xs text-gray-500">Offline repair copilot · Powered by Gemma</p>
          </div>
          <span className="flex items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500" />
            Offline ready
          </span>
        </div>
      </header>

      {/* Main layout */}
      <main className="mx-auto max-w-6xl px-4 py-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
          {/* Left panel */}
          <div className="flex flex-col gap-4 lg:w-80 lg:shrink-0">
            {/* Diagnose card */}
            <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
              <h2 className="mb-3 text-sm font-semibold text-gray-700">Describe the problem</h2>
              {deviceId && (
                <DiagnoseForm
                  onResult={handleResult}
                  deviceId={deviceId}
                />
              )}
            </div>

            {/* History card */}
            <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
              <h2 className="mb-3 text-sm font-semibold text-gray-700">Recent repairs</h2>
              {deviceId && (
                <SessionHistory
                  key={historyKey}
                  deviceId={deviceId}
                  onSelect={setResult}
                />
              )}
            </div>
          </div>

          {/* Right panel */}
          <div className="flex-1">
            {result ? (
              <RepairCard output={result} />
            ) : (
              <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-gray-200 bg-white py-16 px-8 text-center">
                <span className="text-5xl mb-4">🔧</span>
                <p className="text-gray-500 mb-6">Describe a problem to get started</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {DEMO_PILLS.map(({ label, symptom }) => (
                    <button
                      key={label}
                      onClick={() => {
                        // Pre-fill by dispatching a custom event the form can listen to
                        // (simple approach: just set result via a quick analyze call)
                        window.dispatchEvent(
                          new CustomEvent("fieldfix:prefill", { detail: symptom })
                        );
                      }}
                      className="rounded-full border border-blue-200 bg-blue-50 px-4 py-1.5 text-sm text-blue-700 hover:bg-blue-100 transition-colors"
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
