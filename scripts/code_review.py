#!/usr/bin/env python

import argparse
import logging
import os
import sys

import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
"https://docs.anthropic.com/en/api/getting-started"

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--api_key", default=ANTHROPIC_API_KEY)
    parser.add_argument("-m", "--max_tokens", type=int, default=8192)
    parser.add_argument("-t", "--temperature", type=int, default=0)
    parser.add_argument("-o", "--model", default="claude-3-5-sonnet-20241022")
    parser.add_argument("-l", "--loglevel", default="INFO")
    parser.add_argument("-c", "--content", default=sys.stdin.read())
    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(level=args.loglevel)

    # Set up Anthropic API access
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
    )

    # Send the contents to the Claude API
    message = client.messages.create(
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        system="Create a diff patch containing suggested code changes that can be applied to the files using the patch"
        "tool. The files will be the Python code used to create a Django web application. Each contents of each"
        "file in the input will be preceded by the filename of that file, such as SORT/settings.py\n\nPlease"
        "generate all suggested changes, primarily focussed on code quality, performance, security, and project"
        "organisation.",
        messages=[
            dict(
                role="user",
                content=[
                    dict(
                        type="text",
                        # Get input from the command line
                        text=str(args.content),
                    )
                ],
            )
        ],
    )

    print(message.content)


if __name__ == "__main__":
    main()
