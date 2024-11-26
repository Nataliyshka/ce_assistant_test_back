from enum import Enum
from client.assistent import AssistantClient
from session import RoleUser


def test_create_cart():
    client = AssistantClient(RoleUser.ADMIN) 
    client.store_get_by_location(coordinates=)