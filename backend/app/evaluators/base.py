from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.models.test_case import TestCase
from app.models.test_result import EvaluatorSignal


class BaseEvaluator(ABC):
    """Base class for all security evaluators."""

    evaluator_type: str = "deterministic"

    @abstractmethod
    def evaluate(
        self, test_case: TestCase, response: str, context: dict[str, Any] | None = None
    ) -> EvaluatorSignal:
        """Evaluate a target agent response against a test case.

        Returns an EvaluatorSignal with verdict, confidence, reason, and evidence.
        """
        ...
