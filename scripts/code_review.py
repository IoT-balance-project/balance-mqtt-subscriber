#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys
import textwrap
from pathlib import Path

import langchain_core.messages
import langchain_core.language_models

MODEL = os.getenv("MODEL", "claude-3-5-haiku-latest")
"https://docs.anthropic.com/en/docs/about-claude/models"
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    textwrap.dedent(
        """
Create a diff file containing suggested code changes that can be applied to the files using the patch tool in Linux.

Respond only with a valid diff file format. It must be the output of the Linux command git diff. The output must be
valid input to the command `patch`.

The contents of each file in the input will be contained inside XML tags for example
<file path="src/my_module/__main__.py"></file>
"""
    ).strip(),
)

logger = logging.getLogger(__name__)


def input_file(x) -> str:
    """Either read input data or open file path"""
    if not x:
        return sys.stdin.read()
    with Path(x).open() as file:
        return file.read()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--api_key")
    parser.add_argument("-m", "--max_tokens", type=int, default=8192)
    parser.add_argument("-t", "--temperature", type=float, default=1.0)
    parser.add_argument("-o", "--model", default=MODEL)
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        help="Verbosity",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument("-c", "--content", type=input_file)
    parser.add_argument("-s", "--system", default=SYSTEM_PROMPT, help="System prompt")
    return parser.parse_args()


def extract_markdown_diff(markdown: str) -> list[str]:
    """
    Extracts diff content from markdown-formatted text that uses ```diff code blocks.

    Args:
        markdown (str): The input text containing markdown-formatted diff content

    Returns:
        List[str]: A list of extracted diff contents, with each element being the
                  content between ```diff and ``` markers. Returns an empty list
                  if no diffs are found.
    """

    # Look for content between ```diff and ``` markers
    diff_pattern = r"```diff\n(.*?)```"
    matches = re.findall(diff_pattern, markdown, re.DOTALL)

    # Clean up any trailing whitespace in the matches
    for diff in matches:
        yield diff.rstrip()


def get_model(model_name: str, **kwargs) -> langchain_core.language_models.BaseLanguageModel:
    if model_name.startswith("claude"):

        if not os.environ.get("ANTHROPIC_API_KEY"):
            import getpass
            os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

        from langchain_anthropic import ChatAnthropic

        model = ChatAnthropic(model=model_name, **kwargs)

    else:
        import langchain_ollama.chat_models

        model = langchain_ollama.chat_models.ChatOllama(model=model_name, **kwargs)

    return model


def main():
    args = get_args()
    logging.basicConfig(level=args.log_level)

    # Configure LLM
    model = get_model(args.model, temperature=args.temperature, max_tokens=args.max_tokens)

    # Build request
    text = str(args.content).strip()
    messages = [
        # System message
        langchain_core.messages.SystemMessage(args.system),
        # Prompt text
        langchain_core.messages.HumanMessage(text)
    ]

    logger.info("Invoking model...")
    message: langchain_core.messages.AIMessage = model.invoke(messages)

    logger.info(message.id)
    logger.info(message.response_metadata)
    logger.info(message.usage_metadata)
    print(message.content)


if __name__ == "__main__":
    main()
