import click
import llm
import os

SYSTEM_PROMPT = """
You are an expert programmer. You are happy to help users by implementing any edits to their code or creating completely new code.
The user will provide you with a file, and you must rewrite it to fulfill the user's request.
Do not provide any other information.
Do not create any new files.
Do not use code blocks.
Only respond with the rewritten file contents.
""".strip()

USER_TEMPLATE = """
{prompt}

```
{content}
```
""".strip()

CONTEXT_TEMPLATE = """
{file}
```
{content}
```
"""


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("file", type=click.Path())
    @click.argument("args", nargs=-1)
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    @click.option(
        "-C", "--context", multiple=True, help="Paths to additional context files"
    )
    def edit(file, args, model, system, key, context):
        """Generate and rewrite files in your shell"""
        from llm.cli import get_default_model

        if not os.path.exists(file):
            with open(file, "w") as f:
                pass

        with open(file, "r") as f:
            content = f.read()
            prompt = USER_TEMPLATE.format(content=content, prompt=" ".join(args))
            if context:
                for ctx_file in context:
                    if os.path.exists(ctx_file):
                        with open(ctx_file, "r") as cf:
                            ctx_content = cf.read()
                            prompt += "\n\n" + CONTEXT_TEMPLATE.format(
                                file=ctx_file, content=ctx_content
                            )
                    else:
                        print(f"Context file {ctx_file} not found. Skipping.")

        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)

        result = model_obj.prompt(prompt, system=system or SYSTEM_PROMPT)

        with open(file, "w") as f:
            f.write(result.text())
