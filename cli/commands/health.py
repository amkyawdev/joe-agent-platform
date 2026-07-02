"""Health command - Check system health status."""

import click
import asyncio
from typing import Dict, Any

from monitoring.health import HealthChecker


@click.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed health info')
@click.option('--watch', '-w', is_flag=True, help='Watch mode')
def health(detailed: bool, watch: bool) -> None:
    """Check system health status."""
    checker = HealthChecker()
    
    if watch:
        click.echo("Watching health status (Ctrl+C to stop)...\n")
        try:
            while True:
                display_health(checker, detailed)
                import time
                time.sleep(5)
                click.clear()
        except KeyboardInterrupt:
            click.echo("\nStopped watching")
    else:
        display_health(checker, detailed)


def display_health(checker: HealthChecker, detailed: bool) -> None:
    """Display health check results."""
    status = asyncio.run(checker.check_all())
    
    overall = status.get('status', 'unknown')
    color = 'green' if overall == 'healthy' else 'red'
    
    click.echo(f"Overall Status: ", nl=False)
    click.secho(overall.upper(), fg=color, bold=True)
    click.echo()
    
    services = status.get('services', {})
    for service, info in services.items():
        service_status = info.get('status', 'unknown')
        color = 'green' if service_status == 'healthy' else 'yellow' if service_status == 'degraded' else 'red'
        
        click.echo(f"  {service}: ", nl=False)
        click.secho(service_status, fg=color)
        
        if detailed and 'details' in info:
            click.echo(f"    Details: {info['details']}")
        
        if detailed and 'latency_ms' in info:
            click.echo(f"    Latency: {info['latency_ms']:.2f}ms")


def main() -> None:
    health()


if __name__ == '__main__':
    health()