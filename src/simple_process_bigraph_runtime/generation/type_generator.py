from process_bigraph_lang.dsl.model import Type
from vivarium import Vivarium


def register_types(assembler: Vivarium, types_to_register: list[Type]):
    for type_to_register in types_to_register:
        if 0 == assembler.get_type(type_to_register.name).size:
            raise ValueError(f"Type {type_to_register.name} is an unknown type")
        # in the future, we'd attempt to generate a new type
