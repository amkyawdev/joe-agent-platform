"""Summarize command - Summarize text or documents."""

import click
from pathlib import Path

from llm.client import LLMClient


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--length', '-l', type=click.Choice(['short', 'medium', 'long']), default='medium')
@click.option('--format', '-f', type=click.Choice(['bullet', 'paragraph']), default='paragraph')
def summarize(input_path: str, length: str, format: str) -> None:
    """Summarize a text file or document."""
    content = Path(input_path).read_text()
    
    length_map = {
        'short': '2-3 sentences',
        'medium': '1-2 paragraphs',
        'long': 'detailed summary with key points'
    }
    
    format_map = {
        'bullet': 'bullet points',
        'paragraph': 'paragraph format'
    }
    
    prompt = f"""Summarize the following content:
    
{content}

Requirements:
- Length: {length_map[length]}
- Format: {format_map[format]}
- Focus on key information and main ideas."""
    
    client = LLMClient()
    summary = client.complete(prompt)
    
    click.echo("\n=== Summary ===\n")
    click.echo(summary)


def main() -> None:
    summarize()


if __name__ == '__main__':
    summarize()