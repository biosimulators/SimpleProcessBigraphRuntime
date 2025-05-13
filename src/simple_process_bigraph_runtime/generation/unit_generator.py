import warnings

from process_bigraph_lang.dsl.model import Model, Unit
from vivarium import Vivarium
with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes


def collect_units(model: Model) -> list[Unit]:
    units_to_process: list[Unit] = []
    for unit in model.units:
        # Insert some parsing code here
        units_to_process.append(unit)
    return units_to_process

def register_units(assembler: Vivarium, units_to_register: list[Unit]) -> None:
    pass
