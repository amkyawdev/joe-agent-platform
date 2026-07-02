"""Version command - Show version information."""

import click
from cli import __version__


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Show verbose version info')
@click.option('--json', is_flag=True, help='Output as JSON')
def version(verbose: bool, json: bool) -> None:
    """Show version information."""
    import sys
    import platform
    
    if json:
        import json
        info = {
            'app_version': __version__,
            'python_version': sys.version,
            'platform': platform.platform(),
            'architecture': platform.machine()
        }
        click.echo(json.dumps(info, indent=2))
        return
    
    click.echo(f"Joe-Agent-Platform v{__version__}")
    
    if verbose:
        click.echo(f"\nPython: {sys.version.split()[0]}")
        click.echo(f"Platform: {platform.platform()}")
        click.echo(f"Architecture: {platform.machine()}")


def main() -> None:
    version()


if __name__ == '__main__':
    version()