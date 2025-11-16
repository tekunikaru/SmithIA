from dataclasses import dataclass
from lmstudio import LlmPredictionConfig

@dataclass
class QwQ3(LlmPredictionConfig):
    max_tokens     = 300
    temperature    = 0.7
    top_p_sampling = 0.8
    top_k_sampling = 20
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class SkyeBlue(LlmPredictionConfig):
    max_tokens     = 300
    temperature    = 1
    top_p_sampling = 0.7
    top_k_sampling = 0
    repeat_penalty = 1
    min_p_sampling = 0

@dataclass
class Novamoon(LlmPredictionConfig):
    max_tokens     = 300
    temperature    = 1
    top_p_sampling = 0.7
    top_k_sampling = 0
    repeat_penalty = 1
    min_p_sampling = 0

@dataclass
class GLM(LlmPredictionConfig):
    max_tokens     = 300
    temperature    = 0.5
    top_p_sampling = 1
    top_k_sampling = 0
    repeat_penalty = 1
    min_p_sampling = 0

@dataclass
class ClarityForge(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 1.3
    top_p_sampling = 1
    top_k_sampling = 50
    repeat_penalty = 1.1
    min_p_sampling = 0.1

@dataclass
class Qset(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 1
    top_p_sampling = 0.92
    top_k_sampling = 0
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class DefaultQwen(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 1.31
    top_p_sampling = 0.85
    top_k_sampling = 49
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class DivineIntellect(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 1.31
    top_p_sampling = 0.14
    top_k_sampling = 49
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class MidnightEnigma(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 0.98
    top_p_sampling = 0.37
    top_k_sampling = 0
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class Shortwave(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 1.53
    top_p_sampling = 0.64
    top_k_sampling = 33
    repeat_penalty = 1.1
    min_p_sampling = 0

@dataclass
class Yara(LlmPredictionConfig):
    max_tokens     = 200
    temperature    = 0.82
    top_p_sampling = 0.21
    top_k_sampling = 72
    repeat_penalty = 1.1
    min_p_sampling = 0