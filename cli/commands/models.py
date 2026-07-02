"""Models command - List and manage LLM models."""

import click

from llm.router import ModelRouter
from llm.models import AVAILABLE_MODELS


@click.command()
@click.option('--provider', '-p', help='Filter by provider')
@click.option('--capabilities', '-c', help='Filter by capability')
@click.option('--free-only', '-f', 'free_only', is_flag=True, help='Show only FREE models')
@click.option('--json/--no-json', default=False, help='Output as JSON')
def models(provider: str, capabilities: str, free_only: bool, json: bool) -> None:
    """List available LLM models."""
    router = ModelRouter()
    
    if json:
        import json
        model_list = router.list_models(provider=provider, capability=capabilities)
        click.echo(json.dumps(model_list, indent=2))
        return
    
    click.echo("Available Models:\n")
    
    # Separate free and paid models
    free_models = [(m_id, m) for m_id, m in AVAILABLE_MODELS.items() if m.get('is_free')]
    paid_models = [(m_id, m) for m_id, m in AVAILABLE_MODELS.items() if not m.get('is_free')]
    
    if free_only:
        click.secho("=== ⭐ FREE MODELS (Recommended for Coding) ===\n", fg='green', bold=True)
        for model_id, info in free_models:
            name = info.get('name', model_id)
            desc = info.get('description', '')
            click.echo(f"  {name}")
            click.echo(f"    ID: {info['id']}")
            click.echo(f"    Description: {desc}")
            click.echo(f"    Context: {info['context_length']:,} tokens")
            click.echo(f"    Capabilities: {', '.join(info.get('capabilities', []))}")
            click.echo()
        return
    
    # Show FREE models first
    click.secho("=== ⭐ FREE CODING MODELS ===", fg='green', bold=True)
    for model_id, info in free_models:
        name = info.get('name', model_id)
        desc = info.get('description', '')
        click.echo(f"  {name}")
        click.echo(f"    {desc}")
    click.echo()
    
    click.secho("\n=== 💰 PAID MODELS ===", fg='yellow')
    
    grouped = {}
    for model_id, info in paid_models:
        p = info.get('provider', 'unknown')
        grouped.setdefault(p, []).append((model_id, info))
    
    for provider_name, model_list in grouped.items():
        if provider and provider != provider_name:
            continue
        
        click.echo(f"\n--- {provider_name.upper()} ---")
        for model_id, info in model_list:
            name = info.get('name', model_id)
            desc = info.get('description', '')
            click.echo(f"  {model_id}")
            if desc:
                click.echo(f"    {desc}")


def main() -> None:
    models()


if __name__ == '__main__':
    models()