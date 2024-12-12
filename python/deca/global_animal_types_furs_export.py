from deca.ff_rtpc import rtpc_from_binary, FieldNameMap, RtpcNode
from deca.db_core import VfsDatabase
from pathlib import Path
import copy
import logging
import json


def open_file(filename: Path):
    with(filename.open("rb")) as f:
        data = rtpc_from_binary(f)
    f_bytes = bytearray(filename.read_bytes())
    return (data.root_node, f_bytes)


def get_value_for_property(node: RtpcNode, name: str, data_type="utf-8"):
    for prop in node.prop_table:
        prop_name = fnm.lookup(hash32=prop.name_hash)
        if prop_name == name:
            return prop.data.decode(data_type)


class Animal:
    __slots__ = ("name", "furs")

    name: str
    furs: dict

    def __init__(self, animal_node: RtpcNode) -> None:
        self.name = get_value_for_property(animal_node, "name")
        furs_list = self._get_furs(animal_node)
        self.furs = furs_list
        #self.furs = self._merge_furs(furs_list)
        #self._calculate_fur_probabilities()

    def _get_visual_variations_table(self, animal_node: RtpcNode) -> RtpcNode:
        for table in animal_node.child_table:
            table_name = get_value_for_property(table, "_class")
            if table_name == "CAnimalTypeVisualVariationSettings":
                return table

    def _get_furs(self, animal_node: RtpcNode) -> None:
        furs_list = []
        visual_variations_table = self._get_visual_variations_table(animal_node)
        for variant_node in visual_variations_table.child_table:
            fur = Fur(variant_node)
            furs_list.append(fur)
        return furs_list

    def _merge_furs(self, furs_list):
        merged_furs = {}
        merged_furs["male"] = [fur for fur in furs_list if fur.gender == "male" and not fur.great_one]
        merged_furs["female"] = [fur for fur in furs_list if fur.gender == "female" and not fur.great_one]
        for fur in [fur for fur in furs_list if fur.gender == "both"]:
            male_fur = copy.deepcopy(fur)
            male_fur.gender = "male"
            merged_furs["male"].append(male_fur)
            female_fur = copy.deepcopy(fur)
            female_fur.gender = "female"
            merged_furs["female"].append(female_fur)
        merged_furs["great_one"] = [fur for fur in furs_list if fur.great_one]
        return merged_furs

    def _calculate_fur_probabilities(self, rount_decimals: int=None):
        male_weight = sum(fur.weight for fur in self.furs["male"])
        for fur in self.furs["male"]:
            fur.probability = fur.weight / male_weight * 100
            if rount_decimals:
                fur.probability = round(fur.probability, rount_decimals)
        self.furs["male"].sort(key=lambda f: f.probability, reverse=True)

        female_weight = sum(fur.weight for fur in self.furs["female"])
        for fur in self.furs["female"]:
            fur.probability = fur.weight / female_weight * 100
            if rount_decimals:
                fur.probability = round(fur.probability, rount_decimals)
        self.furs["female"].sort(key=lambda f: f.probability, reverse=True)

        great_one_weight = sum(fur.weight for fur in self.furs["great_one"])
        for fur in self.furs["great_one"]:
            fur.probability = fur.weight / great_one_weight * 100
            if rount_decimals:
                fur.probability = round(fur.probability, rount_decimals)
        self.furs["great_one"].sort(key=lambda f: f.probability, reverse=True)

    def furs_to_json(self) -> dict:
        data = [fur.to_json() for fur in self.furs]
        return data

    def fur_probability_to_json(self) -> dict:
        data = {
            "male": {fur.name: fur.probability for fur in self.furs["male"]},
            "female": {fur.name: fur.probability for fur in self.furs["female"]},
        }
        if self.furs["great_one"]:
            data["great_one"] = {fur.name: fur.probability for fur in self.furs["great_one"]}
        return data
    
    def fur_ids_to_json(self) -> dict:
        data = {
            "male": {fur.name: fur.id for fur in self.furs["male"]},
            "female": {fur.name: fur.id for fur in self.furs["female"]},
        }
        if self.furs["great_one"]:
            data["great_one"] = {fur.name: fur.id for fur in self.furs["great_one"]}
        return data
    
    # def furs_to_json(self) -> dict:
    #     data = {
    #         "male": {fur.name: fur.id for fur in self.furs["male"]},
    #         "female": {fur.name: fur.id for fur in self.furs["female"]},
    #     }
    #     if self.furs["great_one"]:
    #         data["great_one"] = {fur.name: fur.id for fur in self.furs["great_one"]}
    #     return data

