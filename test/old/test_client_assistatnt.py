from enum import Enum
from client.assistent import AssistantClient
from session import RoleUser


def test_create_cart():
    client = AssistantClient(RoleUser.ADMIN) 
    client.item_get_by_barcode('65416849846514')