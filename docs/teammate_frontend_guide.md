# FieldFix AI — Frontend Setup Guide for Teammate

This document tells you exactly what to do to get the frontend running.
The backend is fully built and running. All React components, TypeScript types,
and API client code are already written — you just need to scaffold the Next.js
project and wire everything together.

**Estimated time: 45–60 minutes.**

---

## What's Already Done (Do Not Rewrite These)

The following files already exist in `frontend/` — copy them into the project after scaffolding:

| File | What it does |
|------|--------------|
| `frontend/types/repair.ts` | All TypeScript interfaces matching the backend API |
| `frontend/lib/api.ts` | Typed fetch functions for every API endpoint |
| `frontend/components/RiskBadge.tsx` | Colored risk level pill (low/medium/high/critical) |
| `frontend/components/DiagnoseForm.tsx` | Symptom textarea + 🎤 speech button + category pills + submit |
| `frontend/components/RepairCard.tsx` | Full repair output display (collapsible sections) |
| `frontend/components/SessionHistory.tsx` | Device repair history list |
| `frontend/app/page.tsx` | Main page — two-panel layout with header |
| `frontend/.env.local.example` | Environment variable template |

---

## Prerequisites

Make sure you have these installed:

```bash
node --version   # needs v18 or higher
npm --version    # needs v9 or higher
```

If not installed, download from https://nodejs.org (LTS version).

---

## Step 1 — Back up the existing files

The `frontend/` folder already has our component files. Before running `create-next-app`
(which will scaffold INTO that folder), copy the existing files somewhere safe first.

```bash
cd /Users/sagarpatel/Documents/fieldfix-ai

# Copy existing frontend files to a temp location
cp -r frontend/ /tmp/fieldfix_frontend_backup/
```

---

## Step 2 — Scaffold Next.js into the frontend folder

```bash
cd /Users/sagarpatel/Documents/fieldfix-ai

# Remove the empty frontend folder (our files are backed up)
rm -rf frontend/

# Scaffold Next.js — answer the prompts as shown below
npx create-next-app@latest frontend
```

**Answer the prompts exactly like this:**

```
✔ Would you like to use TypeScript?              → Yes
✔ Would you like to use ESLint?                  → Yes
✔ Would you like to use Tailwind CSS?            → Yes
✔ Would you like your code inside a `src/` directory? → No
✔ Would you like to use App Router?              → Yes
✔ Would you like to use Turbopack?               → No  (use No for stability)
✔ Would you like to customize the import alias?  → Yes
  What import alias would you like configured?   → @/*  (just press Enter, this is the default)
```

This creates `frontend/` with `package.json`, `tsconfig.json`, `tailwind.config.ts`,
`next.config.ts`, and a working `app/layout.tsx`.

---

## Step 3 — Restore our pre-written files

```bash
# Copy our files back in (overwriting Next.js defaults where needed)
cp /tmp/fieldfix_frontend_backup/types/repair.ts frontend/types/repair.ts
cp /tmp/fieldfix_frontend_backup/lib/api.ts frontend/lib/api.ts
cp /tmp/fieldfix_frontend_backup/components/RiskBadge.tsx frontend/components/RiskBadge.tsx
cp /tmp/fieldfix_frontend_backup/components/DiagnoseForm.tsx frontend/components/DiagnoseForm.tsx
cp /tmp/fieldfix_frontend_backup/components/RepairCard.tsx frontend/components/RepairCard.tsx
cp /tmp/fieldfix_frontend_backup/components/SessionHistory.tsx frontend/components/SessionHistory.tsx
cp /tmp/fieldfix_frontend_backup/app/page.tsx frontend/app/page.tsx
cp /tmp/fieldfix_frontend_backup/.env.local.example frontend/.env.local.example
```

Create the missing directories if needed:

```bash
mkdir -p frontend/types frontend/lib frontend/components
```

---

## Step 4 — Set up environment variables

```bash
cd frontend
cp .env.local.example .env.local
```

Open `.env.local` and set the backend URL:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **For phone access (demo mode):** Replace `localhost` with your laptop's WiFi IP address.
> Find it with: `ipconfig getifaddr en0` (Mac) or `hostname -I` (Linux)
> Example: `NEXT_PUBLIC_API_URL=http://192.168.1.42:8000`

---

## Step 5 — Update app/layout.tsx

Next.js creates a default `layout.tsx`. Replace its content with this:

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FieldFix AI",
  description: "Offline repair copilot powered by Gemma",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 min-h-screen`}>
        {children}
      </body>
    </html>
  );
}
```

---

## Step 6 — Clean up Next.js default styles

Open `frontend/app/globals.css`. Delete everything inside it and replace with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Step 7 — Install and run

```bash
cd /Users/sagarpatel/Documents/fieldfix-ai/frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser. You should see the FieldFix AI UI.

---

## Step 8 — Connect to the backend

Make sure the backend is running in a separate terminal:

```bash
cd /Users/sagarpatel/Documents/fieldfix-ai
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Then try the app — type a symptom like "servo is buzzing" and click Analyze.

> **If you see CORS errors in the browser console:** The backend already has CORS
> open to all origins (`allow_origins=["*"]`), so this should not happen. If it
> does, make sure NEXT_PUBLIC_API_URL matches the exact URL the backend is running on.

