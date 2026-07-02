"""Config command - Manage configuration settings."""

import click
from pathlib import Path

from config.settings import Settings
from dotenv import load_dotenv


@click.command()
@click.option('--list', '-l', 'list_all', is_flag=True, help='List all configuration')
@click.option('--get', '-g', help='Get specific config value')
@click.option('--set', '-s', nargs=2, help='Set config value')
@click.option('--reset', '-r', is_flag=True, help='Reset to default')
@click.option('--export', '-e', type=click.Path(), help='Export config to file')
def config(list_all: bool, get: str, set: tuple, reset: bool, export: str) -> None:
    """Manage configuration settings."""
    settings = Settings()
    
    if reset:
        if Path('.env').exists():
            Path('.env').unlink()
        click.echo("Configuration reset to defaults")
        return
    
    if export:
        export_config(export, settings)
        click.echo(f"Configuration exported to {export}")
        return
    
    if set:
        key, value = set
        set_config(key, value)
        click.echo(f"Set {key} = {value}")
        return
    
    if get:
        value = get_config(get, settings)
        click.echo(f"{get} = {value}")
        return
    
    if list_all:
        list_all_config(settings)
        return
    
    click.echo("Use --help to see available options")


def list_all_config(settings: Settings) -> None:
    """List all configuration values."""
    config_dict = settings.model_dump()
    for key, value in config_dict.items():
        if not key.startswith('_'):
            click.echo(f"{key} = {value}")


def get_config(key: str, settings: Settings) -> str:
    """Get a specific config value."""
    return getattr(settings, key, 'Not found')


def set_config(key: str, value: str) -> None:
    """Set a configuration value in .env file."""
    env_path = Path('.env')
    if not env_path.exists():
        Path('.env.example').write_text(env_path.read_text())
    
    load_dotenv(env_path)
    
    lines = env_path.read_text().splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    
    if not found:
        lines.append(f"{key}={value}")
    
    env_path.write_text('\n'.join(lines) + '\n')


def export_config(path: str, settings: Settings) -> None:
    """Export configuration to a file."""
    config_dict = {k: v for k, v in settings.model_dump().items() if not k.startswith('_')}
    import json
    Path(path).write_text(json.dumps(config_dict, indent=2))


def main() -> None:
    config()


if __name__ == '__main__':
    config()