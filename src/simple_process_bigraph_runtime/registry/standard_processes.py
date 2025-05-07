from typing import Any
from process_bigraph import Process, Composite, ProcessTypes, pp

class StateData(dict):
    def __new__(cls, *args, **kwargs):
        return super(StateData, cls).__new__(cls, *args, **kwargs)

class PortSchema(dict):
    def __new__(cls, *args, **kwargs):
        return super(PortSchema, cls).__new__(cls, *args, **kwargs)


class InputPortSchema(PortSchema):
    pass


class OutputPortSchema(PortSchema):
    pass

class Toy(Process):
    config_schema = {
        'k': 'float'
    }
    def __init__(self, config: dict[str, Any] = None, core: ProcessTypes = None) -> None:
        super().__init__(config, core)
        self.k = self.config['k']

    def initial_state(self) -> StateData:
        return StateData(
            x=self.k,
            y=self.k**self.k
        )

    def inputs(self) -> InputPortSchema:
        return InputPortSchema(
            x='float'
        )

    def outputs(self) -> OutputPortSchema:
        return OutputPortSchema(
            x='float',
            y='float'
        )

    def update(self, state, interval) -> StateData:
        x = state['x'] * self.k
        return StateData({
            'x': x,
            'y': x**x
        })