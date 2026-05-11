from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Step:
    label: str
    placeholder: str
    value: Optional[str] = None


@dataclass
class SequentialFieldDemo:
    """Paste-ready step-by-step flow for the final placement."""

    steps: List[Step] = field(default_factory=lambda: [
        Step(label="project_name", placeholder="Enter the project name"),
        Step(label="first_field", placeholder="Fill the first field"),
        Step(label="second_field", placeholder="Fill the second field"),
        Step(label="api_code", placeholder="Paste the API code here later"),
    ])
    index: int = 0

    def next_step(self, user_input: str) -> str:
        if self.index >= len(self.steps):
            return f"All steps complete. Final input: {user_input}"

        current = self.steps[self.index]
        current.value = user_input
        self.index += 1

        if current.label == "api_code":
            # CALL THE API HANDLER HERE
            # Replace the body of `handle_api_step` with your API integration code.
            return self.handle_api_step(user_input)

        return f"Step {self.index}: {current.placeholder}. You entered: {user_input}"

    def progress(self) -> str:
        lines = []
        for position, step in enumerate(self.steps, start=1):
            value = step.value if step.value is not None else "[empty]"
            lines.append(f"{position}. {step.label}: {value}")
        return "\n".join(lines)

    def handle_api_step(self, api_input: str) -> str:
        """
        Hook for the final API step.

        Replace the body of this method with your API call. Example usage:

        def handle_api_step(self, api_input: str) -> str:
            # import your client or library
            # result = my_api_client.call(api_input)
            # return result_text

        The method should return a human-readable string to display as the step result.
        Keep it synchronous for now; if you need async, adapt the caller accordingly.
        """
        # Production-ready example using Google's Generative Language REST API.
        # This uses the requests library and expects GEMINI_API_KEY and optional
        # GEMINI_MODEL/GEMINI_SYSTEM_PROMPT to be set in the environment.
        import os
        from pathlib import Path

        try:
            import requests
            from dotenv import load_dotenv
        except Exception:
            return "Missing dependency: install 'requests' and 'python-dotenv'"

        # Load .env from parent directory (where the main app is)
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(str(env_path))

        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        system_prompt = os.getenv(
            "GEMINI_SYSTEM_PROMPT",
            "You are a concise, friendly AI assistant. Reply briefly.",
        )

        if not api_key:
            return "API-avain puuttuu (aseta GEMINI_API_KEY ympäristömuuttujaan)."

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": api_input}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512},
        }

        try:
            resp = requests.post(endpoint, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts).strip()
            return text or "API palautti tyhjän vastauksen."
        except requests.HTTPError as e:
            try:
                err = resp.json().get("error", {}).get("message")
            except Exception:
                err = str(e)
            return f"API-virhe: {err}"
        except Exception as e:
            return f"API-kutsu epäonnistui: {e}"


def create_demo() -> SequentialFieldDemo:
    return SequentialFieldDemo()
