"""Robust local implementation gateway provider for Groq Cloud API inference executing Llama models."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Final

# Path resilience injection framework for local executor isolation
PROJECT_ROOT: Final[str] = str(Path(__file__).parent.parent.parent.resolve())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from groq import Groq
except ImportError:
    Groq = None


class GroqProvider:
    """Manages secure communication lifecycles and completion payloads targeting Groq Cloud endpoints."""

    def __init__(
        self, api_key_env_var: str = "GROQ_API_KEY", model_target: str = "openai/gpt-oss-20b"
    ) -> None:
        """Initializes the infrastructure provider, fetching credentials securely from environment scopes."""
        self._api_key = os.environ.get(api_key_env_var, "")
        self._model_target = model_target

    def generate_completion(self, system_prompt_context: str) -> str:
        """Dispatches an inference request payload toward the remote cloud execution gateway grid."""
        if not self._api_key:
            return "Generic Operational Alert: The configuration profile is missing a valid API authentication key."

        if Groq is None:
            return "Dependency Constraint: The explicit third-party 'groq' distribution bundle is not available on disk."

        try:
            client = Groq(api_key=self._api_key)

            completion_payload = client.chat.completions.create(
                model=self._model_target,
                messages=[{"role": "user", "content": system_prompt_context}],
                temperature=0.2,
                max_tokens=2048,
                top_p=0.9,
                stream=False,
            )

            if completion_payload.choices:
                output_content = completion_payload.choices[0].message.content
                return output_content.strip() if output_content else ""

            return "⚠️ Connection Warning: Received an empty message context response from the remote gateway engine."

        except Exception as error_exception:
            return f"❌ Ingestion Gateway Failure: Unable to complete operation due to active context error: {error_exception}"

    def generate_response(self, system_prompt_context: str) -> str:
        """Alias wrapper ensuring total backward compatibility for Streamlit pages context layers."""
        return self.generate_completion(system_prompt_context)

    @property
    def configured_model(self) -> str:
        """Exposes the internal target processing model string identifier currently deployed."""
        return self._model_target
