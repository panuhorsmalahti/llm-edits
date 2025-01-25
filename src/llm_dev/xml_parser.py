import os
import re


def adjust_indentation(base_indent, content):
    """
    Adjust the indentation of the content to match the given base_indent.
    """
    lines = content.splitlines()
    adjusted_lines = [(base_indent + line if line.strip() else line) for line in lines]
    return "\n".join(adjusted_lines)


def apply_modifications(input_string):
    """
    Apply multiple modifications based on <mod> tags containing <old> and <new>.
    Supports multi-line strings and a 'path' attribute for specifying files.
    """
    # Find all <mod> blocks with path, <old>, and <new> tags
    mods = re.findall(
        r'<mod path="(.*?)">\s*<old>(.*?)</old>\s*<new>(.*?)</new>\s*</mod>',
        input_string,
        re.DOTALL,
    )

    if not mods:
        print("Error: No valid <mod> blocks found in the input string.")
        return

    for file_path, old_code, new_code in mods:
        file_path = file_path.strip()
        old_code = old_code.strip()
        new_code = new_code.strip()

        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            continue

        try:
            # Read the content of the file
            with open(file_path, "r") as file:
                file_content = file.read()

            # Locate the old_code in the file
            match = re.search(re.escape(old_code), file_content)
            if not match:
                print(f"Warning: Code block not found in '{file_path}'. Skipping.")
                continue

            # Determine the base indentation of the old_code
            start_index = match.start()
            # Find the start of the line containing old_code
            line_start_index = file_content.rfind('\n', 0, start_index) + 1
            # Get the indentation (whitespace at the start of the line containing old_code)
            base_indent_match = re.match(r"(\s*)", file_content[line_start_index:start_index])
            base_indent = base_indent_match.group(1) if base_indent_match else ''

            # Adjust the indentation of the new_code to match the base_indent
            adjusted_new_code = adjust_indentation(base_indent, new_code)

            # Replace old_code with the adjusted new_code
            updated_content = file_content.replace(old_code, adjusted_new_code)

            # Write the updated content back to the file
            with open(file_path, "w") as file:
                file.write(updated_content)

            print(f"Modifications applied successfully to '{file_path}'.")

        except Exception as e:
            print(f"An error occurred while processing '{file_path}': {e}")
