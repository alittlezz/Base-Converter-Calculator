from big_number import convert_by_substitution, convert_by_division, convert_fast_to_2, convert_fast_from_2


class Controller:
    def __init__(self):
        pass

    def convert_general(self, number, base):
        """
            Converts a number to base in the most optimal way

            Args:
                number(BigNumber): number to be converted
                base(int): destination base

            Returns:
                BigNumber: number converted to base
        """
        if number.base == base:
            print("Numarul", number, "este deja in baza", base)
            return number
        if (number.base == 2 and base in [4, 8, 16]) or (number.base in [4, 8, 16] and base == 2):
            return self.convert_fast(number, base)
        if number.base < base:
            return self.convert_substitution(number, base)
        return self.convert_division(number, base)

    def convert_intermediary(self, number, base, intermediary_base):
        """
            Converts a number to base using an intermediary base

            Args:
                number(BigNumber): number to be converted
                base(int): destination base
                intermediary_base(int): intermediary base

            Returns:
                BigNumber: number converted to base
        """
        number_intermediary = self.convert_general(number, intermediary_base)
        result = self.convert_general(number_intermediary, base)
        return result

    def convert_substitution(self, number, base):
        """
            Converts a number to base using substitution method

            Args:
                number(BigNumber): number to be converted
                base(int): destination base

            Returns:
                BigNumber: number converted to base
        """
        if number.base == base:
            print("Numarul", number, "este deja in baza", base)
            return number
        result = convert_by_substitution(number, base)
        print("Numarul", number, "a fost convertit in", result, "prin substitutie")
        return result

    def convert_division(self, number, base):
        """
            Converts a number to base using division method

            Args:
                number(BigNumber): number to be converted
                base(int): destination base

            Returns:
                BigNumber: number converted to base
        """
        if number.base == base:
            print("Numarul", number, "este deja in baza", base)
            return number
        result = convert_by_division(number, base)
        print("Numarul", number, "a fost convertit in", result, "prin impartiri repetate")
        return result

    def convert_fast(self, number, base):
        """
            Converts a number to base using fast conversion method

            Args:
                number(BigNumber): number to be converted
                base(int): destination base

            Returns:
                BigNumber: number converted to base
        """
        if number.base == base:
            print("Numarul", number, "este deja in baza", base)
            return number
        if base == 2:
            result = convert_fast_to_2(number)
            print("Numarul", number, "a fost convertit in", result, "prin conversie rapida")
        else:
            result = convert_fast_from_2(number, base)
            print("Numarul", number, "a fost convertit in", result, "prin conversie rapida")
        return result