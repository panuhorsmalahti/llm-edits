import click
import gitingest
import llm

from .xml_parser import apply_modifications
from .prompts import SYSTEM_PROMPT, CONTEXT_PROMPT, USER_PROMT


def create_context(
    source,
    include_patterns: list[str] | str,
    exclude_patterns: list[str] | str,
):
    _, _, content = gitingest.ingest(
        source=source,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    context_prompt = CONTEXT_PROMPT.format(content=content)

    return context_prompt


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("file", type=click.Path(exists=True))
    @click.argument("prompt")
    @click.option("-m", "--model", default=None, help="Specify the model to use.")
    @click.option(
        "-C",
        "--context",
        default=None,
        type=click.Path(),
        help="Specify the path to use as additional context.",
    )
    @click.option(
        "-i", "--include", default=[], help="Patterns to include from the context dir"
    )
    @click.option(
        "-e", "--exclude", default=[], help="Patterns to exclude from the context dir"
    )
    @click.option("--key", help="Specify the key to use.")
    def dev(file, prompt, context, model, include, exclude, key):
        """Generate and apply a git diff"""
        from llm.cli import get_default_model

        model_obj = llm.get_model(model or get_default_model())
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)

        if context:
            exclude.append(file)
            system_prompt = create_context(
                source=context, include_patterns=include, exclude_patterns=exclude
            )
        else:
            system_prompt = SYSTEM_PROMPT

        with open(file, "r") as f:
            content = f.read()

        user_prompt = USER_PROMT.format(file=file, content=content, prompt=prompt)

        generation = model_obj.prompt(prompt=user_prompt, system=system_prompt)
        print(generation)

        apply_modifications(generation.text())
