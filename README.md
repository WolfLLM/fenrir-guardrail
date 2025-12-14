# Fenrir Guardrail v3.0 🐺⛓️

Lightweight, inference-time mechanism to enhance multi-turn stability in LLMs during abrupt or gradual mode shifts (casual ↔ technical).

Inspired by the Norse wolf Fenrir — bound by Gleipnir to hold back chaos until the right moment.

## Problem
In long sessions, sudden prompt complexity changes cause:
- Tone whiplash
- Factual drift & hallucinations
- Structural breakdown

## Solution
- Adaptive rate-of-change detection in prompt entropy (bidirectional, relative %)
- Session maturity gating
- Direction-specific context recalibration
- Task Alignment Metrics (TAM) refresh for coherence/safety

Zero retraining required. Full synergy with existing safety layers.

## Core Features
- Entropy Proxy (length + vocab + formality + reasoning markers)
- Trigger thresholds: |Δ%| ≥70% single or ≥45% over 3 prompts
- Actions: context compression, sampling tweaks, system reminders
- TAM: 5 weighted metrics with regeneration on failure

## Estimated Impact (Hypothetical)
| Failure Mode            | Without Fenrir | With Fenrir |
|-------------------------|----------------|-------------|
| Tone Whiplash           | 75%            | 15%         |
| Factual Drift           | 60%            | 12%         |
| Structural Collapse     | 65%            | 10%         |
| Pro-Social Slip         | 20%            | 5%          |
| Overall Stability       | 45%            | 85%         |

## Author
WolfLLM

Open to collaboration on the right projects.


## Liability Disclaimer

Fenrir Guardrail is provided free of charge and "AS IS," without any warranty or guarantee of any kind. By downloading, using, or modifying this software, you agree to the following:

1. **No Warranty**: There is no warranty for the program, to the extent permitted by applicable law. Except when otherwise stated in writing, the copyright holders and/or other parties provide the program "AS IS" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the program is with you. Should the program prove defective, you assume the cost of all necessary servicing, repair, or correction.

2. **Limitation of Liability**: In no event unless required by applicable law or agreed to in writing will any copyright holder, or any other party who modifies and/or conveys the program as permitted above, be liable to you for damages, including any general, special, incidental, or consequential damages arising out of the use or inability to use the program (including but not limited to loss of data or data being rendered inaccurate or losses sustained by you or third parties or a failure of the program to operate with any other programs), even if such holder or other party has been advised of the possibility of such damages.

3. **User Acknowledgment**: By using this software, you acknowledge that you have read this disclaimer, understand it, and agree to be bound by its terms.

This disclaimer is governed by the laws of [Your Jurisdiction, e.g., Canada]. If any provision is found to be unenforceable, the remaining provisions remain in effect.

Date: December 14, 2025  
Author: Luca Montanaro
