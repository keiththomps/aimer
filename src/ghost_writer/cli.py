"""
Entrypoint for Ghost Writer, responsible for the CLI commands
and handling user input.
"""

import os
import sys

import click

from .prompts import build_system_prompt, fetch_system_prompt
from .ai_providers import get_provider


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Ghost writer leverages LLMs function calling capability to allow AI to write
    code for you based on a prompt while leveraging context from files that you provide.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(write)


@cli.command()
@click.option(
    "--ai",
    "-a",
    type=click.Choice(["OpenAI", "Anthropic"], case_sensitive=False),
    default="Anthropic",
    help="AI Provider.",
)
@click.option(
    "--model",
    "-m",
    help="Large language model to use.",
)
@click.option("--dry-run", "-d", is_flag=True, help="Dry run mode.")
@click.option("--output", "-o", default=None, help="Output file.")
@click.option("--system-prompt", "-s", help="Custom system prompt to use.")
@click.argument("prompt", nargs=1)
@click.argument("files", nargs=-1)
# pylint: disable=too-many-arguments
def write(ai, model, dry_run, output, system_prompt, prompt, files):
    """
    [Default Command] Perform code actions based on a prompt.
    """
    try:
        prompt_start = fetch_system_prompt(system_prompt)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}")
        click.echo("Consider running `ghost config` to create a default prompt.")
        sys.exit(1)

    provider = get_provider(ai, model)
    result = provider.send_message(prompt_start, prompt, files)
    print(result)


@cli.command()
def config():
    """
    Interactive multi-step process to build an LLM prompt.
    """
    click.echo("Welcome to the LLM prompt configuration!")

    # Ask for project languages
    project_languages = click.prompt(
        "\nWhat languages are used in your project?", type=str
    )

    # Ask for project frameworks
    project_frameworks = click.prompt(
        "\nWhat frameworks are used in your project?", type=str
    )

    # Ask if comments in code are desired
    comments_in_code = click.confirm(
        "\nDo you want comments in the code?", default=True
    )

    # Ask if automated tests are desired
    automated_tests = click.confirm(
        "\nWould you like automated tests provided for the code?", default=True
    )
    testing_frameworks = []
    if automated_tests:
        testing_frameworks = click.prompt(
            "\nWhat testing framework(s) would you like to use?", type=str
        ).split(",")

    # Ask if an example test case should be provided
    example_test_case = None
    if automated_tests and click.confirm(
        "\nWould you like to provide an example of how you want a test to be written?",
        default=False,
    ):
        example_test_case = click.edit("\nWrite an example test case:\n")

    # Build the system prompt
    system_prompt = build_system_prompt(
        project_languages,
        project_frameworks,
        comments_in_code,
        automated_tests,
        testing_frameworks,
        example_test_case,
    )

    click.echo("\nYour system prompt:\n")
    click.echo(system_prompt)

    confirm = click.confirm("\nDo you want to save this prompt?", default=True)
    if confirm:
        prompt_dir = os.path.join(os.getcwd(), ".ghost")
        os.makedirs(prompt_dir, exist_ok=True)
        prompt_file = os.path.join(prompt_dir, "default_prompt.txt")
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(system_prompt)
        click.echo(f"System prompt saved to {prompt_file}")
    else:
        click.echo("System prompt not saved.")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter