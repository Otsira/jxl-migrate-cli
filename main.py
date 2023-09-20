import typer
from typing_extensions import Annotated
import os
from multiprocessing import cpu_count
from typing import Optional
from multiprocessing.pool import ThreadPool
from subprocess import check_output
import subprocess
import time
import tempfile

app = typer.Typer()


@app.command()
def main(
    input_dir: str,
    output_dir: Annotated[Optional[str], typer.Argument()] = None,
    lossless: bool = True,
    jobs: int = cpu_count(),
    remove: bool = False,
):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            print(os.path.join(root, filename))


def handle_file(filename, root):
    if not filename.endswith(("jpg", "jpeg", "gif", "png", "apng", "webp")):
        return None


def transcode(input_path, target_path, lossless, jobs, remove):
    proc = subprocess.run(
        "cjxl",
        input_path,
        target_path,
        "-d",
        "0" if lossless else "1",
        "-j",
        "1" if lossless else "0",
        capture_output=True,
    )
    if proc.returncode != 0 or not os.path.exists(target_path):
        return None
    else:
        os.utime(target_path, (time.time(), os.path.getmtime(input_path)))
        if remove:
            os.remove(input_path)
        return target_path


if __name__ == "__main__":
    app()
