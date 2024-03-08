from pydantic import BaseModel

from nexusravenv2utils.core import Argument


class ArgumentTestCase(BaseModel):
    argument: Argument
    string: str
    signature: str
    comment: str


arguments = [
    ArgumentTestCase(
        argument=Argument(name="a"), string="a", signature="a", comment="no type no description no default"
    ),
    ArgumentTestCase(
        argument=Argument(name="a", type=int),
        string="a (int)",
        signature="a: int",
        comment="no description no default",
    ),
    ArgumentTestCase(
        argument=Argument(name="a", description="the description"),
        string="a: the description",
        signature="a",
        comment="no type no default",
    ),
    ArgumentTestCase(
        argument=Argument(name="a", default=1),
        string="a (optional)",
        signature="a = 1",
        comment="no type no description",
    ),
    ArgumentTestCase(
        argument=Argument(name="a", type=int, description="the description"),
        string="a (int): the description",
        signature="a: int",
        comment="no default",
    ),
]
