import warnings

from process_bigraph_lang.dsl.model import Model

with warnings.catch_warnings(): # Temporary minimal_impact bug in process_bigraphs
    warnings.simplefilter("ignore", SyntaxWarning)
    #warnings.filterwarnings("error", category=SyntaxWarning)
    from process_bigraph import ProcessTypes


def collect_stores(model: Model):
    pass

def register_stores(core: ProcessTypes) -> None:
    pass