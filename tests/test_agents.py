import pytest
from src.agents.validator import ValidatorAgent

# Pytest automatically discovers any function starting with "test_"


def test_validator_success():
    """Test that valid JSON passes the validator."""
    validator = ValidatorAgent()
    valid_data = {"steps": ["Analyze logs", "Check database"]}

    # assert checks if the condition is True. If it's False, the test fails.
    assert validator.validate_planner_output(valid_data) is True


def test_validator_missing_key():
    """Test that missing the 'steps' key raises a KeyError."""
    validator = ValidatorAgent()
    invalid_data = {"wrong_key": ["Analyze logs"]}

    # We use pytest.raises to mathematically prove that this specific error is triggered
    with pytest.raises(KeyError):
        validator.validate_planner_output(invalid_data)


def test_validator_not_a_dictionary():
    """Test that passing a list instead of a dictionary raises a ValueError."""
    validator = ValidatorAgent()
    invalid_data = ["Analyze logs", "Check database"]  # This is a list, not a dict

    with pytest.raises(ValueError):
        validator.validate_planner_output(invalid_data)


def test_validator_steps_not_a_list():
    """Test that passing a string for steps raises a TypeError."""
    validator = ValidatorAgent()
    invalid_data = {
        "steps": "Analyze logs and check database"
    }  # String instead of array

    with pytest.raises(TypeError):
        validator.validate_planner_output(invalid_data)
