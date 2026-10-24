
from getpass import getpass

COMMON_PASSWORDS = frozenset({
    "123456",
    "123456789",
    "password",
    "password123",
    "password123!",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
})


def validate_password_input(password: str) -> None:
    """Reject invalid password input."""
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not password or password.isspace():
        raise ValueError("Password cannot be empty or whitespace only.")


def get_password_features(password: str) -> dict:
    """Extract password characteristics without returning the password."""
    return {
        "length": len(password),
        "has_lowercase": any(c.islower() for c in password),
        "has_uppercase": any(c.isupper() for c in password),
        "has_digit": any(c.isdigit() for c in password),
        "has_symbol": any(
            not c.isalnum() and not c.isspace()
            for c in password
        ),
    }


def is_common_password(password: str) -> bool:
    """Check for an exact match against the local denylist."""
    return password.casefold() in COMMON_PASSWORDS


def calculate_score(features: dict) -> int:
    """Calculate a heuristic score from 0 to 6."""
    score = 0

    if features["length"] >= 8:
        score += 1
    if features["length"] >= 12:
        score += 1

    for feature in (
        "has_lowercase",
        "has_uppercase",
        "has_digit",
        "has_symbol",
    ):
        if features[feature]:
            score += 1

    return score


def classify_password(
    features: dict,
    score: int,
    is_common: bool,
) -> str:
    """Classify a password using the project's heuristic rules."""
    if is_common or features["length"] < 8:
        return "Weak"

    if features["length"] >= 12 and score >= 5:
        return "Strong"

    if score >= 3:
        return "Medium"

    return "Weak"


def evaluate_password(password: str) -> dict:
    """Coordinate validation, feature extraction, scoring and classification."""
    validate_password_input(password)

    features = get_password_features(password)
    common = is_common_password(password)
    score = calculate_score(features)
    strength = classify_password(features, score, common)

    return {
        **features,
        "score": score,
        "strength": strength,
        "is_common_password": common,
    }



def generate_recommendations(result: dict) -> list[str]:
    """Generate actionable feedback from the evaluation result."""
    recommendations = []

    if result["is_common_password"]:
        recommendations.append(
            "Choose a password that is not on the common-password list."
        )

    if result["length"] < 12:
        recommendations.append(
            "Consider using a longer password or passphrase."
        )

    if not result["has_lowercase"]:
        recommendations.append("Consider including lowercase letters.")

    if not result["has_uppercase"]:
        recommendations.append("Consider including uppercase letters.")

    if not result["has_digit"]:
        recommendations.append("Consider including a number.")

    if not result["has_symbol"]:
        recommendations.append("Consider including a symbol.")

    if not recommendations:
        recommendations.append(
            "No issues were detected by these basic checks."
        )

    return recommendations

def main() -> None:
    print("=" * 40)
    print("       PASSWORD STRENGTH ANALYZER")
    print("=" * 40)

    password = getpass("Enter a test password: ")

    try:
        result = evaluate_password(password)
    except (TypeError, ValueError) as error:
        print(f"\nInvalid input: {error}")
        return

    print(f"\nStrength       : {result['strength'].upper()}")
    print(f"Score          : {result['score']}/6")
    print(f"Length         : {result['length']} characters")
    print(
        "Common password: "
        f"{'Yes' if result['is_common_password'] else 'No'}"
    )

    print("\nAnalysis:")
    for feature in (
        "has_lowercase",
        "has_uppercase",
        "has_digit",
        "has_symbol",
    ):
        label = feature.removeprefix("has_").replace("_", " ").title()
        status = "OK" if result[feature] else "!!"
        print(f"  [{status}] {label}")

    recommendations = generate_recommendations(result)

    print("\nRecommendations:")
    for recommendation in recommendations:
        print(f"  - {recommendation}")

    print("\nNote: This is a heuristic estimate, not a guarantee.")
    print("=" * 40)


if __name__ == "__main__":
    main()

