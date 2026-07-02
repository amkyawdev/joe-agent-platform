"""Analyze command - Analyze text, code, or documents."""

import click
from pathlib import Path

from llm.client import LLMClient
from agent.reasoning import Analyzer


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--type', '-t', type=click.Choice(['text', 'code', 'document']), default='text')
@click.option('--aspects', '-a', multiple=True, help='Aspects to analyze')
def analyze(input_path: str, type: str, aspects: tuple) -> None:
    """Analyze text, code, or documents."""
    content = Path(input_path).read_text()
    analyzer = Analyzer()
    client = LLMClient()
    
    if aspects:
        analysis_types = list(aspects)
    else:
        analysis_types = ['key_points', 'sentiment', 'structure']
    
    results = analyzer.analyze(content, analysis_types=analysis_types)
    
    click.echo("\n=== Analysis Results ===\n")
    for aspect, result in results.items():
        click.echo(f"\n{aspect.replace('_', ' ').title()}:")
        click.echo(f"  {result}")


def main() -> None:
    analyze()


if __name__ == '__main__':
    analyze()