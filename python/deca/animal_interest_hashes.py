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
FILE = "extracted\\settings\\hp_settings\\animal_interest.bin"

logger = logging.getLogger(__name__)
vfs = VfsDatabase(PROJ, DECA_PATH, logger)
fnm = FieldNameMap(vfs)
root, data = open_file(Path(DECA_PATH + "\\" + FILE))

hashes = {}
print("Extracting name hashes...")
for node in root.child_table:
    hashes[node.name_hash] = fnm.lookup(hash32=node.name_hash)
print(f"Successfully extracted {len(hashes)} hashes.")

print("Writing JSON file...")
with open('animal_interest.json', 'w') as f:
    json.dump({"equipment_name_hash": hashes}, f, indent=4)
print("Successfully wrote to 'animal_interest.jaon'")
