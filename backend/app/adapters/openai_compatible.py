from __future__ import annotations

import ipaddress
import json
import logging
import time
from typing import Any
from urllib.parse import urlparse

import httpx

from app.adapters.base import AdapterResponse, TargetAgentAdapter
from app.core.config import settings

logger = logging.getLogger(__name__)

# Private/internal IP ranges for SSRF protection
_PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def is_private_ip(hostname: str) -> bool:
    """Check if a hostname resolves to a private/internal IP."""
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_loopback or addr.is_private or addr.is_link_local:
            return True
        return any(addr in net for net in _PRIVATE_RANGES)
    except ValueError:
        # Not an IP literal — hostname like "api.openai.com"
        return False


def is_localhost(hostname: str) -> bool:
    return hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0")


def validate_target_url(url: str) -> tuple[bool, str]:
    """Validate a target URL for safety. Returns (valid, reason)."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"

    if parsed.scheme not in ("http", "https"):
        return False, f"Unsupported scheme: {parsed.scheme}. Only http/https allowed."

    hostname = parsed.hostname or ""
    if not hostname:
        return False, "URL has no hostname"

    if is_localhost(hostname) and not settings.ALLOW_LOCALHOST_TARGETS:
        return False, "Localhost targets are not allowed in production mode"

    if is_private_ip(hostname) and not settings.ALLOW_LOCALHOST_TARGETS:
        return False, "Private/internal IP targets are not allowed in production mode"

    return True, ""


class OpenAICompatibleAdapter(TargetAgentAdapter):
    """Adapter for OpenAI-compatible chat/completions APIs."""

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        model: str = "",
        response_extraction: str = "choices.0.message.content",
        timeout_seconds: int = 30,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.response_extraction = response_extraction
        self.timeout = timeout_seconds

    async def send_prompt(self, prompt: str, context: dict[str, Any] | None = None) -> AdapterResponse:
        url = f"{self.endpoint}/v1/chat/completions"
        model = self.model or (context or {}).get("model", "gpt-3.5-turbo")

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }

        # Add system message if provided in context
        if context and context.get("system_message"):
            payload["messages"].insert(0, {"role": "system", "content": context["system_message"]})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=headers)

            latency_ms = (time.monotonic() - start) * 1000

            if response.status_code >= 500:
                return AdapterResponse(
                    content="",
                    status_code=response.status_code,
                    error=f"Target agent server error: HTTP {response.status_code}",
                    latency_ms=latency_ms,
                )

            if response.status_code >= 400:
                error_body = response.text[:500]
                return AdapterResponse(
                    content="",
                    status_code=response.status_code,
                    error=f"Target agent client error: HTTP {response.status_code} - {error_body}",
                    latency_ms=latency_ms,
                )

            data = response.json()
            content = self._extract_response(data)

            return AdapterResponse(
                content=content,
                status_code=response.status_code,
                raw_response=data,
                latency_ms=latency_ms,
            )

        except httpx.TimeoutException:
            latency_ms = (time.monotonic() - start) * 1000
            return AdapterResponse(
                content="", error="Target agent request timed out", latency_ms=latency_ms
            )
        except httpx.ConnectError as e:
            latency_ms = (time.monotonic() - start) * 1000
            return AdapterResponse(
                content="", error=f"Connection failed: {type(e).__name__}", latency_ms=latency_ms
            )
        except httpx.HTTPError as e:
            latency_ms = (time.monotonic() - start) * 1000
            return AdapterResponse(
                content="", error=f"HTTP error: {type(e).__name__}", latency_ms=latency_ms
            )
        except Exception as e:
            latency_ms = (time.monotonic() - start) * 1000
            logger.exception("Unexpected adapter error for %s", self.endpoint)
            return AdapterResponse(
                content="", error=f"Unexpected error: {type(e).__name__}", latency_ms=latency_ms
            )

    def _extract_response(self, data: dict[str, Any]) -> str:
        """Extract the response content using dot-notation path."""
        parts = self.response_extraction.split(".")
        current: Any = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                idx = int(part)
                current = current[idx] if idx < len(current) else None
            else:
                current = None
            if current is None:
                break
        if isinstance(current, str):
            return current
        # Fallback: try common paths
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            pass
        return json.dumps(data)

    def validate_endpoint(self, endpoint: str) -> bool:
        valid, _ = validate_target_url(endpoint)
        return valid
