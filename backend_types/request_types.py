__author__ = 'ishwartz'

import endpoints
from protorpc import messages
from protorpc import message_types

ID_RESOURCE_SETTING = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1),
    play_list_size=messages.IntegerField(2),
    enable=messages.BooleanField(3),
    loc=messages.StringField(4))

ID_RESOURCE = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1),
)

ID_RESOURCE_S = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1))

ID_RESOURCE_P = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1),
    play_list_id=messages.StringField(2))

ID_RESOURCE_P_Test = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1),
    up=messages.IntegerField(2),
    down=messages.IntegerField(3))
