from pathlib import Path

from process_bigraph_lang.dsl.model import Model

from simple_process_bigraph_runtime.main import generatePythonModel, performConversion


def test_add(model_path_abc: Path) -> None:
    ast_model: Model = generatePythonModel(model_path_abc)
    pb_composite, _0, _1 = performConversion(ast_model)

    duration = 10.0
    pb_composite.run(duration)
