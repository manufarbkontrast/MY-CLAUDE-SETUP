# Message History Management

## Token Tracking

Track tokens incrementally per message pair to enable precise truncation without recalculating.

```python
class MessageHistory:
    def __init__(self, model, system, context_window_tokens, client, enable_caching=True):
        self.messages = []
        self.total_tokens = 0
        self.message_tokens = []  # List of (input_tokens, output_tokens)
        self.enable_caching = enable_caching

        # Initialize with system prompt tokens
        try:
            system_token = client.messages.count_tokens(
                model=model, system=system,
                messages=[{"role": "user", "content": "test"}],
            ).input_tokens - 1
        except Exception:
            system_token = len(system) / 4  # Fallback estimate
        self.total_tokens = system_token
```

## Adding Messages

Messages are stored with content always normalized to block format:

```python
async def add_message(self, role, content, usage=None):
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]

    self.messages.append({"role": role, "content": content})

    # Track tokens from assistant responses
    if role == "assistant" and usage:
        total_input = (
            usage.input_tokens
            + getattr(usage, "cache_read_input_tokens", 0)
            + getattr(usage, "cache_creation_input_tokens", 0)
        )
        current_turn_input = total_input - self.total_tokens
        self.message_tokens.append((current_turn_input, usage.output_tokens))
        self.total_tokens += current_turn_input + usage.output_tokens
```

**Key insight**: `current_turn_input` is calculated by subtracting the running total from the API-reported input tokens. This captures exactly how many tokens the new message pair added.

## Smart Truncation

Removes oldest message **pairs** (user + assistant) to maintain conversation coherence:

```python
def truncate(self):
    if self.total_tokens <= self.context_window_tokens:
        return

    TRUNCATION_NOTICE_TOKENS = 25
    TRUNCATION_MESSAGE = {
        "role": "user",
        "content": [{"type": "text", "text": "[Earlier history has been truncated.]"}],
    }

    while (
        self.message_tokens
        and len(self.messages) >= 2
        and self.total_tokens > self.context_window_tokens
    ):
        # Remove oldest user + assistant pair
        self.messages.pop(0)
        self.messages.pop(0)

        input_tokens, output_tokens = self.message_tokens.pop(0)
        self.total_tokens -= input_tokens + output_tokens

        # Replace first remaining message with truncation notice
        if self.messages and self.message_tokens:
            self.messages[0] = TRUNCATION_MESSAGE
            orig_input, orig_output = self.message_tokens[0]
            self.message_tokens[0] = (TRUNCATION_NOTICE_TOKENS, orig_output)
            self.total_tokens += TRUNCATION_NOTICE_TOKENS - orig_input
```

**Why pairs?** Removing a single user or assistant message would break the alternating role pattern that the Claude API requires.

## Prompt Caching

Add `cache_control` to the last message for cost savings in repeated agent loops:

```python
def format_for_api(self):
    result = [{"role": m["role"], "content": m["content"]} for m in self.messages]

    if self.enable_caching and self.messages:
        result[-1]["content"] = [
            {**block, "cache_control": {"type": "ephemeral"}}
            for block in self.messages[-1]["content"]
        ]
    return result
```

**Why only the last message?** In an agent loop, all previous messages are identical between iterations. Caching the last message means the API can reuse the cached prefix for the next call, saving input token costs.

## Configuration

```python
@dataclass
class ModelConfig:
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 1.0
    context_window_tokens: int = 180000  # Leave headroom below 200k
```

Set `context_window_tokens` below the actual model limit to leave room for the response.
