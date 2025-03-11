# LLM Edits

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ajac-zero/llm-edit/blob/main/LICENSE)

Use LLMs to generate and edit files in your shell

This is a plugin for [llm](https://github.com/simonw/llm),
a command line interface for both local and remote large language models.

## Description

`llm edits` is a command line tool to edit files using large language models.
It allows users to provide a model with a file, context, and instructions to
generate or modify the file on your behalf.

## Usage Guide

```bash
# Install the tool
llm install llm-edits

# Edit files
cat repomix-output.txt | llm edits -s "create a program that solves fizzbuzz on an input number"
```

## Help

```bash
# To see the CLI docs, run:
llm edits --help
```

## Acknowledgments

Based originally on https://github.com/ajac-zero/llm-edit, adding multi-file support.

## License

This project is licensed under the Apache License, Version 2.0.
