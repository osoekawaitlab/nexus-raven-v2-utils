from nexusravenv2utils.core import Output, ParseError


def test_output_parse_raises_parse_error_when_output_is_invalid() -> None:

    output = "Invalid output"
    try:
        Output.parse(output)
    except ParseError as e:
        assert str(e) == "Invalid output"
    else:
        assert False
