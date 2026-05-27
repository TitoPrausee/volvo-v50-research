# Ollama Cloud Models — Agenten-Referenz

> Stand: Mai 2026 · Quelle: ollama.com/search?c=cloud  
> Alle Modelle erfordern ollama signin und Ollama ≥ v0.12

## Modelle nach Kategorie

### 💻 Coding
| Modell-ID | Stärken | Tags | Compute-Level |
|---|---|---|---|
| glm-5.1:cloud | State-of-the-art Coding, SWE-Bench Pro | tools, thinking | 3 |
| qwen3-coder-next:cloud | Agentic Coding Workflows, Tool-Nutzung | tools | 2 |
| devstral-small-2:24b-cloud | 24B, Codebase-Exploration, Multi-File Editing | vision, tools | 2 |
| minimax-m2.1:cloud | Multilingual, stark im Code Engineering | tools | 2 |
| rnj-1:8b-cloud | 8B, Code + STEM | tools | 1 |

### 🧠 Reasoning
| Modell-ID | Stärken | Tags | Compute-Level |
|---|---|---|---|
| deepseek-v4-pro:cloud | Frontier MoE, 1M-Token Kontext, 3 Reasoning-Modi | tools, thinking | 4 |
| deepseek-v4-flash:cloud | 284B MoE, 13B aktiv, schnell + effizient | tools, thinking | 3 |
| deepseek-v3.2:cloud | Hohe Effizienz, Agentic-Workflows | tools, thinking | 3 |
| qwen3-next:80b-cloud | 80B, gute Efficiency | tools, thinking | 3 |

### 🤖 Agentic / Multi-Agent
| Modell-ID | Stärken | Tags | Compute-Level |
|---|---|---|---|
| glm-5:cloud | 744B/40B aktiv, Long-horizon Tasks | tools, thinking | 4 |
| kimi-k2.6:cloud | Multimodal, Swarm-Orchestration | vision, tools, thinking | 4 |
| nemotron-3-super:120b-cloud | 120B MoE, Multi-Agent | tools, thinking | 3 |
| minimax-m2.7:cloud | Coding + Agentic + Produktivität | tools, thinking | 3 |
| nemotron-3-nano:cloud | 4-30B, effizient, leichte Parallelaufgaben | tools, thinking | 1 |

### 🌐 Multimodal / Vision
| Modell-ID | Stärken | Tags | Compute-Level |
|---|---|---|---|
| gemma4:cloud | Frontier, Multimodal inkl. Audio | vision, tools, thinking | 3 |
| qwen3.5:cloud | Multimodal, 0.8b–122b | vision, tools, thinking | 2 |
| gemini-3-flash-preview:cloud | Speed + niedrige Kosten | vision, tools, thinking | 2 |
| ministral-3:cloud | Edge, multimodal, 3-14B | vision, tools | 1 |

## Rollen-Mapping für Agenten
| Rolle | Modell | Begründung |
|---|---|---|
| Research / Web-Suche | qwen3.5:cloud | Flexibel, gute Tool-Nutzung |
| Coding | glm-5.1:cloud | Bestes Coding-Modell |
| Orchestrator | kimi-k2.6:cloud | Swarm-nativ |
| Schnelle Subtasks | gemini-3-flash-preview:cloud | Speed |
| Reasoning | deepseek-v4-pro:cloud | 1M Kontext |
| Creative | gemma4:cloud | Vision + Audio |