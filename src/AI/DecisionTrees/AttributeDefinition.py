from typing import List


class AttributeDefinition:
    def __init__(self, id, name: str, values: List):
        """

        :param id:
        :param name: Attribute name
        :param values: Possible values
        """
        self.id = id
        self.name = name
        self.values = values
