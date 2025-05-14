import warnings
import re
from typing import Any

from vivarium import Vivarium
from process_bigraph_lang.dsl.model import Model, StoreDef, ProcessDef, Reference

def process_composite(model: Model, assembler: Vivarium):
    for composite_def in model.compositeDefs:
        store_to_store_def_map: dict[str, StoreDef] = {}
        for store_ref in composite_def.stores:
            # verify we have a reference for desired process
            match_obj = re.match("^#(/(\w+)(@(\d+))+)+$", store_ref.store_def.ref)
            if not match_obj:
                raise ValueError(
                    f"Unexpected reference for process reference: `{store_ref.store_def.ref_text}` ({store_ref.store_def.ref})")
            full, section, _, index = match_obj.groups()
            if section != "store_defs":
                raise ValueError(f"Unexpected section `{section}` for reference `{store_ref.store_def.ref_text}` ({full})`")
            store_to_store_def_map[composite_def.name + "::" + store_ref.name] = model.store_defs[int(index)]

        store_value_mapping: dict[str, Any] = {}
        for process in composite_def.processes:
            # verify we have a reference for desired process
            match_obj = re.match("^#(/(\w+)(@(\d+))+)+$", process.process_def.ref)
            if not match_obj:
                raise ValueError(f"Unexpected reference for process reference: `{process.process_def.ref_text}` ({process.process_def.ref})")
            full, section, _, index = match_obj.groups()
            if section != "processDefs":
                raise ValueError(f"Unexpected section `{section}` for reference `{process.process_def.ref_text}` ({full})`")

            # Identify ports needing to be bound
            process_def_actual: ProcessDef = model.processDefs[int(index)]
            input_bindings: dict[str, list[str]] = {elem.ref_text : [] for elem in process_def_actual.inputs}
            output_bindings: dict[str, list[str]] = {elem.ref_text : [] for elem in process_def_actual.outputs}

            # create config
            # config = {}
            # for param in process_def_actual.params:
            #     config[param.name] = param.default.val if param.default is not None else determine_builtin_default(param.type.ref_text)

            # store validation
            store_ref: Reference
            for store_ref in process.stores:
                match_obj = re.match("^#(/[\w]+(@\d)+)+$", store_ref.ref)
                if not match_obj:
                    raise ValueError(f"Unexpected reference for process reference: `{store_ref.ref_text}` ({store_ref.ref})")
                tokenized_reference_path: list[tuple[str, int]] = [(elem.split("@")[0], int(elem.split("@")[1])) for elem in store_ref.ref[1:].split("/") if '@' in elem]
                map_key: str = composite_def.name + "::" + store_ref.ref_text
                if map_key not in store_to_store_def_map:
                    raise ValueError(f"Store {store_ref} not found in mapping using key `{map_key}`")
                actual_def = store_to_store_def_map[map_key]
                for state_def in actual_def.states:
                    in_path = input_bindings[state_def.name] if state_def.name in input_bindings else []
                    out_binding = output_bindings[state_def.name] if state_def.name in output_bindings else []
                    if 0 != len(in_path and 0 != len(out_binding)):
                        continue
                    if 0 == len(in_path) and 0 == len(out_binding): #nothing has been initialized with this store
                        store_value_mapping[map_key] = state_def.default.val if state_def.default is not None else determine_builtin_default(state_def.type.ref_text)
                    if 0 == len(in_path):
                        for token in map_key.split("::"):
                            in_path.append(token)
                    if 0 == len(out_binding):
                        for token in map_key.split("::"):
                            out_binding.append(token)
            config = {p.name: p.default.val for p in process_def_actual.params}
            assembler.add_process(
                name=process.name,
                process_id=".".join(process_def_actual.python_path.path),
                config=config,
                inputs=input_bindings,
                outputs=output_bindings,
            )
        # end scope of composite def for loop
        for path_str in store_value_mapping:
            path = path_str.split("::")
            assembler.set_value(path=path, value=store_value_mapping[path_str])
    assembler.add_emitter()

def determine_builtin_default(type_to_infer: str):
    if type_to_infer == "float":
        return 0.0
    elif type_to_infer == "int":
        return 0
    else:
        raise ValueError(f"Unknown built-in default for type `{type_to_infer}`")