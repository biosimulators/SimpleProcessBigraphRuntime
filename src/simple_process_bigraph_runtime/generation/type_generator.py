import warnings

from process_bigraph_lang.dsl.model import Model, Type

with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes


def collect_types(model: Model) -> list[Type]:
    types_to_process: list[Type] = []
    for type in model.types:
        # Insert some parsing code here
        types_to_process.append(type)
    return types_to_process

def register_type(core: ProcessTypes, types_to_register: list[Type]):
    pass