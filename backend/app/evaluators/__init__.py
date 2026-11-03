from app.evaluators.base import BaseEvaluator
from app.evaluators.prompt_injection import PromptInjectionEvaluator
from app.evaluators.jailbreak import JailbreakEvaluator
from app.evaluators.data_leakage import DataLeakageEvaluator
from app.evaluators.tool_security import ToolSecurityEvaluator
from app.evaluators.unsafe_behavior import UnsafeBehaviorEvaluator
from app.evaluators.semantic import SemanticEvaluator

EVALUATOR_REGISTRY: dict[str, type[BaseEvaluator]] = {
    "PromptInjectionEvaluator": PromptInjectionEvaluator,
    "JailbreakEvaluator": JailbreakEvaluator,
    "DataLeakageEvaluator": DataLeakageEvaluator,
    "ToolSecurityEvaluator": ToolSecurityEvaluator,
    "UnsafeBehaviorEvaluator": UnsafeBehaviorEvaluator,
}

__all__ = [
    "BaseEvaluator",
    "PromptInjectionEvaluator",
    "JailbreakEvaluator",
    "DataLeakageEvaluator",
    "ToolSecurityEvaluator",
    "UnsafeBehaviorEvaluator",
    "SemanticEvaluator",
    "EVALUATOR_REGISTRY",
]
