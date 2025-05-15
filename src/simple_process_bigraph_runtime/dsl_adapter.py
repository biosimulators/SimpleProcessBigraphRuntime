import os

from process_bigraph_lang.antlr_dsl.generate import bind_model
from process_bigraph_lang.dsl import generate
from process_bigraph_lang.dsl.model import (
    Model,
)


def generateModelAst(pblang_file: os.PathLike[str]) -> Model:
    model_json: str = generate.generate_model(pblang_file)
    model: Model = Model.model_validate_json(model_json)
    bind_model(model)
    #result: str = model.model_dump_json(indent=4)
    #rich.print(result)
    return model