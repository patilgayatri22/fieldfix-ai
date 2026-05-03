"""Gemma 3 client via Ollama.

Wraps the Ollama REST API for local inference.
Auto-falls back to mock mode if Ollama is unreachable — demo always works.

Environment variables:
    OLLAMA_URL    Base URL for Ollama  (default: http://localhost:11434)
    GEMMA_MODEL   Model tag to use     (default: gemma3:4b)
    GEMMA_TIMEOUT Request timeout (s)  (default: 60)
    USE_MOCK      "true" forces mock   (default: false — tries Ollama first)

Usage:
    client = GemmaClient()
    raw_str = client.generate("explain this symptom: ...")
    data    = client.generate_json("return a JSON list of causes for: ...")
"""

from __future__ import annotations

import json
import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)

OLLAMA_URL: str = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL: str = os.environ.get("GEMMA_MODEL", "gemma3:4b")
TIMEOUT: float = float(os.environ.get("GEMMA_TIMEOUT", "60"))
CONNECT_TIMEOUT: float = 2.0  # fast fail for availability check


class GemmaClient:
    """
    Thin wrapper around the Ollama /api/generate endpoint.

    Automatically falls back to returning an empty dict / empty string
    if Ollama is unreachable, so callers can handle gracefully.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        timeout: float = TIMEOUT,
        ollama_url: str = OLLAMA_URL,
    ) -> None:
        self.model = model
        self.timeout = timeout
        self.ollama_url = ollama_url
        self._available: bool | None = None  # cached after first check

    # ── Availability ──────────────────────────────────────────────────────────

    def is_available(self) -> bool:
        """Return True if Ollama is running AND the configured model is pulled."""
        if self._available is not None:
            return self._available
        try:
            r = httpx.get(
                f"{self.ollama_url}/api/tags",
                timeout=CONNECT_TIMEOUT,
            )
            if r.status_code != 200:
                self._available = False
            else:
                # Check that our model is in the pulled model list
                models = r.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                # Match on model name prefix (e.g. "gemma3:4b" matches "gemma3:4b")
                self._available = any(
                    self.model in name or name.startswith(self.model.split(":")[0])
                    for name in model_names
                )
                if not self._available:
                    logger.warning(
                        "Ollama running but model '%s' not pulled. "
                        "Run: ollama pull %s",
                        self.model, self.model,
                    )
        except Exception:
            self._available = False
        if not self._available:
            logger.warning(
                "Ollama not reachable at %s — falling back to mock mode", self.ollama_url
            )
        return self._available

    def reset_availability_cache(self) -> None:
        """Force re-check of Ollama availability on next call."""
        self._available = None

    # ── Core generation ───────────────────────────────────────────────────────

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        json_mode: bool = False,
    ) -> str:
        """
        Generate text from Gemma via Ollama.

        Args:
            prompt:    User-turn prompt.
            system:    Optional system prompt prepended to the conversation.
            json_mode: Pass format="json" to Ollama for JSON-constrained output.

        Returns:
            Generated text string, or "" on any failure.
        """
        if not self.is_available():
            return ""

        payload: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,   # low temp for structured/factual output
                "num_predict": 1024,
            },
        }
        if system:
            payload["system"] = system
        if json_mode:
            payload["format"] = "json"

        try:
            r = httpx.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            r.raise_for_status()
            return r.json().get("response", "")
        except httpx.TimeoutException:
            logger.warning("Ollama request timed out after %.0fs", self.timeout)
            self._available = None  # recheck next call
            return ""
        except Exception as exc:
            logger.warning("Ollama generate failed: %s", exc)
            return ""

    def generate_json(
        self,
        prompt: str,
        system: str | None = None,
    ) -> dict:
        """
        Generate and parse a JSON object from Gemma.

        Uses Ollama's json mode + best-effort extraction if the model
        returns JSON embedded in prose.

        Returns:
            Parsed dict, or {} on any failure.
        """
        raw = self.generate(prompt, system=system, json_mode=True)
        if not raw:
            return {}

        # Try direct parse first
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Extract first {...} block from prose response
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        logger.warning("Could not parse JSON from Gemma response (len=%d)", len(raw))
        return {}


# ── Module-level singleton ─────────────────────────────────────────────────────
# Import this instead of constructing a new client every request.

_client: GemmaClient | None = None


def get_client() -> GemmaClient:
    """Return module-level GemmaClient singleton."""
    global _client
    if _client is None:
        _client = GemmaClient()
    return _client
