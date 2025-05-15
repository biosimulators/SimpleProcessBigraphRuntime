from process_bigraph_lang.dsl.model import Unit
from vivarium import Vivarium

def register_units(assembler: Vivarium, units_to_register: list[Unit]) -> None:
    for unit_to_register in units_to_register:
        pass
        # if 0 == assembler.get_type(unit_to_register.name).size:
        #     raise ValueError(f"Type {unit_to_register.name} is an unknown type")
        # in the future, we'd attempt to generate a new type

