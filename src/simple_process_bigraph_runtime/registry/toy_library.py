import os.path

from process_bigraph import Process, Step
from vivarium import Vivarium

complex_number = {
    "real" : "float",
    "imag" : "float",
}

TYPES_DICT = {
    "complex_number": complex_number,
}

class AddFloats(Step):
    def inputs(self):
        return {
            "left_hand_addend": "float",
            "right_hand_addend": "float"
        }

    def outputs(self):
        return {
            "result": "float"
        }

    def update(self, inputs):
        left_hand_addend: float = inputs["left_hand_addend"]
        right_hand_addend: float = inputs["right_hand_addend"]
        result = left_hand_addend + right_hand_addend
        return {
            "result": result
        }

class AddFloatsRepeatedly(Process):
    def inputs(self):
        return {
            "left_hand_addend": "float",
            "right_hand_addend": "float"
        }

    def outputs(self):
        return {
            "result": "float"
        }

    def update(self, inputs, interval):
        left_hand_addend: float = inputs["left_hand_addend"]
        right_hand_addend: float = inputs["right_hand_addend"]
        result = left_hand_addend + right_hand_addend
        return {
            "result": result
        }

class SaveFloatToFile(Step):

    def inputs(self):
        return {
            "result": "float",
        }

    def update(self, state):
        with open(os.path.expanduser(self.config["output_file_path"]), "w+") as f:
            f.write(str(state["result"]))

class SaveFloatToFileRepeatedly(Process):
    def inputs(self):
        return {
            "result": "float",
        }

    def update(self, state, interval):
        value = str(state["result"])
        with open(os.path.expanduser(self.config["output_file_path"]), "w+") as f:
            f.write(value)

class AddComplexNumbers(Step):
    def inputs(self):
        return {
            "left_hand_addend": "complex_number",
            "right_hand_addend": "complex_number"
        }

    def update(self, inputs):
        result = {}
        left_hand_addend: complex_number = inputs["left_hand_addend"]
        right_hand_addend: complex_number = inputs["right_hand_addend"]
        result["real"] = left_hand_addend["real"] + right_hand_addend["real"]
        result["imag"] = left_hand_addend["imag"] + right_hand_addend["imag"]


class GetRealFromComplexNumber(Step):
    pass

PROCESS_DICT = {
    "AddFloats" : AddFloats,
    "AddFloatsRepeatedly": AddFloatsRepeatedly,
    "SaveFloatToFile" : SaveFloatToFile,
    "SaveFloatToFileRepeatedly": SaveFloatToFileRepeatedly,
    "AddComplexNumbers" : AddComplexNumbers,
    "GetRealFromComplexNumber" : GetRealFromComplexNumber
}

def apply_to_vivarium(vivarium: Vivarium) -> None:
    for type_name, type_schema in TYPES_DICT.items():
        vivarium.core.register("toy.type." + type_name, type_schema)
    for process_name, process in PROCESS_DICT.items():
        vivarium.core.register_process("toy." + process_name, process)