import tempfile
from pathlib import Path

from process_bigraph_lang.antlr_dsl.generate import bind_model
from process_bigraph_lang.dsl.model import Model

from simple_process_bigraph_runtime.main import generatePythonModel


def test_parse_abc_with_process(model_paths_abc_processes: tuple[Path, Path]) -> None:
    pblang_path = model_paths_abc_processes[0]
    json_path = model_paths_abc_processes[1]

    # create the AST Model by parsing the pblang DSL
    parsed_ast_model: Model = generatePythonModel(pblang_path)

    # read JSON from DSL in second argument of tuple
    with open(json_path, 'r') as file:
        model_json = file.read()

    loaded_ast_model: Model = Model.model_validate_json(model_json)
    bind_model(loaded_ast_model)

    assert loaded_ast_model == parsed_ast_model


def test_parse_add_with_steps(model_paths_abc_steps: tuple[Path, Path]) -> None:
    pblang_path = model_paths_abc_steps[0]
    json_path = model_paths_abc_steps[1]

    # create the AST Model by parsing the pblang DSL
    parsed_ast_model: Model = generatePythonModel(pblang_path)

    # read JSON from DSL in second argument of tuple
    with open(json_path, 'r') as file:
        model_json = file.read()

    loaded_ast_model: Model = Model.model_validate_json(model_json)
    bind_model(loaded_ast_model)

    assert loaded_ast_model == parsed_ast_model
