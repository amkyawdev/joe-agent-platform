"""Code command - Code generation and analysis."""

import click
from pathlib import Path

from llm.client import LLMClient
from llm.prompts import CODE_SYSTEM_PROMPT


@click.command()
@click.argument('task')
@click.option('--language', '-l', default='python', help='Programming language (python, javascript, typescript, go, rust, etc.)')
@click.option('--explain/--no-explain', default=False, help='Include code explanation')
@click.option('--test/--no-test', default=False, help='Include test code')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def code(task: str, language: str, explain: bool, test: bool, output: str) -> None:
    """Generate or analyze code."""
    client = LLMClient()
    
    prompt = f"""{CODE_SYSTEM_PROMPT}

Generate {language} code for this task: {task}

Requirements:
- Write clean, efficient, production-ready code
- Include proper error handling
- Follow {language} best practices and conventions
- Add docstrings/comments for complex logic
"""
    
    if test:
        prompt += "- Include unit tests using pytest/unittest\n"
    
    if explain:
        prompt += "- Include detailed comments explaining the code\n"
    
    click.echo(f"Generating {language} code...")
    code_response = client.complete(prompt)
    
    if output:
        Path(output).write_text(code_response)
        click.secho(f"✅ Code saved to {output}", fg='green')
    else:
        click.echo("\n" + "="*60)
        click.echo(code_response)
        click.echo("="*60 + "\n")


def main() -> None:
    code()


if __name__ == '__main__':
    code()