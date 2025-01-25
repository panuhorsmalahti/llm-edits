import click
import gitingest
import llm
from llm.cli import get_default_model

from .prompts import CONTEXT_PROMPT, SYSTEM_PROMPT, USER_PROMPT
from .xml_parser import apply_modifications


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("file", type=click.Path(exists=True))
    @click.argument("prompt")
    @click.option("-m", "--model", default=None, help="Specify the model to use.")
    @click.option("-d", "--context-dir", type=click.Path(exists=True))
    def dev(file, prompt, context_dir, model):
        model_obj = llm.get_model(model or get_default_model())

        if model_obj.needs_key:
            model_obj.key = llm.get_key(
                None, model_obj.needs_key, model_obj.key_env_var
            )

        if context_dir:
            _, _, content = gitingest.ingest(
                source=context_dir,
                exclude_patterns=[file],
            )

            system_prompt = (
                SYSTEM_PROMPT + "\n\n" + CONTEXT_PROMPT.format(content=content)
            )
        else:
            system_prompt = SYSTEM_PROMPT

        with open(file, "r") as f:
            content = f.read()

        user_prompt = USER_PROMPT.format(file=file, content=content, prompt=prompt)

        generation = model_obj.prompt(prompt=user_prompt, system=system_prompt)

        apply_modifications(generation.text())
