import sys
import os
import warnings

import typer
from process_bigraph_lang.dsl.model import Model
from typing_extensions import Annotated

from simple_process_bigraph_runtime.generation.process_generator import register_process_defs

with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes
from simple_process_bigraph_runtime import dsl_adapter
from vivarium import Vivarium
from process_bigraph import Composite

from simple_process_bigraph_runtime.generation.type_generator import register_types
from simple_process_bigraph_runtime.generation.unit_generator import register_units
from simple_process_bigraph_runtime.generation.composite_generator import process_composite
import simple_process_bigraph_runtime.registry.spatio_flux_library as spatioflux
import simple_process_bigraph_runtime.registry.toy_library as toy
from bigraph_viz import plot_bigraph

plot_settings = {
    'remove_process_place_edges': True
}
save_images = True
if save_images:
    plot_settings.update({
        'out_dir': '/Users/logandrescher/Documents/pb_output_dir',
        'dpi': '70'
    })

app = typer.Typer()

@app.command()
def validate(pblang_path: Annotated[str, typer.Argument(help="Path to the pblang file to validate")]):
    ast_model: Model = generatePythonModel(pblang_path)
    _, pb_doc, pb_core = performConversion(ast_model)
    plot_bigraph(state=pb_doc['state'], schema=pb_doc['composition'],
                 core=pb_core,
                 show_values=True,
                 out_dir=os.path.expanduser("~/Documents/pb_output_dir"),
                 filename='final_diagram',
                 dpi='140')

@app.command()
def execute(duration: float, pblang_path: Annotated[str, typer.Argument(help="Path to the pblang file to validate")]):
    ast_model: Model = generatePythonModel(pblang_path)
    pb_composite, _0, _1 = performConversion(ast_model)

    pb_composite.run(duration)
    print("Execution complete")

@app.command()
def playground():
    pass

def generatePythonModel(pblang_path: os.PathLike[str]) -> Model:
    absolute_path: str = validate_pb_absolute_path(os.path.abspath(pblang_path))

    return dsl_adapter.generateModelAst(pblang_path)

def validate_pb_absolute_path(absolute_path: str) -> str:
    if not os.path.exists(absolute_path):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: no file with that name exists.\n")
        exit(1)
    if os.path.isdir(absolute_path):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: file is a directory, not a script.\n")
        exit(1)
    if not absolute_path.endswith(".pblang"):
        sys.stderr.write(f"Error finding pblang file ({absolute_path}):: file is labeled with an unexpected extension.\n")
        exit(1)
    return absolute_path

def performConversion(ast_model: Model) -> tuple[Composite, dict, ProcessTypes]:
    assembler = Vivarium()
    spatioflux.apply_to_vivarium(assembler)
    toy.apply_to_vivarium(assembler)
    register_types(assembler, ast_model.types)
    register_units(assembler, ast_model.units)
    register_process_defs(assembler, ast_model.processDefs)
    process_composite(ast_model, assembler)

    return assembler.composite, assembler.make_document(), assembler.core

if __name__ == "__main__":
    app()

