import typer
from typing_extensions import Annotated
import os

app = typer.Typer()


@app.command()
def main(input_dir: str):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            print(os.path.join(root, filename))

    pass


if __name__ == "__main__":
    app()
