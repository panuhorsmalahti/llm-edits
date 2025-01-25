import click
import llm

SYSTEM_PROMPT = """
You are an expert programmer. You are happy to help users by implementing any edits to their code or creating completely new code.
The user will provide you with a file, and you must rewrite it to fulfill the user's request.
Do not provide any other information.
Do not create any new files.
""".strip()

USER_TEMPLATE = """
<file path={file}>
{content}
</file>

<prompt>
{prompt}
</prompt>
""".strip()


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("file", type=click.Path())
    @click.argument("args", nargs=-1)
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    def dev(file, args, model, system, key):
        """Generate and rewrite files in your shell"""
        from llm.cli import get_default_model

        with open(file, "r") as f:
            prompt = USER_TEMPLATE.format(
                file=file, content=f.read(), prompt=" ".join(args)
            )

        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)

        result = model_obj.prompt(prompt, system=system or SYSTEM_PROMPT)

        with open(file, "w") as f:
            f.write(result.text())
