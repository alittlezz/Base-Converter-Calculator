def validate_number(number):
    """
        Validates a number and its base

        Args:
            number(BigNumber): number to be validated

        Raises:
            ValueError: if number contains digits bigger or equal to the base
    """
    validate_base(number.base)
    for digit in number:
        if digit >= number.base:
            raise ValueError("Numarul trebuie sa contine cifre mai mici decat baza")

def validate_base(base):
    """
        Validates a base

        Args:
            base(int): base to be validated

        Raises:
            ValueError: if base is not in the possible bases set
    """
    if base not in [2, 3, 4, 5, 6, 7, 8, 9, 10, 16]:
        raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")