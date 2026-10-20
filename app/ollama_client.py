from typing import Optional

import httpx

from app.config import settings


class OllamaError(Exception):
    """Raised when Ollama cannot provide a valid answer."""


async def generate_answer(question: str, context: Optional[str] = None) -> str:
    prompt = question

    if context:
        prompt = (
            "You are a helpful assistant. Use the student records below when they "
            "are relevant. If they are not relevant, answer normally.\n\n"
            f"Student records:\n{context}\n\n"
            f"Question: {question}"
        )

    url = f"{settings.ollama_base_url.rstrip('/')}/api/generate"

    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise OllamaError(
            "Could not reach Ollama or the request failed. Start it with "
            "`ollama serve` and ensure the model is available using "
            f"`ollama pull {settings.ollama_model}`."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise OllamaError("Ollama returned an invalid JSON response.") from exc

    if not isinstance(data, dict):
        raise OllamaError("Ollama returned an unexpected response format.")

    answer = data.get("response")

    if not isinstance(answer, str) or not answer.strip():
        raise OllamaError("Ollama returned an empty or invalid answer.")

    return answer.strip()
