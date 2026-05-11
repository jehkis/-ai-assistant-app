# Gem Scaffold

This folder is a separate scratch area for the next version of the assistant flow.

## File

- `sequence_demo.py`: a paste-ready step-by-step flow with a reserved final API step.

## Run

```bash
cd /home/joona/ai-assistant-app/gem
python3 sequence_demo.py
```

Use it like this in the final place:

```python
from gem.sequence_demo import create_demo

demo = create_demo()
print(demo.next_step("Project name"))
print(demo.next_step("First field"))
print(demo.next_step("Second field"))
print(demo.next_step("API code later"))
```

The flow fills fields in order and keeps the last step as a placeholder for the API code.
