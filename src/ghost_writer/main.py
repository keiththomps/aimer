import click

@click.command()
@click.option("--ai", "-a", type=click.Choice(["OpenAI", "Anthropic"], case_sensitive=False), default="OpenAI", help="AI Provider.")
@click.option("--model", "-m", default="gpt-4-turbo", help=f"Large language model to use.")
@click.option("--dry-run", "-d", is_flag=True, help="Dry run mode.")
@click.option("--output", "-o", default=None, help="Output file.")
@click.option("--system-prompt", "-s", help="Custom system prompt to use.")
@click.argument("prompt", nargs=1)
@click.argument("files", nargs=-1)
def main(ai, model, dry_run, output, system_prompt, prompt, files):
    """
    Ghost writer leverages LLMs function calling capability to allow AI to write
    code for you based on a prompt while leveraging context from files that you provide.
    """
    import pdb; pdb.set_trace()
    pass

if __name__ == '__main__':
    main()
