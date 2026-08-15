import typer
from rich.console import Console
from atlas.core.constants import APP_NAME, VERSION
from atlas.core.status import STATUS_STYLE, STATUS_OK
from atlas.core.atlas import Atlas

console = Console()

app = typer.Typer(help="Atlas Mechanical Compiler")


def status(label: str, value: str):
    style = STATUS_STYLE[value]

    console.print(f"{label:.<20} [{style['color']}]{value} {style['icon']}[/{style['color']}]")


@app.command()
def doctor():
    """Check the Atlas environment."""

    console.print(f"[bold cyan]{APP_NAME}[/bold cyan] Compiler")
    typer.echo("----------------")
    status("Python ", STATUS_OK)
    status("Environment ", STATUS_OK)
    typer.echo("Plugins ........... 0")
    typer.echo("Exporters ......... 0")
    typer.echo("Machine ........... None")
    typer.echo()
    typer.echo(f"{APP_NAME} is ready.")


@app.command()
def version():
    """Show version."""

    typer.echo(f"{APP_NAME} {VERSION}")


@app.command()
def compile():
    """Compile and creates the modules."""
    atlas = Atlas()
    atlas.compile()
