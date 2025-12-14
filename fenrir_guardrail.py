"""
Fenrir Guardrail v3.0 🐺⛓️
Lightweight inference-time mechanism to prevent multi-turn drift in LLMs.

Author: Luca Montanaro | Wolf LLM
"""

import re
import statistics
from typing import List, Dict, Tuple

class FenrirGuardrail:
    def __init__(self, session_maturity_threshold: int = 8):
        self.session_maturity_threshold = session_maturity_threshold  # Min prompts before activation
        self.prompt_history: List[str] = []
        self.entropy_history: List[float] = []
        self.baseline_entropy = 0.0
        self.session_active = False

    def _calculate_entropy_proxy(self, prompt: str) -> float:
        """Composite entropy proxy approximating 'effective temperature'."""
        if not prompt.strip():
            return 0.0

        words = prompt.split()
        num_words = len(words)
        if num_words == 0:
            return 0.0

        # 1. Length (log-scaled)
        length_score = min(num_words / 100, 1.0)  # Cap at ~100 words

        # 2. Vocabulary richness (Type-Token Ratio)
        unique_words = len(set(words))
        ttr = unique_words / num_words if num_words > 0 else 0.0

        # 3. Formality / technical markers
        technical_keywords = [
            r'\b(step by step|chain of thought|reasoning|analyze|calculate|derive|prove|implement|code|algorithm|model|training|entropy|temperature|drift|alignment)\b',
            r'[A-Za-z]+=[A-Za-z]+',  # Simple var=val pattern
            r'\b(PhD|research|paper|arxiv|github|repo|spec)\b'
        ]
        tech_matches = sum(len(re.findall(pattern, prompt, re.IGNORECASE)) for pattern in technical_keywords)
        tech_score = min(tech_matches / 10, 1.0)

        # 4. Reasoning/CoT markers
        cot_markers = ['lets think', 'step by step', 'first', 'second', 'therefore', 'conclude']
        cot_score = any(marker in prompt.lower() for marker in cot_markers)

        # Weighted composite
        entropy = (
            0.3 * length_score +
            0.25 * ttr +
            0.25 * tech_score +
            0.2 * float(cot_score)
        )
        return round(entropy, 3)

    def _update_baseline(self, new_entropy: float):
        """Exponential moving average baseline."""
        alpha = 0.15
        if self.baseline_entropy == 0.0:
            self.baseline_entropy = new_entropy
        else:
            self.baseline_entropy = alpha * new_entropy + (1 - alpha) * self.baseline_entropy

    def detect_pivot(self, current_prompt: str) -> Tuple[bool, str]:
        """Returns (is_pivot, reason)"""
        self.prompt_history.append(current_prompt)
        current_entropy = self._calculate_entropy_proxy(current_prompt)
        self.entropy_history.append(current_entropy)

        # Session not mature yet
        if len(self.prompt_history) < self.session_maturity_threshold:
            self.session_active = True
            self._update_baseline(current_entropy)
            return False, "session_not_mature"

        self._update_baseline(current_entropy)

        # Sudden shift
        delta_pct = abs((current_entropy - self.baseline_entropy) / self.baseline_entropy) if self.baseline_entropy > 0 else 0
        if delta_pct >= 0.7:
            direction = "low_to_high" if current_entropy > self.baseline_entropy else "high_to_low"
            return True, f"sudden_shift_{direction} (+{delta_pct:.1%})"

        # Sustained trend over last 3 prompts
        if len(self.entropy_history) >= 3:
            recent = self.entropy_history[-3:]
            trend_delta = (recent[-1] - recent[0]) / recent[0] if recent[0] > 0 else 0
            if abs(trend_delta) >= 0.45:
                direction = "low_to_high" if trend_delta > 0 else "high_to_low"
                return True, f"sustained_trend_{direction}"

        # Explicit mode commands (bonus trigger)
        explicit_commands = [
            "switch to chill", "yo bro", "be casual", "go deep", "phd level", "explain formally", "eli5"
        ]
        if any(cmd in current_prompt.lower() for cmd in explicit_commands):
            return True, "explicit_mode_command"

        return False, "no_pivot"

    def recalibrate_for_pivot(self, direction: str) -> Dict[str, str]:
        """Returns suggested adjustments for the LLM sampler."""
        if "low_to_high" in direction:
            return {
                "action": "precision_mode",
                "context": "compress_prior_casual",
                "sampling": "tighten (temp ×0.9, top_p -0.1)",
                "reminder": "High-complexity pivot detected. Prioritize precision and structure."
            }
        else:
            return {
                "action": "chill_mode",
                "context": "summarize_prior_technical",
                "sampling": "relax slightly",
                "reminder": "Casual shift detected. Maintain helpfulness with natural tone."
            }

# Example usage
if __name__ == "__main__":
    fenrir = FenrirGuardrail()

    test_prompts = [
        "hey bro whats up",
        "yo chill vibe",
        "tell me a joke",
        "nah explain quantum entanglement step by step with math",
        "now derive the bell inequality",
        "yo back to memes"
    ]

    for prompt in test_prompts:
        is_pivot, reason = fenrir.detect_pivot(prompt)
        print(f"Prompt: {prompt[:50]}...")
        print(f"Entropy: {fenrir.entropy_history[-1] if fenrir.entropy_history else 0}")
        print(f"Pivot: {is_pivot} | Reason: {reason}")
        if is_pivot and "shift" in reason:
            recal = fenrir.recalibrate_for_pivot(reason)
            print(f"→ Action: {recal['action']} | {recal['reminder']}")
        print("-" * 60)

