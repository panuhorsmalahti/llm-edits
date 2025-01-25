# LLM Edit

## Description

`llm edit` is a command line tool to edit files using large language models.
It allows users to provide a model with a file, context, and instructions to
generate or modify the file on your behalf.

## Usage Guide

```bash
# Install the tool
pip install llm-edit

# Edit a file
llm edit fizzbuzz.py create a program that solves fizzbuzz on an input number

# Add additional context files with -C
llm edit -C fizzbuzz.py fizzbuzz.js rewrite the program in js, dont use prompt

# Use any model within the `llm` ecosystem with -m
llm edit -m deepseek-v3 guide.md Write a guide on how to finetune a LLM
```

## License

This project is licensed under the Apache License, Version 2.0.

## Contributions

Contributions are welcome! Please submit a pull request with your changes.

## Acknowledgments

This project would not be possible without the `llm` library and its creator, [Simon Willison](https://simonwillison.net/),.

