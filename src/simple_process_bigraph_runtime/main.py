import sys
import os
import warnings

import typer
from process_bigraph_lang.dsl.model import Model
from typing_extensions import Annotated
with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes
from simple_process_bigraph_runtime import dsl_adapter
from spatio_flux import processes

app = typer.Typer()


core = ProcessTypes()

@app.command()
def validate(pblang_path: Annotated[str, typer.Argument(help="Path to the pblang file to validate")]):
    generatePythonModel(pblang_path)

@app.command()
def execute(pblang_path: Annotated[str, typer.Argument(help="Path to the pblang file to validate")]):
    generatePythonModel(pblang_path)

def generatePythonModel(pblang_path: os.PathLike[str]) -> Model:
    absolute_path: str = os.path.abspath(pblang_path)
    if not os.path.exists(absolute_path):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: no file with that name exists.\n")
        exit(1)
    if os.path.isdir(absolute_path):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: file is a directory, not a script.\n")
        exit(1)
    if not absolute_path.endswith(".pblang"):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: file is labeled with an unexpected extension.\n")
        exit(1)

    return dsl_adapter.generateModelAst(pblang_path)

def performConversion(ast_model: Model) -> tuple[str, ProcessTypes]:
    pass

if __name__ == "__main__":
    app()

