import warnings
from typing import Any
from process_bigraph_lang.dsl.model import Model, Store
from vivarium import Vivarium

with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes


def collect_stores(model: Model) -> tuple[list[Store], Any]:
    pass

def register_stores(assembler: Vivarium, stores_to_register: list[Store]) -> None:
    pass