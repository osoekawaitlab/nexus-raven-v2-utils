from collections.abc import Sequence
from typing import Any, Type


class Argument:
    def __init__(self, name: str, type: Type[Any], description: str, default: Any = None) -> None:
        self._name = name
        self._type = type
        self._description = description
        self._default = default

    def __str__(self) -> str:
        """
        Return the string representation of the argument.

        Returns:
            str: The string representation of the argument.

        >>> str(Argument("a", int, "The first argument."))
        'a (int): The first argument.'
        >>> str(Argument("b", int, "The second argument.", 1))
        'b (:obj:`int`, optional): The second argument.'
        """
        if self._default is None:
            return f"{self._name} ({self._type.__name__}): {self._description}"
        else:
            return f"{self._name} (:obj:`{self._type.__name__}`, optional): {self._description}"

    @property
    def signature(self) -> str:
        """
        Return the signature of the argument.

        Returns:
            str: The signature of the argument.

        >>> Argument("a", int, "The first argument.").signature
        'a: int'
        >>> Argument("b", int, "The second argument.", 1).signature
        'b: int = 1'
        """
        if self._default is None:
            return f"{self._name}: {self._type.__name__}"
        else:
            return f"{self._name}: {self._type.__name__} = {self._default}"


class Function:
    def __init__(
        self,
        name: str,
        description: str,
        arguments: Sequence[Argument],
        return_type: Type[Any],
        return_description: str,
    ) -> None:
        self._name = name
        self._description = description
        self._arguments = arguments
        self._return_type = return_type
        self._return_description = return_description

    def __str__(self) -> str:
        """
        Return the string representation of the function.

        Returns:
            str: The string representation of the function.

        >>> print(str(Function("foo", "The foo function.", [Argument("a", int, "The first argument.")], str, "The return value.")))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                self._return_type: The return value.
            \"\"\"
        <BLANKLINE>
        """  # noqa: E501
        return f"""\
Function:
def {self._name}({', '.join([argument.signature for argument in self._arguments])}) -> {self._return_description}:
    \"\"\"
    {self._description}

    Args:
        {chr(10).join([str(argument) for argument in self._arguments])}

    Returns:
        self._return_type: {self._return_description}
    \"\"\"
"""


class PromptTemplate:
    def __init__(self, functions: Sequence[Function]) -> None:
        self._functions = functions

    def __str__(self) -> str:
        """
        Return the string representation of the prompt template.

        Returns:
            str: The string representation of the prompt template.

        >>> print(str(PromptTemplate([Function("foo", "The foo function.", [Argument("a", int, "The first argument.")], str, "The return value.")])))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                self._return_type: The return value.
            \"\"\"
        <BLANKLINE>
        User Query: {user_query}
        """  # noqa: E501
        return f"""{chr(10).join([str(function) for function in self._functions])}
User Query: {{user_query}}"""

    def format(self, user_query: str) -> str:
        """
        Return the formatted string representation of the prompt template.

        Args:
            user_query (str): The user query.

        Returns:
            str: The formatted string representation of the prompt template.

        >>> print(PromptTemplate([Function("foo", "The foo function.", [Argument("a", int, "The first argument.")], str, "The return value.")]).format("pass foo to a string 'bar'"))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                self._return_type: The return value.
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

        >>> print(PromptTemplate([Function("foo", "The foo function.", [Argument("a", int, "The first argument.")], str, "The return value.")]).render("pass foo to a string 'bar'"))
        Function:
        def foo(a: int) -> The return value.:
            \"\"\"
            The foo function.
        <BLANKLINE>
            Args:
                a (int): The first argument.
        <BLANKLINE>
            Returns:
                self._return_type: The return value.
            \"\"\"
        <BLANKLINE>
        User Query: pass foo to a string 'bar'<human_end>
        """  # noqa: E501
        return f"{self.format(user_query)}<human_end>"
