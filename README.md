# 🧠 Language Interpreter

*A step-by-step implementation of a simple interpreter for a tiny arithmetic language, featuring a lexer, parser (AST), and interpreter with variables and assignment.*

<br>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<br>

## 📖 About The Project

This project explores the fascinating world of programming language design by building a complete interpreter from the ground up. It demonstrates the fundamental phases involved in processing code: lexical analysis (tokenization), syntactic analysis (parsing to an Abstract Syntax Tree - AST), and interpretation (execution).

Starting with basic arithmetic, the language progressively adds features like variables and assignment, culminating in an interactive Read-Eval-Print Loop (REPL). This project offers deep insights into compilers and interpreters, showing how human-readable code is transformed into executable actions.

## ✨ Key Features

* **Lexer (Tokenizer):** Converts raw input text into a stream of meaningful tokens (numbers, operators, identifiers, parentheses).
* **Parser (Syntax Analyzer):** Takes the token stream and constructs an Abstract Syntax Tree (AST), representing the hierarchical structure and order of operations of the code. Utilizes recursive descent parsing.
* **Interpreter (Evaluator):** Traverses the AST to perform computations, evaluating arithmetic expressions.
* **Arithmetic Operations:** Supports addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`) with correct operator precedence and parentheses handling.
* **Variables & Assignment:** Allows declaring and using variables (e.g., `x = 10`, `y = x + 5`).
* **Global Scope:** Manages variable storage in a simple global symbol table.
* **Interactive REPL:** Provides a command-line interface to type expressions and statements, and see immediate results.
* **Error Handling:** Includes basic error reporting for lexing, parsing, and runtime issues (e.g., undefined variables, division by zero, invalid syntax).

## 🚀 How It Works

The interpreter follows a three-stage pipeline:

1.  **Lexical Analysis (Lexer):** Reads the input string character by character, identifying sequences that form distinct tokens (e.g., '1', '2', '3' become the INTEGER token '123'). It skips whitespace and reports invalid characters.
2.  **Syntactic Analysis (Parser):** Consumes the token stream from the Lexer and verifies that the sequence of tokens conforms to the language's grammar rules. It then constructs an Abstract Syntax Tree (AST), which is a hierarchical representation of the program's structure (e.g., identifying expressions, terms, factors, and assignments).
3.  **Interpretation (Interpreter):** Traverses the generated AST. For each node in the tree, it performs the corresponding action: retrieving variable values, storing assigned values, or executing arithmetic operations. The `NodeVisitor` pattern is used for clean AST traversal.

The REPL continuously reads a line of input, passes it through this pipeline, prints the result (if any), and then loops back for the next input.

## 🛠️ Built With

* **Python 3.x:** Core programming language.
* **Standard Library:** Primarily `enum` for token types.

## 🏁 Getting Started

To get the tiny language interpreter running locally:

### Prerequisites

* Python 3.x installed on your system.

### Installation

1.  Clone this repository to your local machine:
    ```sh
    git clone https://github.com/DiegoNatanael/language-interpreter.git
    ```
2.  Navigate into the project directory:
    ```sh
    cd language-interpreter
    ```

### Usage

1.  Run the interpreter from your terminal:
    ```sh
    python interpreter.py
    ```
2.  You will see a `calc>` prompt. Type in expressions or assignment statements:

    ```
    calc> x = 10 + 5
    calc> x * 2
    30
    calc> y = (x + 10) / 5
    calc> y
    5.0
    calc> hello_world = 42
    calc> hello_world + 8
    50
    calc> 10 / 0
    Error: Runtime error: Division by zero
    calc> exit
    ```
3.  Type `exit` or `quit` and press Enter to exit the REPL.

## 📜 License

All Rights Reserved. © 2025 Diego Natanael Gonzalez Esparza

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby denied.

## 📬 Contact

Project Link: [https://github.com/DiegoNatanael/language-interpreter](https://github.com/DiegoNatanael/language-interpreter)
