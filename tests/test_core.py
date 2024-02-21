from nexusravenv2utils.core import Argument, Function, Output, ParseError


def test_output_parse_raises_parse_error_when_output_is_invalid() -> None:

    output = "Invalid output"
    try:
        Output.parse(output)
    except ParseError as e:
        assert str(e) == "Invalid output"
    else:
        assert False


def test_output_parse_raises_parse_error_when_output_is_invalid_2() -> None:

    output = "Call:  \nThought: b"
    try:
        Output.parse(output)
    except ParseError as e:
        assert str(e) == "Call:  \nThought: b"
    else:
        assert False


def test_output_parse_raises_parse_error_when_empty_output() -> None:

    output = ""
    try:
        Output.parse(output)
    except ParseError as e:
        assert str(e) == ""
    else:
        assert False


def test_output_parse() -> None:

    output = """fulfillment, order fulfillment solutions, order fulfillment platforms, order fulfillment technology, order fulfillment software, order fulfillment app, order fulfillment service, order fulfillment partner, order fulfillment provider, order fulfillment platform, order fulfillment software companies, order fulfillment software for e-commerce, order fulfillment system for retail, order fulfillment software for retail
A few years ago, a friend was struggling to get his order fulfillment system to work the way he wanted it to. After going through countless trial and error sessions, he had decided to outsource his order fulfillment system to a well-known provider.
Here are some reasons why your order fulfillment needs an outsourcing partner:

1. Order fulfillment is a complex and time-consuming process that requires specialized knowledge and expertise. Outsourcing the order fulfillment process to a specialized partner will help ensure that your order fulfillment system runs smoothly and efficiently.
2. Outsourcing order fulfillment will allow you to focus on other important aspects of your business, such as marketing, sales, and customer service. This will help you avoid the distraction of having to manage the order fulfillment process in-house, which can be time-consuming and costly.
3. Outsourcing order fulfillment will help you to reduce your overhead costs, as the provider will handle the warehousing, packaging, and shipping of your products. This will allow you to save on costs associated with managing a large order fulfillment system in-house.
4. Outsourcing order fulfillment will also help you to get the best possible deal. By contracting with a third-party provider, you will be able to negotiate the best price and terms for your order fulfillment services, which will help you to save on costs. In summary, outsourcing order fulfillment to a well-known provider can help you to streamline your business processes, reduce costs, and improve your overall efficiency. By focusing on the core competencies of your business, you will be able to improve your bottom line and increase your profits."""  # noqa: E501
    try:
        Output.parse(output)
    except ParseError as e:
        assert str(e) == output
    else:
        assert False


def test_function_no_return_description() -> None:
    assert (
        str(
            Function(
                name="name",
                description="the description",
                arguments=[Argument(name="a")],
                return_type=int,
                return_description=None,
            )
        )
        == """\
Function:
def name(a) -> int:
    \"\"\"
    the description

    Args:
        a: (no description provided)

    Returns:
        int: (no description provided)
    \"\"\"
"""
    )


def test_function_no_arguments() -> None:
    assert (
        str(
            Function(
                name="name",
                description="the description",
                arguments=[],
                return_type=int,
                return_description="the return description",
            )
        )
        == """\
Function:
def name() -> int:
    \"\"\"
    the description

    Returns:
        int: the return description
    \"\"\"
"""
    )
