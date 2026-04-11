# Ports

Ports are the interfaces the application layer defines to communicate with the outside world.

They are Protocols — Python's structural typing mechanism. The application layer
depends on these abstractions. Infrastructure provides the concrete implementations.
The application never imports from infrastructure directly.

## The dependency rule

```
application/ports/  ←  defines the interface
infrastructure/     ←  implements the interface
```

The application does not care whether routing is done by Gemini, OpenAI, or a
keyword matcher. It calls `classifier.classify(summary)` and receives a
`RoutingClassification`. Swapping the implementation requires no change to the
use case.

## Current ports

| Port | File | Implemented by |
|---|---|---|
| `RoutingClassifier` | `classifier.py` | `RuleBasedRoutingClassifier`, `GeminiRoutingClassifier`, `OpenAIRoutingClassifier`, `FallbackRoutingClassifier` |
| `LiveRoutingClassifier` | `classifier.py` | `GeminiRoutingClassifier`, `OpenAIRoutingClassifier` |

## Adding a new port

1. Define a `Protocol` class here with the minimum interface the use case needs
2. Implement it in `src/infrastructure/`
3. Inject the implementation in `src/interface/api/main.py`

Keep ports small. A port with one method is better than a port with five.
