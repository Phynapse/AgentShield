from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AdapterResponse:
    """Structured response from target agent communication."""

    content: str
    status_code: int = 200
    raw_response: dict[str, Any] | None = None
    error: str | None = None
    latency_ms: float = 0.0


class TargetAgentAdapter(ABC):
    """Abstract interface for communicating with target AI agents."""

    @abstractmethod
    async def send_prompt(self, prompt: str, context: dict[str, Any] | None = None) -> AdapterResponse:
        """Send a prompt to the target agent and return a structured response."""
        ...

    @abstractmethod
    def validate_endpoint(self, endpoint: str) -> bool:
        """Check whether an endpoint URL is valid and allowed."""
        ...
