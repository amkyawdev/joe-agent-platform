"""Search command - Search and retrieve information."""

import click

from rag.retriever import Retriever
from rag.generator import AnswerGenerator


@click.command()
@click.argument('query')
@click.option('--top-k', '-k', type=int, default=5, help='Number of results')
@click.option('--collection', '-c', default='default', help='Vector collection name')
@click.option('--stream/--no-stream', default=False, help='Stream response')
def search(query: str, top_k: int, collection: str, stream: bool) -> None:
    """Search for information using RAG."""
    retriever = Retriever(collection_name=collection)
    generator = AnswerGenerator()
    
    results = retriever.search(query, top_k=top_k)
    
    click.echo(f"Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        click.echo(f"{i}. Score: {result['score']:.4f}")
        click.echo(f"   {result['content'][:200]}...")
        click.echo()
    
    if stream:
        context = "\n".join([r['content'] for r in results])
        answer = generator.generate(query, context, stream=True)
        for chunk in answer:
            click.echo(chunk, nl=False)
        click.echo()


def main() -> None:
    search()


if __name__ == '__main__':
    search()