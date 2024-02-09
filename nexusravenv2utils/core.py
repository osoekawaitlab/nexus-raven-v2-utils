from collections.abc import Sequence
from typing import Any, Optional, Type

from pydantic import BaseModel as PydanticBaseModel


class BaseError(Exception):
    pass


class ParseError(BaseError, ValueError):
    pass


class BaseModel(PydanticBaseModel): ...


class Output(BaseModel):
    call: str
    thought: str

    def __str__(self) -> str:
        """
        Return the string representation of the output.

        Returns:
            str: The string representation of the output.

        >>> print(str(Output(call="add(1, 1)", thought='The function call `add(1, 1)` answers the question "What is 1 plus 1?" by adding 1 and 1.')))
        Output(call='add(1, 1)', thought='The function call `add(1, 1)` answers the question "What is 1 plus 1?" by adding 1 and 1.')
        """  # noqa: E501
        return f"Output(call='{self.call}', thought='{self.thought}')"

    def __repr__(self) -> str:
        """
        Return the string representation of the output.

        Returns:
            str: The string representation of the output.

        >>> print(repr(Output(call="add(1, 1)", thought='The function call `add(1, 1)` answers the question "What is 1 plus 1?" by adding 1 and 1.')))
        Output(call='add(1, 1)', thought='The function call `add(1, 1)` answers the question "What is 1 plus 1?" by adding 1 and 1.')
        """  # noqa: E501
        return self.__str__()

    @classmethod
    def parse(cls, output: str) -> "Output":
        """
        Parse the output from LLM.

        Args:
            output (str): The output from LLM.

        Returns:
            Output: The parsed output.

        >>> Output.parse('Call: add (a=1, b=1) \\nThought: The function call `add (a=1, b=1) ` answers the question "What is 1 plus 1?" because it passes the values 1 and 1 to the `add` function, which adds them together and returns the result.\\n\\nThe `add` function takes two integer arguments, `a` and `b`, and returns their sum. In this case, the function is called with the values `a=1` and `b=1`, which means the function will return the sum of 1 and 1, which is 2.\\n\\nTherefore, the function call `add (a=1, b=1) ` answers the question "What is 1 plus 1?" by returning the value 2, which is the result of adding 1 and 1 together.')
        Output(call='add (a=1, b=1)', thought='The function call `add (a=1, b=1) ` answers the question "What is 1 plus 1?" because it passes the values 1 and 1 to the `add` function, which adds them together and returns the result.
        <BLANKLINE>
        The `add` function takes two integer arguments, `a` and `b`, and returns their sum. In this case, the function is called with the values `a=1` and `b=1`, which means the function will return the sum of 1 and 1, which is 2.
        <BLANKLINE>
        Therefore, the function call `add (a=1, b=1) ` answers the question "What is 1 plus 1?" by returning the value 2, which is the result of adding 1 and 1 together.')
        """  # noqa: E501
        chunks = output.split(chr(10))
        call = ""
        thought = ""
        call_end = False
        for chunk in chunks:
            if chunk.startswith("Thought: "):
                call_end = True
                thought += chunk[len("Thought: ") :]
            elif call_end:
                thought += f"\n{chunk}"
            elif chunk.startswith("Call: "):
                call += chunk[len("Call: ") :]
            else:
                call += f"\n{chunk}"
        if not call or not thought:
            raise ParseError(output)
        return cls(call=call.strip(), thought=thought)


class Argument(BaseModel):
    name: str
    type: Type[Any]
    description: str
    default: Optional[Any] = None

    def __str__(self) -> str:
        """
        Return the string representation of the argument.

        Returns:
            str: The string representation of the argument.

        >>> str(Argument(name="a", type=int, description="The first argument."))
        'a (int): The first argument.'
        >>> str(Argument(name="b", type=int, description="The second argument.", default=1))
        'b (:obj:`int`, optional): The second argument.'
        """
        if self.default is None:
            return f"{self.name} ({self.type.__name__}): {self.description}"
        else:
            return f"{self.name} (:obj:`{self.type.__name__}`, optional): {self.description}"

    @property
    def signature(self) -> str:
        """
        Return the signature of the argument.

        Returns:
            str: The signature of the argument.

        >>> Argument(name="a", type=int, description="The first argument.").signature
        'a: int'
        >>> Argument(name="b", type=int, description="The second argument.", default=1).signature
        'b: int = 1'
        """
        if self.default is None:
            return f"{self.name}: {self.type.__name__}"
        else:
            return f"{self.name}: {self.type.__name__} = {self.default}"


class Function(BaseModel):
    name: str
    description: str
    arguments: Sequence[Argument]
    return_type: Type[Any]
    return_description: str

    def __str__(self) -> str:
        """
        Return the string representation of the function.

        Returns:
            str: The string representation of the function.

        >>> print(str(Function(name="foo", description="The foo function.", arguments=[Argument(name="a", type=int, description="The first argument.")], return_type=str, return_description="The return value.")))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                str: The return value.
            \"\"\"
        <BLANKLINE>
        """  # noqa: E501
        return f"""\
Function:
def {self.name}({', '.join([argument.signature for argument in self.arguments])}) -> {self.return_description}:
    \"\"\"
    {self.description}

    Args:
        {chr(10).join([str(argument) for argument in self.arguments])}

    Returns:
        {self.return_type.__name__}: {self.return_description}
    \"\"\"
"""


class PromptTemplate(BaseModel):
    functions: Sequence[Function]

    def __str__(self) -> str:
        """
        Return the string representation of the prompt template.

        Returns:
            str: The string representation of the prompt template.

        >>> print(str(PromptTemplate(functions=[Function(name="foo", description="The foo function.", arguments=[Argument(name="a", type=int, description="The first argument.")], return_type=str, return_description="The return value.")])))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                str: The return value.
            \"\"\"
        <BLANKLINE>
        User Query: {user_query}
        """  # noqa: E501
        return f"""{chr(10).join([str(function) for function in self.functions])}
User Query: {{user_query}}"""

    def format(self, user_query: str) -> str:
        """
        Return the formatted string representation of the prompt template.

        Args:
            user_query (str): The user query.

        Returns:
            str: The formatted string representation of the prompt template.

        >>> print(PromptTemplate(functions=[Function(name="foo", description="The foo function.", arguments=[Argument(name="a", type=int, description="The first argument.")], return_type=str, return_description="The return value.")]).format("pass foo to a string 'bar'"))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                str: The return value.
            \"\"\"
        <BLANKLINE>
        User Query: pass foo to a string 'bar'
        """  # noqa: E501
        return self.__str__().format(user_query=user_query)

    def render(self, user_query: str) -> str:
        """
        Render the formatted string representation of the prompt template.

        Args:
            user_query (str): The user query.

        >>> print(PromptTemplate(functions=[Function(name="foo", description="The foo function.", arguments=[Argument(name="a", type=int, description="The first argument.")], return_type=str, return_description="The return value.")]).render("pass foo to a string 'bar'"))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                str: The return value.
            \"\"\"
        <BLANKLINE>
        User Query: pass foo to a string 'bar'<human_end>
        """  # noqa: E501
        return f"{self.format(user_query)}<human_end>"
