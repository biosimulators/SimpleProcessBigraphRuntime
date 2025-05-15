from pathlib import Path

from process_bigraph_lang.dsl.model import Model, ProcessDef
from vivarium import Vivarium  # type: ignore[import-untyped]

import simple_process_bigraph_runtime.registry.toy_library as toy
from simple_process_bigraph_runtime.generation.composite_generator import process_composite
from simple_process_bigraph_runtime.generation.process_generator import register_process_defs
from simple_process_bigraph_runtime.generation.type_generator import register_types
from simple_process_bigraph_runtime.generation.unit_generator import register_units
from simple_process_bigraph_runtime.main import generatePythonModel, performConversion


def test_add(model_path_abc: Path) -> None:
    ast_model: Model = generatePythonModel(model_path_abc)

    assembler = Vivarium()
    for type_name, type_schema in toy.TYPES_DICT.items():
        assembler.core.register("toy.type." + type_name, type_schema)
    for process_name, process in toy.PROCESS_DICT.items():
        assembler.core.register_process("toy." + process_name, process)
    register_process_defs(assembler, ast_model.processDefs)
    register_types(assembler, ast_model.types)
    register_units(assembler, ast_model.units)
    process_composite(ast_model, assembler)
    composite = assembler.composite

    duration = 10.0
    composite.run(duration)
    core = composite.core
    print(core)

    add_num: ProcessDef = ast_model.processDefs[0]
    assert add_num.python_path
    assert ".".join(add_num.python_path.path) == 'toy.AddFloatsRepeatedly'
    assert ".".join(add_num.python_path.path) in core.process_registry.registry

    print(core.process_registry.registry)

    print_results: ProcessDef = ast_model.processDefs[1]
    assert print_results.python_path
    assert ".".join(print_results.python_path.path) == 'toy.SaveFloatToFile'
    assert ".".join(print_results.python_path.path) in core.process_registry.registry
