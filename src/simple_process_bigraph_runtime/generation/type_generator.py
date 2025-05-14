import warnings

from process_bigraph_lang.dsl.model import Model, Type
from vivarium import Vivarium

with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes

def collect_types(model: Model) -> list[Type]:
    types_to_process: list[Type] = []
    for type_to_add in model.types:
        # Insert some parsing code here
        types_to_process.append(type_to_add)
    return types_to_process


def register_types(assembler: Vivarium, types_to_register: list[Type]):
    for type_to_register in types_to_register:
        if 0 == assembler.get_type(type_to_register.name).size:
            raise ValueError(f"Type {type_to_register.name} is an unknown type")
        # in the future, we'd attempt to generate a new type
