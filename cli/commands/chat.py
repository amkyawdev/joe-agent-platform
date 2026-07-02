"""Chat command - Interactive chat with the AI agent."""

import click
from typing import List, Dict

from llm.client import LLMClient
from agent.memory import ConversationMemory


@click.command()
@click.option('--model', '-m', help='LLM model to use')
@click.option('--system', '-s', help='System prompt')
@click.option('--history', type=int, default=10, help='Number of history messages to keep')
def chat(model: str, system: str, history: int) -> None:
    """Interactive chat session with the AI agent."""
    memory = ConversationMemory(max_messages=history)
    client = LLMClient(model=model)
    
    if system:
        memory.add_message("system", system)
    
    click.echo("Joe Chat - Type 'exit' or 'quit' to end session\n")
    
    while True:
        try:
            user_input = click.prompt("You")
            if user_input.lower() in ('exit', 'quit', 'q'):
                click.echo("Goodbye!")
                break
            
            if not user_input.strip():
                continue
            
            memory.add_message("user", user_input)
            
            messages = memory.get_messages()
            response = client.chat(messages)
            
            memory.add_message("assistant", response)
            click.echo(f"\nAssistant: {response}\n")
            
        except (KeyboardInterrupt, EOFError):
            click.echo("\nGoodbye!")
            break


def main() -> None:
    chat()


if __name__ == '__main__':
    chat()