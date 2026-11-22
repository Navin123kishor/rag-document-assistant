
from google import genai
from google.genai import types, errors

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL_NAME,
    SYSTEM_INSTRUCTION,
    MAX_RESPONSE_TOKENS,
    RESPONSE_TEMPERATURE
)


class LLMClient:
    def __init__(self):
        retry_options = types.HttpRetryOptions(
            attempts=3,
            initial_delay=1.0,
            exp_base=2.0,
            max_delay=4.0,
            jitter=1.0,
            http_status_codes=[408, 429, 500, 502, 503, 504]
        )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(
                retry_options=retry_options
            )
        )

        self.model_name = GEMINI_MODEL_NAME

    def generate_response(
        self,
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    ):
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=MAX_RESPONSE_TOKENS,
                    temperature=RESPONSE_TEMPERATURE
                )
            )

            return response.text

        except errors.APIError as e:
            if e.code == 429:
                raise RuntimeError(
                    "Gemini rate limit or quota exceeded."
                ) from e

            elif e.code == 503:
                raise RuntimeError(
                    "Gemini service is temporarily unavailable."
                ) from e

            elif e.code >= 500:
                raise RuntimeError(
                    f"Gemini server error: {e.code}"
                ) from e

            elif e.code == 403:
                raise RuntimeError(
                    "Access denied. Check API key and permissions."
                ) from e

            elif e.code == 404:
                raise RuntimeError(
                    "Gemini model not found. Check model name."
                ) from e

            raise RuntimeError(
                f"Gemini API error: {e.code} - {e.message}"
            ) from e
