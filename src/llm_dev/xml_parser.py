import os
import re
from rich.console import Console

console = Console()


def adjust_indentation(base_indent, content):
    """
    Preserve relative indentation while prefixing with base_indent.
    """
    lines = content.splitlines()
    if not lines:
        return ""

    # Find the minimum indentation in non-empty lines
    min_indent = min(
        (len(line) - len(line.lstrip()) for line in lines if line.strip()), default=0
    )

    # Adjust each line, preserving relative indentation
    adjusted_lines = [
        base_indent + line[min_indent:] if line.strip() else line for line in lines
    ]

    return "\n".join(adjusted_lines)


def apply_modifications(input_string):
    """
    Apply multiple modifications based on <mod> tags containing <old> and <new>.
    Supports multi-line strings and a 'path' attribute for specifying files.
    """
    # More robust regex to handle multi-line content
    mods = re.findall(
        r'<mod\s+path="([^"]+)">\s*<old>(.*?)</old>\s*<new>(.*?)</new>\s*</mod>',
        input_string,
        re.DOTALL | re.MULTILINE,
    )

    if not mods:
        raise ValueError(
            "[bold red]Error:[/bold red] No valid <mod> blocks found in the input string."
        )

    for file_path, old_code, new_code in mods:
        file_path = file_path.strip()
        old_code = old_code.strip()
        new_code = new_code.strip()

        if not os.path.exists(file_path):
            console.print(
                f"[bold red]Error:[/bold red] File '{file_path}' does not exist."
            )
            continue

        try:
            with open(file_path, "r") as file:
                file_content = file.read()

            # More robust replacement that preserves indentation
            lines = file_content.splitlines()
            updated_lines = []
            i = 0
            while i < len(lines):
                if old_code in lines[i]:
                    # Find the indentation of the current line
                    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]

                    # Split new_code into lines and indent them
                    new_lines = new_code.splitlines()
                    indented_new_lines = [f"{indent}{line}" for line in new_lines]

                    # Replace the old line with indented new lines
                    updated_lines.extend(indented_new_lines)

                    # Skip lines that match the old code
                    while i < len(lines) and old_code in lines[i]:
                        i += 1
                else:
                    updated_lines.append(lines[i])
                    i += 1

            # Write back the updated content
            updated_content = "\n".join(updated_lines)
            with open(file_path, "w") as file:
                file.write(updated_content)

            console.print(
                f"[bold green]Success:[/bold green] Modifications applied successfully to '{file_path}'."
            )

        except Exception as e:
            raise ValueError(
                f"[bold red]Error:[/bold red] Processing '{file_path}': {e}"
            )