class Fur:
    __slots__ = ("name", "id", "great_one", "gender", "weight", "rarity", "probability")

    name: str
    id: str
    great_one: bool
    gender: str
    weight: int
    rarity: int
    probability: float

    def __init__(self, variant_node: RtpcNode) -> None:
        self.great_one = False
        self._get_name(variant_node)
        self._get_id(variant_node)
        self._get_gender(variant_node)
        self._get_weight(variant_node)
        self._get_rarity(variant_node)

    def _get_name(self, variant_node) -> None:
        for prop in reversed(variant_node.prop_table):
            value = prop.data
            if isinstance(value, bytes):
                value = prop.data.decode("utf-8")
            if isinstance(value, str):
                if value.startswith("animal_visual_variation_"):
                    self.name = value.replace("animal_visual_variation_","")
                    break
        if "great_one" in self.name:
            self.great_one = True

    def _get_id(self, variant_node: RtpcNode) -> None:
        for prop in variant_node.prop_table:
            prop_name = fnm.lookup(hash32=prop.name_hash)
            if prop_name == "_object_id":
                self.id = prop.data
                print(f"{self.id} : {self.name}")
                break

    def _get_gender(self, variant_node: RtpcNode) -> None:
        for prop in variant_node.prop_table:
            prop_name = fnm.lookup(hash32=prop.name_hash)
            if prop_name == "gender":
                gender = prop.data
                break
        if gender == 0:
            self.gender = "shared"
        if gender == 1:
            self.gender = "male"
        if gender == 2:
            self.gender = "female"

    def _get_weight(self, variant_node: RtpcNode) -> None:
        if type(variant_node.prop_table[-3].data) == int:
            i = -3
        else:
            i = -4
        print(f"weight_name = {variant_node.prop_table[i]}")
        # print(f"weight_lookup = {fnm.lookup(hash32=variant_node.prop_table[i].name_hash)}")
        self.weight = variant_node.prop_table[i].data

    def _get_rarity(self, variant_node: RtpcNode) -> None:
        rarity_lookup = {
            0: "common",
            1: "uncommon",
            2: "rare",
            3: "very_rare"
        }
        if type(variant_node.prop_table[6].data) == int:
            i = 6
        else:
            i = 7
        print(f"rarity_name = {variant_node.prop_table[i]}")
        # print(f"rarity_lookup = {fnm.lookup(hash32=variant_node.prop_table[i].name_hash)}")
        rarity = variant_node.prop_table[i].data
        self.rarity = rarity_lookup[rarity]

    def to_json(self):
        data = {
            "name": self.name,
            "id": self.id,
            "great_one": self.great_one,
            "gender": self.gender,
            "weight": self.weight,
            "rarity": self.rarity,
        }
        return data


DECA_PATH = "C:\\Users\\Ryan\\Tools\\deca_gui-b595\\work\\hp"
PROJ = DECA_PATH + "\\project.json"
FILE = "extracted\\global\\global_animal_types.blo"

logger = logging.getLogger(__name__)
vfs = VfsDatabase(PROJ, DECA_PATH, logger)
fnm = FieldNameMap(vfs)
root, data = open_file(Path(DECA_PATH + "\\" + FILE))

print("Parsing animal data from global_animal_types.blo...")
animals = []
animal_types_list = root.child_table[0].child_table
for animal_node in animal_types_list:
    animal = Animal(animal_node)
    animals.append(animal)
animals.sort(key=lambda animal: animal.name)

# total_hashes = len(hashes.items()) + sum(len(nested_hashes) for nested_hashes in hashes.values())
print(f"Successfully parsed {len(animals)} animals")
print("Writing to JSON file...")

animal_data = {animal.name: animal.furs_to_json() for animal in animals}
with open('animal_furs.json' , 'w') as f:
    json.dump(animal_data, f, indent=4)

# Fur Probabilities
# animal_data = {animal.name: animal.fur_probability_to_json() for animal in animals}
# with open('animal_fur_probabilities.txt' , 'w') as f:
#     json.dump(animal_data, f, indent=4)

# Fur Object IDs
# animal_data = {animal.name: animal.fur_ids_to_json() for animal in animals}
# with open('animal_fur_ids.json' , 'w') as f:
#     json.dump(animal_data, f, indent=4)
