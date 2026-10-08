import importlib

import pytest

MODULES = [
    "CommonFunctions", "Data", "DB", "InputKey", "Inventory", "Trophy",
    "GunFunctions", "KickEnemy", "SpecialEnemy",
    "Camp", "CampEvents", "CollectionBook",
    "CreateStone", "NagakuteEvents", "NagoyaEvents", "RandomEvents", "WithHorse", "WithMerchant",
    "FieldJunction", "NagakuteField", "NagoyaField",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)
