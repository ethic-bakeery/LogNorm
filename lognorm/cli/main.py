import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """LogNorm — Convert raw Linux logs into structured, normalized output."""
    pass

@cli.command()
@click.argument("files", nargs=-1, required=False)
@click.option("--stdin", "use_stdin", is_flag=True, help="Read from stdin")
@click.option("--format", "output_format", 
              type=click.Choice(["table", "jsonl", "csv"]), 
              default="table", show_default=True)
@click.option("--severity", default=None, help="Filter by severity eg HIGH,CRITICAL")
@click.option("--user", default=None, help="Filter by username")
@click.option("--ip", default=None, help="Filter by IP address")
@click.option("--suspicious-only", is_flag=True, help="Show only suspicious events")
@click.option("--summary", is_flag=True, help="Show summary report")
@click.option("--no-color", is_flag=True, help="Disable colored output")
def analyze(files, use_stdin, output_format, severity, user, ip, suspicious_only, summary, no_color):
    """Analyze and normalize log files."""
    console.print("[yellow]analyze command — not yet implemented[/yellow]")

@cli.command()
@click.argument("files", nargs="+")
def detect(files):
    """Detect the log type of a file."""
    console.print("[yellow]detect command — not yet implemented[/yellow]")

@cli.command()
@click.argument("file")
def sample(file):
    """Display annotated sample lines from a log file."""
    console.print("[yellow]sample command — not yet implemented[/yellow]")

@cli.command()
@click.argument("file")
@click.option("--line", type=int, required=True, help="Line number to explain")
def explain(file, line):
    """Explain a specific log line in plain English."""
    console.print("[yellow]explain command — not yet implemented[/yellow]")

if __name__ == "__main__":
    cli()
