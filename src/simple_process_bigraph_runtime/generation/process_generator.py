from process_bigraph_lang.dsl.model import ProcessDef
from vivarium import Vivarium  # type: ignore[import-untyped]
from vivarium.vivarium import VivariumTypes  # type: ignore[import-untyped]


def register_process_defs(assembler: Vivarium, process_defs: list[ProcessDef]) -> None:
    # note: does not actually dynamically build processes...yet
    registry: VivariumTypes = assembler.core
    for process_def in process_defs:
        if not process_def.python_path:
            raise ValueError(f"Process definition {process_def.name} has no python path")
        python_path = ".".join(process_def.python_path.path)
        if not registry.process_registry.find(python_path):
            raise ValueError(f"Unknown process definition {process_def.name}")

