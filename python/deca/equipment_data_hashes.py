from deca.ff_rtpc import rtpc_from_binary, FieldNameMap
from deca.db_core import VfsDatabase
from pathlib import Path
import logging
import json

def open_file(filename: Path):
 with(filename.open("rb")) as f:
   data = rtpc_from_binary(f)
 f_bytes = bytearray(filename.read_bytes())
 return (data.root_node, f_bytes)

DECA_PATH = "C:\\Users\\Ryan\\Tools\\deca_gui-b595\\work\\hp"
PROJ = DECA_PATH + "\\project.json"
FILE = "extracted\\settings\\hp_settings\\equipment_data.bin"

logger = logging.getLogger(__name__)
vfs = VfsDatabase(PROJ, DECA_PATH, logger)
fnm = FieldNameMap(vfs)
root, data = open_file(Path(DECA_PATH + "\\" + FILE))

hashes = {}
print("Extracting name hashes...")
for equipment_type_node in root.child_table:
    equipment_type_name = fnm.lookup(hash32=equipment_type_node.name_hash)
    hashes[equipment_type_name] = {}
    for equipment_node in equipment_type_node.child_table:
        equipment_name = fnm.lookup(hash32=equipment_node.name_hash)
        display_name = ""
        for i in range(equipment_node.prop_count):
            raw_name = equipment_node.prop_table[i].data
            if type(raw_name) is bytes:
                display_name = raw_name.decode("utf-8")
                if display_name.startswith("equipment_") or display_name == "store_featured":
                    display_name = ""
                    continue
                break
        equipment_dict = {"name": equipment_name, "display_name": display_name}
        hashes[equipment_type_name][equipment_node.name_hash] = equipment_dict

total_hashes = len(hashes.items()) + sum(len(nested_hashes) for nested_hashes in hashes.values())
print(f"Successfully extracted {total_hashes} hashes.")

print("Writing JSON file...")
with open('equipment_data.json', 'w') as f:
    json.dump(hashes, f, indent=4)
