import typer
import uvicorn

app = typer.Typer(
    help="cli tool stuff thing",
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
)


@app.command(help="Serve the main uvicorn application")
def runserver(prod: bool = typer.Option(
    False, help="Use production server with workers")):
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=not prod)


@app.command()
def makemigrations(name: str):
    print('Hello', name)


if __name__ == '__main__':
    app()
