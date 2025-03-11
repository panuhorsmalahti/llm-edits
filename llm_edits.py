import os
import re

import click
import httpx
import llm

SYSTEM_PROMPT = """
You are an expert programmer. You are happy to help users by implementing any edits to their code or creating completely new code.
The user will provide the source for one or more files, and you must rewrite or create them to fulfill the user's request.
Your output should consist of zero or more sections in the format:

File: path/to/some_file.py
<the entire updated or newly created file content>

Then repeat that for as many files as needed. Only respond with these file sections, nothing else.
""".strip()

USER_TEMPLATE = """
Below is the user request and any code provided. Please produce the rewritten or newly created files.

Request/Prompt:
{prompt}
""".strip()

def _parse_files_from_output(text):
    """
    Parse text looking for sections of the form:

    File: path/to/file.xyz
    <content lines>
    <content lines>
    (ends at next File: or end of text)

    Returns a dict of filename -> file content.
    """
    pattern = r"(?:^|\n)File:\s*(.+?)\r?\n(.*?)(?=(?:\nFile:\s)|\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL)
    output = {}
    for filename, file_content in matches:
        # Strip trailing newlines
        file_content = file_content.rstrip("\r\n")
        filename = filename.strip()
        output[filename] = file_content
    return output


@llm.hookimpl
def register_commands(cli):
    @cli.command(name="edits")
    @click.argument("args", nargs=-1)
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    def edit(args, model, system, key):
        """
        Generate or modify multiple files based on user instructions.

        The user request and any code can be passed in as arguments or piped from stdin.
        The tool will parse the model's output for multiple file blocks:
            File: path/to/file
            <content>

        Then it will create or rewrite those files.
        """
        from llm.cli import get_default_model

        user_prompt = " ".join(args)
        if not user_prompt.strip():
            # If the user prompt was not given via args, read from stdin
            user_prompt = click.get_text_stream("stdin").read()

        # Build final prompt
        final_prompt = USER_TEMPLATE.format(prompt=user_prompt)

        # Get model
        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)

        # Invoke LLM
        result = model_obj.prompt(
            final_prompt,
            system=SYSTEM_PROMPT,
        )

        # Parse files from result
        files_dict = _parse_files_from_output(result.text())

        # Write them out
        for fpath, content in files_dict.items():
            os.makedirs(os.path.dirname(fpath), exist_ok=True) if "/" in fpath else None
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Wrote: {fpath}")

        if not files_dict:
            print("No files were found in the model's output.")
