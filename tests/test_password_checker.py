
import pytest


from password_checker import (
    get_password_features,
    evaluate_password,
    is_common_password,
    calculate_score,
    classify_password,
    generate_recommendations,

)


@pytest.mark.parametrize(
    ("password", "expected_strength"),
    [
        ("abc", "Weak"),
        ("abcdefgh", "Weak"),
        ("Password1", "Medium"),
        ("Abcdefgh12!x", "Strong"),
        ("123456789012", "Medium"),
        
    ],
)
def test_password_strength(password, expected_strength):
    result = evaluate_password(password)

    assert result["strength"] == expected_strength


def test_password_length():
    result = get_password_features("Abcdef12!")

    assert result["length"] == 9


def test_character_detection():
    result = get_password_features("Abc123!x")

    assert result["has_lowercase"] is True
    assert result["has_uppercase"] is True
    assert result["has_digit"] is True
    assert result["has_symbol"] is True


def test_password_without_uppercase():
    result = get_password_features("password123!")

    assert result["has_uppercase"] is False


def test_password_without_digits():
    result = get_password_features("Password!")

    assert result["has_digit"] is False


def test_score_is_within_expected_range():
    result = evaluate_password("Abcdefgh12!x")

    assert 0 <= result["score"] <= 6


def test_empty_password_is_rejected():
    with pytest.raises(ValueError):
        evaluate_password("")


def test_whitespace_only_password_is_rejected():
    with pytest.raises(ValueError):
        evaluate_password("   ")


def test_non_string_input_is_rejected():
    with pytest.raises(TypeError):
        evaluate_password(None)


def test_whitespace_does_not_count_as_symbol():
    result = get_password_features("hello world")

    assert result["has_symbol"] is False


def test_punctuation_counts_as_symbol():
    result = get_password_features("hello!")

    assert result["has_symbol"] is True


def test_unicode_letters_are_detected():
    result = get_password_features("École123!")

    assert result["has_uppercase"] is True
    assert result["has_lowercase"] is True
    assert result["has_digit"] is True
    assert result["has_symbol"] is True

@pytest.mark.parametrize(
    "password",
    ["password", "PASSWORD"],
)
def test_common_password_is_detected_case_insensitively(password):
    assert is_common_password(password) is True


def test_common_password_cannot_be_classified_as_strong():
    result = evaluate_password("Password123!")

    assert result["is_common_password"] is True
    assert result["strength"] == "Weak"


def test_unlisted_password_is_not_marked_common():
    assert is_common_password("UnlistedExample9#") is False

def test_evaluation_is_deterministic():
    password = "UniquePassphrase9#"

    first_result = evaluate_password(password)
    second_result = evaluate_password(password)

    assert first_result == second_result


def test_result_does_not_expose_raw_password():
    password = "UniquePassphrase9#"

    result = evaluate_password(password)

    assert "password" not in result
    assert password not in str(result)


def test_common_password_is_never_strong():
    result = evaluate_password("Password123!")

    assert result["is_common_password"] is True
    assert result["strength"] == "Weak"
from password_checker import calculate_score, classify_password


def test_calculate_score_for_all_features():
    features = {
        "length": 12,
        "has_lowercase": True,
        "has_uppercase": True,
        "has_digit": True,
        "has_symbol": True,
    }

    assert calculate_score(features) == 6


def test_calculate_score_for_no_features():
    features = {
        "length": 5,
        "has_lowercase": False,
        "has_uppercase": False,
        "has_digit": False,
        "has_symbol": False,
    }

    assert calculate_score(features) == 0


def test_common_password_is_classified_as_weak():
    features = {
        "length": 12,
        "has_lowercase": True,
        "has_uppercase": True,
        "has_digit": True,
        "has_symbol": True,
    }

    assert classify_password(features, 6, True) == "Weak"


def test_long_password_with_high_score_is_strong():
    features = {
        "length": 12,
        "has_lowercase": True,
        "has_uppercase": True,
        "has_digit": True,
        "has_symbol": True,
    }

    assert classify_password(features, 6, False) == "Strong"
def test_short_password_gets_length_recommendation():
    result = evaluate_password("abc")

    recommendations = generate_recommendations(result)

    assert any(
        "longer password" in item
        for item in recommendations
    )


def test_common_password_gets_warning():
    result = evaluate_password("password")

    recommendations = generate_recommendations(result)

    assert any(
        "common-password list" in item
        for item in recommendations
    )


def test_recommendations_are_returned_as_a_list():
    result = evaluate_password("UniquePassphrase9#")

    assert isinstance(generate_recommendations(result), list)