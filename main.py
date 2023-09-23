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
    inputdir: str,
    outputdir: Annotated[Optional[str], typer.Argument()] = None,
    lossless: bool = True,
    jobs: int = cpu_count(),
    remove: bool = False,
):
    if not outputdir:
        outputdir = inputdir
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for root, _, files in os.walk(inputdir):
        subfolder = os.path.relpath(root, inputdir)
        if subfolder != "." and not os.path.exists(os.path.join(outputdir, subfolder)):
            os.makedirs(os.path.join(outputdir, subfolder))
        if subfolder != ".":
            targetdir = os.path.join(outputdir, subfolder)
        else:
            targetdir = outputdir
        for filename in files:
            handle_file(filename, root, targetdir, lossless, remove)


def handle_file(filename, inputdir, outputdir, lossless=True, remove=False):
    if not filename.endswith(("jpg", "jpeg", "gif", "png", "apng")):
        return None
    bare_filename = os.path.splitext(filename)[0]
    input_path = os.path.join(inputdir, filename)
    output_path = os.path.join(outputdir, bare_filename + ".jxl")
    if os.path.exists(output_path):
        return None
    transcode(input_path, output_path, lossless, remove)


def transcode(input_path, target_path, lossless, remove):
    proc = subprocess.run(
        args=[
            "cjxl",
            input_path,
            target_path,
            "-d",
            "0" if lossless else "1",
            "-j",
            "1" if lossless else "0",
        ],
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
