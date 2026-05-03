/**
 * FieldFix AI — Web Speech API snippet for Next.js
 *
 * Works on iOS Safari (webkit prefix) and Chrome/Edge.
 * Drop the hook into your component and wire up `symptom` state.
 *
 * Usage:
 *   const { symptom, isListening, startListening, error } = useSpeechInput()
 *   <button onClick={startListening}>{isListening ? "Listening…" : "🎙 Speak"}</button>
 *   <p>{symptom}</p>
 */

"use client";

import { useState, useCallback, useRef } from "react";

export function useSpeechInput() {
  const [symptom, setSymptom] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);

  const startListening = useCallback(() => {
    // iOS Safari uses webkit prefix; Chrome/Edge use standard SpeechRecognition
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError("Speech recognition not supported on this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "en-US";
    recognition.continuous = false;       // single utterance per tap
    recognition.interimResults = false;   // only final result
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setSymptom(transcript);
    };

    recognition.onerror = (event) => {
      setError(`Speech error: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  }, []);

  return { symptom, setSymptom, isListening, startListening, stopListening, error };
}


/**
 * Example component wiring:
 *
 * import { useSpeechInput } from "@/apps/speech_snippet";
 *
 * export default function SymptomInput({ onSubmit }) {
 *   const { symptom, setSymptom, isListening, startListening, error } = useSpeechInput();
 *
 *   return (
 *     <div className="flex flex-col gap-2">
 *       <textarea
 *         value={symptom}
 *         onChange={(e) => setSymptom(e.target.value)}
 *         placeholder="Describe the problem, or tap the mic…"
 *         className="w-full rounded-xl border p-3 text-sm"
 *         rows={3}
 *       />
 *       <div className="flex gap-2">
 *         <button
 *           onClick={startListening}
 *           className={`rounded-xl px-4 py-2 text-sm font-medium ${
 *             isListening ? "bg-red-500 text-white animate-pulse" : "bg-gray-100"
 *           }`}
 *         >
 *           {isListening ? "🔴 Listening…" : "🎙 Speak"}
 *         </button>
 *         <button
 *           onClick={() => onSubmit(symptom)}
 *           className="flex-1 rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white"
 *         >
 *           Analyze →
 *         </button>
 *       </div>
 *       {error && <p className="text-xs text-red-500">{error}</p>}
 *     </div>
 *   );
 * }
 */
