import warnings
from vivarium import Vivarium
from process_bigraph_lang.dsl.model import Model
with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes, Process


def register_process_defs(assembler: Vivarium, model: Model) -> None:
    # note: does not actually dynamically build processes...yet
    registry = assembler.core
    for process_def in model.processDefs:
        if registry.process_registry.find(process_def.name) is not None:
            continue
        raise ValueError(f"Unknown process definition {process_def.name}")

