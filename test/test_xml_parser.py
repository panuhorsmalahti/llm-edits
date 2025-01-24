from llm_dev.xml_parser import apply_modifications

# Example usage:
if __name__ == "__main__":
    # Path to the code file
    file_path = "example_code.py"

    # Input string with multi-line <old> and <new> content
    input_string = """
    <mod>
        <old>
        def greet():
            print("Hello, World!")
            print("This is the old version.")
        </old>
        <new>
        def greet():
            print("Hello, Python!")
            print("This is the new version.")
        </new>
    </mod>
    <mod>
        <old>
        if x == 5:
            print("Old condition met.")
        </old>
        <new>
        if x == 10:
            print("New condition met.")
        </new>
    </mod>
    """

    apply_modifications(file_path, input_string)