---

## Step 9 — Test on phone (iOS Safari)

1. Make sure laptop and phone are on the same WiFi network.
2. Find laptop IP: `ipconfig getifaddr en0`
3. Update `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://192.168.x.x:8000
   ```
4. Restart Next.js dev server: `npm run dev -- --host 0.0.0.0`
5. Open `http://192.168.x.x:3000` in iPhone Safari.
6. Tap the 🎤 Speak button — iOS Safari will ask for microphone permission. Allow it.

---

## Step 10 — Production build check

Before the demo, run a production build to catch any errors:

```bash
cd frontend
npm run build
```

It should say `✓ Compiled successfully`. Warnings are fine. Errors must be fixed.

---

## What Each Component Does (so you can style/tweak)

### `app/page.tsx`
The main page. Two-panel layout:
- **Left panel:** DiagnoseForm (symptom input) + SessionHistory (past repairs)
- **Right panel:** RepairCard (results) or empty state with demo suggestion pills

### `components/DiagnoseForm.tsx`
- Textarea for typing symptoms
- 🎤 Speak button — uses Web Speech API (works on iOS Safari)
- Category pills: Auto-detect / Robotics / Electronics / Emergency / Household
- Analyze button — calls backend `/repair/analyze`
- Shows loading spinner and error messages

### `components/RepairCard.tsx`
Displays the full repair output. Sections:
- Header: detected item, risk badge, confidence bar
- Critical banner (red, shown only for critical risk — gas leaks, etc.)
- Likely causes with confidence percentages
- Step-by-step repair (hidden if critical risk)
- Tools needed, stop conditions, prevention, sources
- All sections are collapsible (click to expand/collapse)

### `components/RiskBadge.tsx`
Color-coded pill:
- 🟢 Low Risk
- 🟡 Medium Risk
- 🟠 High Risk
- 🔴 Do Not Attempt

### `components/SessionHistory.tsx`
Shows past repairs for the current device (stored in SQLite on the backend).
Clicking a history item loads it back into the right panel.

### `frontend/lib/api.ts`
All backend calls are here. Functions:
- `analyzeRepair(params)` → POST /repair/analyze
- `checkSafety(symptom)` → POST /safety/check
- `getDeviceHistory(deviceId)` → GET /memory/{device_id}
- `deleteDeviceHistory(deviceId)` → DELETE /memory/{device_id}
- `searchRAG(query, category, top_k)` → POST /rag/search
- `getHealth()` → GET /health

---

## Optional Enhancements (if you have time)

These are nice-to-haves, not required for the demo:

1. **shadcn/ui components** — prettier buttons and cards
   ```bash
   npx shadcn@latest init
   npx shadcn@latest add button card badge textarea
   ```

2. **Demo pill prefill** — the demo suggestion pills in `page.tsx` dispatch a
   `fieldfix:prefill` custom event. To wire them to the form, add this inside
   `DiagnoseForm.tsx`'s `useEffect`:
   ```tsx
   useEffect(() => {
     const handler = (e: Event) => {
       setSymptom((e as CustomEvent).detail as string);
     };
     window.addEventListener("fieldfix:prefill", handler);
     return () => window.removeEventListener("fieldfix:prefill", handler);
   }, []);
   ```

3. **Loading skeleton** — show a pulsing skeleton while waiting for the API response

4. **Dark mode** — Tailwind supports it with `dark:` classes

---

## Common Problems

| Problem | Fix |
|---------|-----|
| `Module not found: @/types/repair` | Make sure `tsconfig.json` has `"paths": {"@/*": ["./*"]}` — `create-next-app` sets this automatically |
| `webkitSpeechRecognition not defined` | Only works in browser (not SSR). The component already has `"use client"` — if still broken, check that Next.js isn't server-rendering it |
| Blank page at localhost:3000 | Run `npm run build` to see the actual error |
| `fetch failed` in browser | Backend not running, or wrong IP in `.env.local`. Check `npm run dev` terminal for API errors |
| TypeScript errors on `SpeechRecognition` | Add `lib: ["dom"]` to `tsconfig.json` compilerOptions if missing |

---

## Final Checklist Before Demo

- [ ] `npm run build` completes with zero errors
- [ ] Backend running: `curl http://localhost:8000/health` returns `{"status":"ok",...}`
- [ ] Typing "servo is buzzing" + Analyze → repair card appears
- [ ] 🎤 Speak button works in Safari (phone or laptop)
- [ ] History panel shows past repairs after a few analyzes
- [ ] Critical safety symptom (e.g. "I smell gas") → red blocked screen appears
- [ ] Phone access: `http://<laptop-ip>:3000` loads in iPhone Safari

---

## Quick Reference — All Running Services

```bash
# Terminal 1 — Ollama (AI model)
ollama serve

# Terminal 2 — Backend API
cd /Users/sagarpatel/Documents/fieldfix-ai
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 — Frontend
cd /Users/sagarpatel/Documents/fieldfix-ai/frontend
npm run dev -- --host 0.0.0.0

# Demo without Gemma (instant mock mode)
USE_MOCK=true uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
