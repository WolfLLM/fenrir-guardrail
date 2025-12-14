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
