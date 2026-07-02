"""Ask command - Ask questions to the AI agent."""

import click
from llm.client import LLMClient


@click.command()
@click.argument('question')
@click.option('--model', '-m', help='LLM model to use')
@click.option('--temperature', '-t', type=float, default=0.7, help='Sampling temperature')
@click.option('--stream/--no-stream', default=False, help='Stream response')
def ask(question: str, model: str, temperature: float, stream: bool) -> None:
    """Ask a question to the AI agent."""
    client = LLMClient(model=model, temperature=temperature)
    
    if stream:
        click.echo("Thinking...")
        for chunk in client.stream(question):
            click.echo(chunk, nl=False)
        click.echo()
    else:
        with click.progressbar(length=100, label='Processing') as bar:
            response = client.complete(question)
            bar.update(100)
        
        click.echo("\n" + response)


def main() -> None:
    ask()


if __name__ == '__main__':
    main()