#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys
import textwrap

import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
"https://docs.anthropic.com/en/api/getting-started"
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
"https://docs.anthropic.com/en/docs/about-claude/models"
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    textwrap.dedent(
        """
Create a diff patch containing suggested code changes that can be applied to the files
using the patch tool.

You will respond only with a valid diff file format, with no explanatory text or markdown formatting.

The files will be the Python code used to create a Django web
application. Each contents of each file in the input will be preceded by the filename
of that file, such as SORT/settings.py

Please generate all suggested changes, primarily focussed on code quality, performance,
security, and project organisation.

Please only return the patch file with no explanatory text. The output must be a valid diff syntax only."""
    ).strip(),
)

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--api_key", default=ANTHROPIC_API_KEY)
    parser.add_argument("-m", "--max_tokens", type=int, default=8192)
    parser.add_argument("-t", "--temperature", type=float, default=1.0)
    parser.add_argument("-o", "--model", default=ANTHROPIC_MODEL)
    parser.add_argument("-l", "--loglevel", default="INFO")
    parser.add_argument("-c", "--content", default=sys.stdin.read())
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


def main():
    args = get_args()
    logging.basicConfig(level=args.loglevel)

    # Set up Anthropic API access
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
    )

    text = str(args.content).strip()

    logger.info("Reviewing code...")

    # Send the contents to the Claude API
    # https://docs.anthropic.com/en/api/messages
    response = client.messages.create(
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        system=SYSTEM_PROMPT,
        messages=[
            dict(
                role="user",
                content=[
                    dict(
                        type="text",
                        # Get input from the command line
                        text=text,
                    )
                ],
            )
        ],
    )

    # Show query information
    logger.info(response.id)
    logger.info(response.model)
    logger.info(response.stop_reason)
    logger.info(response.role)
    logger.info(response.type)
    logger.info(response.usage)

    # Show results
    for i, text_block in enumerate(response.content):
        logger.info("Text block #%s type: %s", i, text_block.type)
        # Get the diff file contents only, without any explainer text
        for diff in extract_markdown_diff(text_block.text):
            print(diff)


if __name__ == "__main__":
    main()
