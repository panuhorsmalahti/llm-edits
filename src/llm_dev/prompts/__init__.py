import os

prompt_dir = os.path.dirname(__file__)

with open(os.path.join(prompt_dir, "system.txt"), "r") as f:
    SYSTEM_PROMPT = f.read()

with open(os.path.join(prompt_dir, "context.txt"), "r") as f:
    CONTEXT_PROMPT = f.read()

with open(os.path.join(prompt_dir, "user.txt"), "r") as f:
    USER_PROMPT = f.read()

