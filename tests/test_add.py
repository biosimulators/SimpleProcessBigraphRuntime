import tempfile
from pathlib import Path

from process_bigraph_lang.dsl.model import Model, ProcessDef
from vivarium import Vivarium  # type: ignore[import-untyped]

import simple_process_bigraph_runtime.registry.toy_library as toy
from simple_process_bigraph_runtime.environment.process_bigraph_env import ProcessBigraphEnv
from simple_process_bigraph_runtime.generation.composite_generator import process_composite
from simple_process_bigraph_runtime.generation.process_generator import register_process_defs
from simple_process_bigraph_runtime.generation.type_generator import register_types
from simple_process_bigraph_runtime.generation.unit_generator import register_units
from simple_process_bigraph_runtime.main import generatePythonModel, performConversion


def test_add_with_process(model_path_abc: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        # parse DSL
        ast_model: Model = generatePythonModel(model_path_abc)

        # specify the python path for the processes
        add_num = ast_model.processDefs[0]
        add_num.python_path.path = ['toy', 'AddFloatsProcess']
        print_results = ast_model.processDefs[1]
        print_results.python_path.path = ['toy', 'SaveFloatToFileStep']

        # set the output file path
        output_file_path = Path(tmp_dirname) / "output.txt"
        print_results.params[0].default.val = str(output_file_path)

        assembler = ProcessBigraphEnv()

        # register the built-in processes and types
        toy.register(assembler)
        assert 'toy.AddFloatsProcess' in assembler.core.process_registry.registry
        assert 'toy.SaveFloatToFileStep' in assembler.core.process_registry.registry

        # register the processes, types, and units from the model
        register_process_defs(assembler, ast_model.processDefs)
        register_types(assembler, ast_model.types)
        register_units(assembler, ast_model.units)
        process_composite(ast_model, assembler)

        # run the process
        duration = 10.0
        assembler.run(duration)

        # Check the output file, its contents should be 55.7
        with open(output_file_path, 'r') as f:
            contents = f.read()
            assert contents.strip() == "55.7"


def test_add_with_step(model_path_abc: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        # parse DSL
        ast_model: Model = generatePythonModel(model_path_abc)

        # specify the python path for the processes
        add_num = ast_model.processDefs[0]
        add_num.python_path.path = ['toy', 'AddFloatsStep']
        print_results = ast_model.processDefs[1]
        print_results.python_path.path = ['toy', 'SaveFloatToFileStep']

        # set the output file path
        output_file_path = Path(tmp_dirname) / "output.txt"
        print_results.params[0].default.val = str(output_file_path)

        assembler = ProcessBigraphEnv()

        # register the built-in processes and types
        toy.register(assembler)
        assert 'toy.AddFloatsStep' in assembler.core.process_registry.registry
        assert 'toy.SaveFloatToFileStep' in assembler.core.process_registry.registry

        # register the processes, types, and units from the model
        register_process_defs(assembler, ast_model.processDefs)
        register_types(assembler, ast_model.types)
        register_units(assembler, ast_model.units)
        process_composite(ast_model, assembler)

        print(assembler.core.process_registry.registry)

        # run the process
        assembler.run(10.0)
        assembler.step()

        # Check the output file, its contents should be 5.57 (only executed once)
        with open(output_file_path, 'r') as f:
            contents = f.read()
            assert contents.strip() == "5.57"
