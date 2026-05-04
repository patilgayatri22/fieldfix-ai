#!/usr/bin/env python3
"""Generate teammate_frontend_guide.pdf from the markdown guide."""

import sys
from pathlib import Path
from fpdf import FPDF
from fpdf.enums import XPos, YPos

OUTPUT = Path(__file__).parent.parent.parent / "docs" / "FieldFix_AI_Teammate_Frontend_Guide.pdf"


_SUPP = "/System/Library/Fonts/Supplemental"
_FONTS = {
    ("Arial", ""):   f"{_SUPP}/Arial.ttf",
    ("Arial", "B"):  f"{_SUPP}/Arial Bold.ttf",
    ("Arial", "I"):  f"{_SUPP}/Arial Italic.ttf",
    ("Arial", "BI"): f"{_SUPP}/Arial Bold Italic.ttf",
    ("Mono",  ""):   "/System/Library/Fonts/Monaco.ttf",
}


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        for (family, style), path in _FONTS.items():
            self.add_font(family, style, path)
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_margins(20, 20, 20)

    # ── Cover / title page helpers ──────────────────────────────────────────

    def cover(self):
        self.set_fill_color(30, 58, 138)          # indigo-900
        self.rect(0, 0, 210, 70, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 24)
        self.set_xy(20, 18)
        self.cell(0, 10, "FieldFix AI", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Arial", "", 13)
        self.set_xy(20, 34)
        self.cell(0, 8, "Frontend Setup Guide for Teammate", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(20, 46)
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "Backend is complete. Your job: scaffold Next.js + wire in pre-written components.",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.set_xy(20, 75)

    # ── Typography helpers ──────────────────────────────────────────────────

    def h1(self, text):
        self.ln(6)
        self.set_font("Arial", "B", 15)
        self.set_text_color(30, 58, 138)
        self.set_fill_color(239, 246, 255)
        self.cell(0, 9, text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def h2(self, text):
        self.ln(4)
        self.set_font("Arial", "B", 12)
        self.set_text_color(55, 65, 81)
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body(self, text, indent=0):
        self.set_font("Arial", "", 10)
        self.set_text_color(31, 41, 55)
        self.set_x(20 + indent)
        self.multi_cell(170 - indent, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def bullet(self, text, indent=4):
        self.set_font("Arial", "", 10)
        self.set_text_color(31, 41, 55)
        self.set_x(20 + indent)
        eff_w = 170 - indent - 6
        # bullet dot
        self.cell(6, 5.5, "•")
        self.multi_cell(eff_w, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def code(self, text):
        self.set_font("Mono", "", 9)
        self.set_fill_color(243, 244, 246)
        self.set_text_color(17, 24, 39)
        self.set_x(20)
        for line in text.split("\n"):
            self.set_x(20)
            self.cell(170, 5.2, line, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def note(self, text):
        self.set_font("Arial", "I", 9)
        self.set_text_color(107, 114, 128)
        self.set_x(20)
        self.multi_cell(170, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def divider(self):
        self.ln(3)
        self.set_draw_color(209, 213, 219)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(3)

    def checkbox(self, text):
        self.set_font("Arial", "", 10)
        self.set_text_color(31, 41, 55)
        self.set_x(20)
        self.cell(8, 5.5, "[ ]")
        self.multi_cell(162, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def table_row(self, col1, col2, header=False):
        if header:
            self.set_fill_color(219, 234, 254)
            self.set_font("Arial", "B", 9)
        else:
            self.set_fill_color(249, 250, 251)
            self.set_font("Arial", "", 9)
        self.set_x(20)
        self.cell(70, 6, col1, border=1, fill=header, new_x=XPos.RIGHT)
        self.cell(100, 6, col2, border=1, fill=header, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Arial", "", 10)


def build(pdf: PDF):
    # ── COVER ────────────────────────────────────────────────────────────────
    pdf.cover()

    # ── OVERVIEW ─────────────────────────────────────────────────────────────
    pdf.h1("Overview")
    pdf.body(
        "The backend is 100% complete — FastAPI, RAG, safety guardrails, Gemma client, "
        "device memory, all agents, and 124 passing tests. All React component files, "
        "TypeScript types, and API client code are already written and sitting in the "
        "frontend/ folder. Your job is to scaffold the Next.js project around them and "
        "wire everything together."
    )
    pdf.body("Estimated time: 45-60 minutes.")
    pdf.ln(2)

    # ── FILES ALREADY WRITTEN ─────────────────────────────────────────────────
    pdf.h1("Files Already Written — Do Not Rewrite These")
    pdf.table_row("File", "Purpose", header=True)
    rows = [
        ("frontend/types/repair.ts",             "TypeScript interfaces for all API types"),
        ("frontend/lib/api.ts",                  "Typed fetch functions for every endpoint"),
        ("frontend/components/RiskBadge.tsx",    "Color-coded risk level pill component"),
        ("frontend/components/DiagnoseForm.tsx", "Symptom input + speech + category pills"),
        ("frontend/components/RepairCard.tsx",   "Full repair output display, collapsible"),
        ("frontend/components/SessionHistory.tsx","Device repair history list"),
        ("frontend/app/page.tsx",                "Main page — two-panel layout + header"),
        ("frontend/.env.local.example",          "Environment variable template"),
    ]
    for r in rows:
        pdf.table_row(*r)
    pdf.ln(4)

    # ── PREREQUISITES ─────────────────────────────────────────────────────────
    pdf.h1("Prerequisites")
    pdf.body("Check you have Node.js 18+ installed:")
    pdf.code("node --version   # needs v18 or higher\nnpm --version    # needs v9 or higher")
    pdf.body("If not installed: download from https://nodejs.org (LTS version).")

    # ── STEP 1 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 1 — Back Up the Existing Frontend Files")
    pdf.body(
        "The frontend/ folder already contains pre-written components. "
        "Back them up before scaffolding Next.js into that folder."
    )
    pdf.code("cd /path/to/fieldfix-ai\n\ncp -r frontend/ /tmp/fieldfix_frontend_backup/")

    # ── STEP 2 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 2 — Scaffold Next.js")
    pdf.code("cd /path/to/fieldfix-ai\n\nrm -rf frontend/\n\nnpx create-next-app@latest frontend")
    pdf.body("Answer the interactive prompts EXACTLY as shown below:")
    pdf.ln(1)
    prompts = [
        ("Use TypeScript?",                          "Yes"),
        ("Use ESLint?",                              "Yes"),
        ("Use Tailwind CSS?",                        "Yes"),
        ("Code inside src/ directory?",              "No"),
        ("Use App Router?",                          "Yes"),
        ("Use Turbopack?",                           "No  (important — pick No)"),
        ("Customize import alias?",                  "Yes"),
        ("What alias?",                              "@/*  (just press Enter)"),
    ]
    pdf.table_row("Prompt", "Your Answer", header=True)
    for p in prompts:
        pdf.table_row(*p)
    pdf.ln(4)

    # ── STEP 3 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 3 — Restore the Pre-Written Files")
    pdf.code(
        "mkdir -p frontend/types frontend/lib frontend/components\n\n"
        "cp /tmp/fieldfix_frontend_backup/types/repair.ts              frontend/types/\n"
        "cp /tmp/fieldfix_frontend_backup/lib/api.ts                   frontend/lib/\n"
        "cp /tmp/fieldfix_frontend_backup/components/RiskBadge.tsx     frontend/components/\n"
        "cp /tmp/fieldfix_frontend_backup/components/DiagnoseForm.tsx  frontend/components/\n"
        "cp /tmp/fieldfix_frontend_backup/components/RepairCard.tsx    frontend/components/\n"
        "cp /tmp/fieldfix_frontend_backup/components/SessionHistory.tsx frontend/components/\n"
        "cp /tmp/fieldfix_frontend_backup/app/page.tsx                 frontend/app/\n"
        "cp /tmp/fieldfix_frontend_backup/.env.local.example           frontend/"
    )

    # ── STEP 4 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 4 — Set Up Environment Variables")
    pdf.code("cd frontend\ncp .env.local.example .env.local")
    pdf.body("Open .env.local and set:")
    pdf.code("NEXT_PUBLIC_API_URL=http://localhost:8000")
    pdf.note(
        "For phone demo: replace localhost with your laptop's WiFi IP.\n"
        "Find it with: ipconfig getifaddr en0 (Mac) or ipconfig (Windows)\n"
        "Example: NEXT_PUBLIC_API_URL=http://192.168.1.42:8000"
    )

    # ── STEP 5 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 5 — Update app/layout.tsx")
    pdf.body(
        "Next.js creates a default layout.tsx. Replace its entire content "
        "with the following:"
    )
    pdf.code(
        'import type { Metadata } from "next";\n'
        'import { Inter } from "next/font/google";\n'
        'import "./globals.css";\n'
        "\n"
        'const inter = Inter({ subsets: ["latin"] });\n'
        "\n"
        "export const metadata: Metadata = {\n"
        '  title: "FieldFix AI",\n'
        '  description: "Offline repair copilot powered by Gemma",\n'
        "};\n"
        "\n"
        "export default function RootLayout({\n"
        "  children,\n"
        "}: {\n"
        "  children: React.ReactNode;\n"
        "}) {\n"
        '  return (\n'
        '    <html lang="en">\n'
        '      <body className={`${inter.className} bg-gray-50 min-h-screen`}>\n'
        "        {children}\n"
        "      </body>\n"
        "    </html>\n"
        "  );\n"
        "}"
    )

    # ── STEP 6 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 6 — Fix globals.css")
    pdf.body(
        "Open frontend/app/globals.css. Delete everything in it and replace with "
        "just these 3 lines:"
    )
    pdf.code("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

    # ── STEP 7 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 7 — Install Dependencies and Run")
    pdf.code(
        "cd /path/to/fieldfix-ai/frontend\n"
        "npm install\n"
        "npm run dev"
    )
    pdf.body("Open http://localhost:3000 — you should see the FieldFix AI interface.")

    # ── STEP 8 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 8 — Connect to Backend")
    pdf.body(
        "The backend must be running for the app to work. "
        "Open a separate terminal and run:"
    )
    pdf.code(
        "cd /path/to/fieldfix-ai\n"
        "source .venv/bin/activate\n"
        "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
    )
    pdf.body(
        "Then try the UI: type 'servo is buzzing' in the textarea and click Analyze. "
        "A repair card should appear in the right panel."
    )

    # ── STEP 9 ────────────────────────────────────────────────────────────────
    pdf.h1("Step 9 — Test on iPhone (iOS Safari)")
    pdf.bullet("Make sure laptop and iPhone are on the same WiFi network.")
    pdf.bullet("Find laptop IP: ipconfig getifaddr en0  (Mac)")
    pdf.bullet("Update frontend/.env.local: NEXT_PUBLIC_API_URL=http://192.168.x.x:8000")
    pdf.bullet("Restart dev server: npm run dev -- --host 0.0.0.0")
    pdf.bullet("Open http://192.168.x.x:3000 in iPhone Safari.")
    pdf.bullet("Tap the microphone button — allow microphone access when prompted.")

    # ── STEP 10 ───────────────────────────────────────────────────────────────
    pdf.h1("Step 10 — Production Build Check (Before Demo)")
    pdf.code("cd frontend\nnpm run build")
    pdf.body(
        "Must show: Compiled successfully  (or: Build succeeded)\n"
        "Warnings are acceptable. Errors must be fixed before the demo."
    )

    # ── COMPONENT OVERVIEW ────────────────────────────────────────────────────
    pdf.h1("What Each Component Does")

    components = [
        ("app/page.tsx",
         "Main page. Left panel: DiagnoseForm + SessionHistory. "
         "Right panel: RepairCard or empty state with 4 demo suggestion pills."),
        ("DiagnoseForm.tsx",
         "Symptom textarea + speech button (Web Speech API, works on iOS Safari) + "
         "category pills (Auto-detect / Robotics / Electronics / Emergency / Household) + "
         "Analyze button. Shows loading spinner and error messages."),
        ("RepairCard.tsx",
         "Displays full repair output. Sections: header (item + risk badge + confidence bar), "
         "critical red banner (gas leaks etc.), likely causes, step-by-step repair, "
         "tools, stop conditions, prevention, sources. All collapsible."),
        ("RiskBadge.tsx",
         "Color pill: green=Low, amber=Medium, orange=High, red=Do Not Attempt."),
        ("SessionHistory.tsx",
         "Lists past repairs for this device (stored in SQLite on backend). "
         "Click any item to reload it into the right panel."),
        ("lib/api.ts",
         "All backend calls: analyzeRepair, checkSafety, getDeviceHistory, "
         "deleteDeviceHistory, searchRAG, getHealth."),
    ]
    for name, desc in components:
        pdf.h2(name)
        pdf.body(desc, indent=4)

    # ── OPTIONAL ENHANCEMENTS ─────────────────────────────────────────────────
    pdf.h1("Optional Enhancements (if time allows)")
    pdf.bullet(
        "shadcn/ui — prettier buttons and cards:\n"
        "  npx shadcn@latest init\n"
        "  npx shadcn@latest add button card badge textarea"
    )
    pdf.bullet(
        "Wire demo pills to prefill the form — add this inside DiagnoseForm useEffect:\n"
        "  const handler = (e) => setSymptom(e.detail);\n"
        "  window.addEventListener('fieldfix:prefill', handler);\n"
        "  return () => window.removeEventListener('fieldfix:prefill', handler);"
    )
    pdf.bullet("Loading skeleton while waiting for API response.")
    pdf.bullet("Dark mode using Tailwind dark: classes.")

    # ── TROUBLESHOOTING ───────────────────────────────────────────────────────
    pdf.h1("Common Problems and Fixes")
    pdf.table_row("Problem", "Fix", header=True)
    issues = [
        ("Module not found: @/types/repair",
         "Check tsconfig.json has paths: {'@/*': ['./*']}"),
        ("Speech button not working",
         "Component needs 'use client' at top. Already included."),
        ("Blank page at localhost:3000",
         "Run npm run build to see the actual error"),
        ("fetch failed in browser",
         "Backend not running, or wrong IP in .env.local"),
        ("TS error on SpeechRecognition",
         "Add \"dom\" to lib array in tsconfig.json compilerOptions"),
        ("CORS error in browser console",
         "Backend allows all origins — check NEXT_PUBLIC_API_URL is correct"),
        ("npm run build fails",
         "Read the error. Usually a missing import or wrong type."),
    ]
    for issue in issues:
        pdf.table_row(*issue)
    pdf.ln(4)

    # ── DEMO CHECKLIST ────────────────────────────────────────────────────────
    pdf.h1("Final Demo Checklist")
    checklist = [
        "npm run build completes with zero errors",
        "Backend running: curl http://localhost:8000/health returns {\"status\":\"ok\"}",
        "Type 'servo is buzzing' + Analyze → repair card appears in right panel",
        "Microphone button works in Safari (phone or laptop)",
        "History panel shows past repairs after analyzing a few symptoms",
        "Type 'I smell gas' → red critical safety banner appears (no repair steps)",
        "Phone access: http://<laptop-ip>:3000 loads in iPhone Safari",
        "Speech input works on iPhone (microphone permission granted)",
    ]
    for item in checklist:
        pdf.checkbox(item)
    pdf.ln(4)

    # ── QUICK REFERENCE ───────────────────────────────────────────────────────
    pdf.h1("Quick Reference — All Running Services")
    pdf.code(
        "# Terminal 1 — AI model\n"
        "ollama serve\n"
        "\n"
        "# Terminal 2 — Backend API\n"
        "cd /path/to/fieldfix-ai\n"
        "source .venv/bin/activate\n"
        "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000\n"
        "\n"
        "# Terminal 3 — Frontend\n"
        "cd /path/to/fieldfix-ai/frontend\n"
        "npm run dev -- --host 0.0.0.0\n"
        "\n"
        "# Demo mode (no Gemma needed — instant mock responses)\n"
        "USE_MOCK=true uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
    )

    # ── FOOTER NOTE ────────────────────────────────────────────────────────────
    pdf.divider()
    pdf.note(
        "Backend: FastAPI v0.2.0 | RAG: 295 chunks (ChromaDB) | Model: Gemma 3 4B via Ollama | "
        "Tests: 124 passing | Safety: deterministic 4-tier guardrails"
    )


if __name__ == "__main__":
    pdf = PDF()
    build(pdf)
    pdf.output(OUTPUT)
    print(f"PDF saved: {OUTPUT}")
