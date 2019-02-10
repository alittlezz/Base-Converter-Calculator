import unittest
from math import log2


def map_to_int(char):
    """
        Converts char to its integer value

        Args:
            char(str): char to be converted

        Returns:
            int: char correspondent
    """
    dic = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'A': 10,
        'B': 11,
        'C': 12,
        'D': 13,
        'E': 14,
        'F': 15
    }
    return dic[char]

def map_to_string(int):
    """
        Converts int to its char value

        Args:
            int(int): int to be converted

        Returns:
            char: int correspondent
    """
    dic = {
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F',
    }
    return dic[int]


class BigNumber:
    """
        Class for big numbers

        Attributes:
            number(list): list of digits of number
            base(int): base of the number
    """
    def __init__(self, number, base):
        self.number = list(map(map_to_int, reversed(number)))
        self.base = base

    @property
    def len(self):
        return len(self.number)

    def __lt__(self, other):
        """
            Checks if self < other

            Args:
                other(BigNumber): number to compare to

            Raises:
                ValueError: if self base and other base are different

            Returns:
                bool: True if self < other
                      False otherwise
        """
        if self.base == other.base:
            if self.len == other.len:
                for i in range(self.len - 1, -1, -1):
                    if self.number[i] == other.number[i]:
                        continue
                    return self.number[i] < other.number[i]
                return False
            else:
                return self.len < other.len
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru comparare")

    def __le__(self, other):
        """
            Checks if self <= other

            Args:
                other(BigNumber): number to compare to

            Raises:
                ValueError: if self base and other base are different

            Returns:
                bool: True if self <= other
                      False otherwise
        """
        if self.base == other.base:
            if self.len == other.len:
                for i in range(self.len - 1, -1, -1):
                    if self.number[i] == other.number[i]:
                        continue
                    return self.number[i] < other.number[i]
                return True
            else:
                return self.len < other.len
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru comparare")

    def __add__(self, other):
        """
            Explicatii:
                Parcurgem cifrele numarului de la cele inferioare la cele superioare:
                Current = transport + cifra curenta + cifra curenta de la celalalt numar
                La rezultat adaugam restul impartirii lui current la baza, iar transportul devine catul impartirii
                La final cat timp mai avem transport il adaugam la rezultat
        """

        """
            Adds self and other

            Args:
                other(BigNumber): number to add to self

            Raises:
                ValueError: if self base and other base are different

            Returns:
                BigNumber: self + other
        """
        if self.base == other.base:
            transport = 0
            result = BigNumber([], self.base)
            for i in range(max(self.len, other.len)):
                current = transport
                try:
                    current += self.number[i]
                except IndexError:
                    pass
                try:
                    current += other.number[i]
                except IndexError:
                    pass
                result.number.append(current % self.base)
                transport = current // self.base
            if transport:
                result.number.append(transport)
            return result
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru adunare")

    def __sub__(self, other):
        """
            Explicatii:
                Parcurgem cifrele numarului de la cele inferioare la cele superioare:
                Current = transport + cifra curenta - cifra curenta de la celalalt numar
                Daca current < 0 atunci adunam la el baza si facem transportul = -1
                La rezultat adaugam current
                La final eliminam 0 superiori
        """

        """
            Subtracts self and other

            Args:
                other(BigNumber): number to subtract from self

            Raises:
                ValueError: if self base and other base are different

            Returns:
                BigNumber: self - other
        """
        if self.base == other.base:
            if self < other:
                raise ValueError("Introduceti un numar A >= B")
            transport = 0
            result = BigNumber([], self.base)
            for i in range(self.len):
                current = transport + self.number[i]
                try:
                    current -= other.number[i]
                except IndexError:
                    pass

                if current < 0:
                    current += self.base
                    transport = -1
                else:
                    transport = 0
                result.number.append(current)
            while result.len > 1 and result.number[-1] == 0:
                result.number.pop()
            return result
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru scadere")

    def __mul__(self, other):
        """
            Explicatii:
                Parcurgem cifrele numarului de la cele inferioare la cele superioare:
                Current = transport + cifra curenta * other(B)
                La rezultat adaugam restul impartirii lui current la baza, iar transportul devine catul impartirii
                La final cat timp mai exista transport il adaugam la numar si eliminam 0 superiori
        """
        
        """
            Multiplies self and other

            Args:
                other(BigNumber): number to multiply to self

            Raises:
                ValueError: if self base and other base are different
                            if other contains more than 1 digit

            Returns:
                BigNumber: self * other
        """
        if self.base == other.base:
            if other.len > 1:
                raise ValueError("B trebuie sa contina doar o cifra in baza " + str(other.base))
            transport = 0
            result = BigNumber([], self.base)
            B = other.number[0]
            for i in range(self.len):
                current = transport + self.number[i] * B
                result.number.append(current % self.base)
                transport = current // self.base
            while transport:
                result.number.append(transport % self.base)
                transport //= self.base
            while result.len > 1 and result.number[-1] == 0:
                result.number.pop()
            return result
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru inmultire")

    def __floordiv__(self, other):
        """
            Explicatii:
                Parcurgem cifrele numarului de la cele superioare la cele inferioare:
                Current = transport * baza + cifra curenta
                La rezultat adaugam current impartit la celalalt numar(B), iar transportul devine restul impartirii
                La final eliminam 0 superiori
        """

        """
            Divides self and other

            Args:
                other(BigNumber): number to divide from self

            Raises:
                ValueError: if self base and other base are different
                            if other contains more than 1 digit
                            if other is equal to 0

            Returns:
                BigNumber, BigNumber: self / other, self % other
        """
        if self.base == other.base:
            if other.len > 1:
                raise ValueError("B trebuie sa contina doar o cifra in baza " + str(other.base))
            transport = 0
            result = BigNumber([], self.base)
            B = other.number[0]
            if B == 0:
                raise ValueError("B trebuie sa fie diferit de 0")
            for i in range(self.len - 1, -1, -1):
                current = transport * self.base + self.number[i]
                result.number.insert(0, current // B)
                transport = current % B
            while result.len > 1 and result.number[-1] == 0:
                result.number.pop()
            return result, BigNumber(map_to_string(transport), self.base)
        else:
            raise ValueError("Introduceti A si B in aceeasi baza pentru inmultire")

    def __repr__(self):
        return "".join(map(map_to_string, reversed(self.number))) + '(' + str(self.base) + ')'

    def __eq__(self, other):
        return self.base == other.base and self.number == other.number

    def __iter__(self):
        return iter(self.number)

    def copy(self):
        return BigNumber("".join(map(map_to_string, reversed(self.number))), self.base)


def parse_to_bignumber(input):
    """
        Converts input to number and base obtaining a BigNumber

        Args:
            input(str): raw string to be parsed

        Raises:
            ValueError: if number or base are in the wrong format

        Returns:
            BigNumber: input parsed
    """
    input = input.strip()
    input = input.upper()
    try:
        number = input[:input.index('(')]
    except ValueError:
        raise ValueError("Introduceti baza numarului, el fiind de forma [numar(baza)]")
    valid_chars = '0123456789ABCDEF'
    for digit in number:
        if digit not in valid_chars:
            raise ValueError("Introduceti doar cifre sau literele A, B, C, D, F pentru numar si sa fie de forma [numar(baza)]")
    try:
        base = int(input[input.index('(') + 1 : -1])
        return BigNumber(number, base)
    except ValueError:
        raise ValueError("Introduceti doar cifre pentru baza, iar numarul trebuie sa fie de forma [numar(baza)]")

def kth_power(number, k):
    """
        Calculates number to the power of k

        Args:
            number(BigNumber): base of the power
            k(int): exponent of the power

        Raises:
            ValueError: if number contains more than 1 digit

        Returns:
            BigNumber: number ^ k
    """
    if number.len > 1:
        raise ValueError("Numarul poate fi doar o cifra in baza " + str(number.base))
    if k == 0:
        return BigNumber("1", number.base)
    result = BigNumber("1", number.base)
    for i in range(k):
        result = result * number
    return result


def concat_numbers(A, B):
    """
        Concatenates A and B

        Args:
            A(BigNumber): first number of the concatenation
            B(BigNumber): second number of the concatenation

        Raises:
            ValueError: if base of A is different than base of B

        Returns:
            BigNumber: A concatenated with B
    """
    if A.base != B.base:
        raise ValueError("Nu putem concatena 2 numere cu baze diferite")

    result = A.copy()
    result.number = B.number + result.number
    while result.len > 1 and result.number[-1] == 0:
        result.number.pop()
    return result


class TestBigNumber(unittest.TestCase):
    def test_add_base10(self):
        self.assertEqual(BigNumber("9", 10) + BigNumber("1", 10), BigNumber("10", 10))
        self.assertEqual(BigNumber("19", 10) + BigNumber("2", 10), BigNumber("21", 10))
        self.assertEqual(BigNumber("99", 10) + BigNumber("101", 10), BigNumber("200", 10))
        self.assertEqual(BigNumber("1500", 10) + BigNumber("13291", 10), BigNumber("14791", 10))
        self.assertEqual(BigNumber("123", 10) + BigNumber("321", 10), BigNumber("444", 10))
        self.assertEqual(BigNumber("0", 10) + BigNumber("0", 10), BigNumber("0", 10))

    def test_add_base2(self):
        self.assertEqual(BigNumber("0", 2) + BigNumber("10", 2), BigNumber("10", 2))
        self.assertEqual(BigNumber("11", 2) + BigNumber("10", 2), BigNumber("101", 2))
        self.assertEqual(BigNumber("101", 2) + BigNumber("10", 2), BigNumber("111", 2))
        self.assertEqual(BigNumber("110011", 2) + BigNumber("11100", 2), BigNumber("1001111", 2))
        self.assertEqual(BigNumber("10101010", 2) + BigNumber("101010101", 2), BigNumber("111111111", 2))

    def test_add_base16(self):
        self.assertEqual(BigNumber("9", 16) + BigNumber("1", 16), BigNumber("A", 16))
        self.assertEqual(BigNumber("9", 16) + BigNumber("3", 16), BigNumber("C", 16))
        self.assertEqual(BigNumber("9", 16) + BigNumber("7", 16), BigNumber("10", 16))
        self.assertEqual(BigNumber("AC", 16) + BigNumber("AC", 16), BigNumber("158", 16))
        self.assertEqual(BigNumber("BEDF", 16) + BigNumber("10ACF", 16), BigNumber("1C9AE", 16))

    def test_sub_base10(self):
        self.assertEqual(BigNumber("3", 10) - BigNumber("3", 10), BigNumber("0", 10))
        self.assertEqual(BigNumber("10", 10) - BigNumber("1", 10), BigNumber("9", 10))
        self.assertEqual(BigNumber("333", 10) - BigNumber("309", 10), BigNumber("24", 10))
        self.assertEqual(BigNumber("101", 10) - BigNumber("5", 10), BigNumber("96", 10))
        self.assertEqual(BigNumber("1111", 10) - BigNumber("1100", 10), BigNumber("11", 10))

    def test_sub_base2(self):
        self.assertEqual(BigNumber("1", 2) - BigNumber("1", 2), BigNumber("0", 2))
        self.assertEqual(BigNumber("1010", 2) - BigNumber("1", 2), BigNumber("1001", 2))
        self.assertEqual(BigNumber("1001100", 2) - BigNumber("1001", 2), BigNumber("1000011", 2))
        self.assertEqual(BigNumber("1001100", 2) - BigNumber("111000", 2), BigNumber("10100", 2))
        self.assertEqual(BigNumber("1000000000000", 2) - BigNumber("1111111", 2), BigNumber("111110000001", 2))

    def test_sub_base16(self):
        self.assertEqual(BigNumber("A", 16) - BigNumber("1", 16), BigNumber("9", 16))
        self.assertEqual(BigNumber("1AC", 16) - BigNumber("23", 16), BigNumber("189", 16))
        self.assertEqual(BigNumber("CDDF", 16) - BigNumber("EC8", 16), BigNumber("BF17", 16))
        self.assertEqual(BigNumber("10", 16) - BigNumber("1", 16), BigNumber("F", 16))

    def test_mul_base10(self):
        self.assertEqual(BigNumber("2", 10) * BigNumber("3", 10), BigNumber("6", 10))
        self.assertEqual(BigNumber("20", 10) * BigNumber("3", 10), BigNumber("60", 10))
        self.assertEqual(BigNumber("19", 10) * BigNumber("4", 10), BigNumber("76", 10))
        self.assertEqual(BigNumber("101", 10) * BigNumber("5", 10), BigNumber("505", 10))
        self.assertEqual(BigNumber("56498", 10) * BigNumber("9", 10), BigNumber("508482", 10))
        self.assertEqual(BigNumber("10", 10) * BigNumber("1", 10), BigNumber("10", 10))
        self.assertEqual(BigNumber("10", 10) * BigNumber("0", 10), BigNumber("0", 10))

    def test_mul_base2(self):
        self.assertEqual(BigNumber("101", 2) * BigNumber("1", 2), BigNumber("101", 2))
        self.assertEqual(BigNumber("101", 2) * BigNumber("0", 2), BigNumber("0", 2))

    def test_mul_base16(self):
        self.assertEqual(BigNumber("1", 16) * BigNumber("F", 16), BigNumber("F", 16))
        self.assertEqual(BigNumber("F", 16) * BigNumber("1", 16), BigNumber("F", 16))
        self.assertEqual(BigNumber("1CD", 16) * BigNumber("0", 16), BigNumber("0", 16))
        self.assertEqual(BigNumber("1CD", 16) * BigNumber("A", 16), BigNumber("1202", 16))
        self.assertEqual(BigNumber("DDEF785", 16) * BigNumber("F", 16), BigNumber("D01080CB", 16))

    def test_div_base10(self):
        self.assertEqual(BigNumber("10", 10) // BigNumber("3", 10), (BigNumber("3", 10), BigNumber("1", 10)))
        self.assertEqual(BigNumber("15", 10) // BigNumber("3", 10), (BigNumber("5", 10), BigNumber("0", 10)))
        self.assertEqual(BigNumber("7", 10) // BigNumber("9", 10), (BigNumber("0", 10), BigNumber("7", 10)))
        self.assertEqual(BigNumber("130", 10) // BigNumber("7", 10), (BigNumber("18", 10), BigNumber("4", 10)))
        self.assertEqual(BigNumber("1000", 10) // BigNumber("9", 10), (BigNumber("111", 10), BigNumber("1", 10)))
        self.assertEqual(BigNumber("13", 10) // BigNumber("1", 10), (BigNumber("13", 10), BigNumber("0", 10)))

    def test_div_base2(self):
        self.assertEqual(BigNumber("10", 2) // BigNumber("1", 2), (BigNumber("10", 2), BigNumber("0", 2)))
        self.assertEqual(BigNumber("1010", 2) // BigNumber("1", 2), (BigNumber("1010", 2), BigNumber("0", 2)))

    def test_div_base16(self):
        self.assertEqual(BigNumber("F", 16) // BigNumber("A", 16), (BigNumber("1", 16), BigNumber("5", 16)))
        self.assertEqual(BigNumber("1F", 16) // BigNumber("A", 16), (BigNumber("3", 16), BigNumber("1", 16)))
        self.assertEqual(BigNumber("AABB", 16) // BigNumber("F", 16), (BigNumber("B61", 16), BigNumber("C", 16)))

    def test_kth_power(self):
        self.assertEqual(kth_power(BigNumber("1", 10), 5), BigNumber("1", 10))
        self.assertEqual(kth_power(BigNumber("2", 10), 5), BigNumber("32", 10))
        self.assertEqual(kth_power(BigNumber("3", 10), 4), BigNumber("81", 10))
        self.assertEqual(kth_power(BigNumber("7", 10), 10), BigNumber("282475249", 10))

    def test_concat_numbers(self):
        self.assertEqual(concat_numbers(BigNumber("123", 10), BigNumber("456", 10)), BigNumber("123456", 10))
        self.assertEqual(concat_numbers(BigNumber("0", 10), BigNumber("1", 10)), BigNumber("1", 10))
        self.assertEqual(concat_numbers(BigNumber("1", 10), BigNumber("0", 10)), BigNumber("10", 10))
        self.assertEqual(concat_numbers(BigNumber("0", 10), BigNumber("0", 10)), BigNumber("0", 10))
        self.assertEqual(concat_numbers(BigNumber("9923", 10), BigNumber("12340", 10)), BigNumber("992312340", 10))

def convert_by_substitution(number, base):
    """
        Explicatii:
            Parcurgem cifrele numarului(care sunt deja in ordine inversa) si pastram in current_power puterea curenta(baza in care e numarul la pozitia curenta)
            Facem cifra curenta * puterea curenta si adunam la rezultat
            Toate operatiile le facem in baza destinatie
    """

    """
        Converts number to base using substitution

        Args:
            number(BigNumber): number to be converted
            base(int): destination base

        Raises:
            ValueError: if numar base if bigger than destination base

        Returns:
            BigNumber: number converted to base
    """
    if number.base == base:
        return number
    if number.base > base:
        raise ValueError("Numarul trebuie sa fie intr-o baza mai mica decat cea destinatie pentru substitutie")

    current_power = BigNumber("1", base)
    result = BigNumber("0", base)
    for digit in number:
        result = result + current_power * BigNumber(map_to_string(digit), base)
        current_power = current_power * BigNumber(map_to_string(number.base), base)
    return result

def convert_by_division(number, base):
    """
        Explicatii:
            Atat timp cat numarul este diferit de 0 facem urmatoarele:
            Impartim numarul la baza destinatie
            Restul il adaugam la rezultat, iar catul devine noul numar
    """

    """
        Converts number to base using division

        Args:
            number(BigNumber): number to be converted
            base(int): destination base

        Raises:
            ValueError: if numar base if bigger than destination base

        Returns:
            BigNumber: number converted to base
    """
    if number.base == base:
        return number
    if number.base < base:
        raise ValueError("Numarul trebuie sa fie intr-o baza mai mare decat cea destinatie pentru substitutie")

    if number == BigNumber("0", number.base):
        return BigNumber("0", base)

    result = BigNumber("", base)
    current_number = number.copy()
    while current_number != BigNumber("0", number.base):
        current_number, remainder = current_number // BigNumber(map_to_string(base), number.base)
        result.number.append(remainder.number[0])
    return result

def convert_bucket_from_2(number):
    """
        Converts number from base 2 to its correspondant in base 16

        Args:
            number(BigNumber): number to be converted

        Returns:
            int: number converted to base 16
    """
    dic = {
        "0000": 0,
        "0001": 1,
        "0010": 2,
        "0011": 3,
        "0100": 4,
        "0101": 5,
        "0110": 6,
        "0111": 7,
        "1000": 8,
        "1001": 9,
        "1010": 10,
        "1011": 11,
        "1100": 12,
        "1101": 13,
        "1110": 14,
        "1111": 15
    }
    number = "".join(map(map_to_string, reversed(number)))
    while len(number) != 4:
        number = "0" + number
    return dic[number]

def convert_fast_from_2(number, base):
    """
        Explicatii:
            Luam lungimea unui bucket_size care trebuie convertit = log2(base)
            Adaugam 0 cat timp lungimea numarului initial nu este divizibila cu bucket_size
            Trecem prin cifrele numarului, si convertim folosind o tabela de conversie rapida fiecare subsecventa de lungime bucket_size in baza base
    """

    """
        Converts number to base using fast conversion method

        Args:
            number(BigNumber): number to be converted
            base(int): destination base

        Raises:
            ValueError: if base is not in [4, 8, 16]

        Returns:
            BigNumber: number converted to base
    """
    if number.base == base:
        return number
    if base not in [4, 8, 16]:
        raise ValueError("Introduceti o baza putere a lui 2 pentru a converti rapid din baza 2")

    bucket_size = int(log2(base))
    number_cpy = number.copy()
    while number_cpy.len % bucket_size != 0:
        number_cpy.number.append(0)

    result = BigNumber("", base)
    for i in range(0, number_cpy.len, bucket_size):
        result.number.append(convert_bucket_from_2(number_cpy.number[i : i + bucket_size]))
    return result

def convert_bucket_to_2(number, bucket_size):
    """
        Converts number from base 16, 8, 4 to its correspondant in base 2

        Args:
            number(BigNumber): number to be converted

        Returns:
            int: number converted to base 2
    """
    dic = {
        0: "0000",
        1: "0001",
        2: "0010",
        3: "0011",
        4: "0100",
        5: "0101",
        6: "0110",
        7: "0111",
        8: "1000",
        9: "1001",
        10: "1010",
        11: "1011",
        12: "1100",
        13: "1101",
        14: "1110",
        15: "1111"
    }
    result = dic[number]
    while len(result) > bucket_size:
        result = result[1:]
    return list(map(int, reversed(result)))

def convert_fast_to_2(number):
    """
        Explicatii:
            Luam lungimea unui bucket_size care trebuie obtinut = log2(base)
            Trecem prin cifrele numarului, si convertim folosind o tabela de conversie rapida fiecare cifra intr-o subsecventa de lungime bucket_size
            La final eliminam 0 superiori
    """

    """
        Converts number to base 2 using fast conversion method

        Args:
            number(BigNumber): number to be converted

        Returns:
            BigNumber: number converted to base 2
    """
    if number.base == 2:
        return number

    bucket_size = int(log2(number.base))
    result = BigNumber("", 2)

    for digit in number:
        for digit2 in convert_bucket_to_2(digit, bucket_size):
            result.number.append(digit2)

    while result.len > 1 and result.number[-1] == 0:
        result.number.pop()
    return result

class TestConverter(unittest.TestCase):
    def test_convert_by_substitution(self):
        self.assertEqual(convert_by_substitution(BigNumber("0", 10), 16), BigNumber("0", 16))
        self.assertEqual(convert_by_substitution(BigNumber("1", 9), 10), BigNumber("1", 10))
        self.assertEqual(convert_by_substitution(BigNumber("10", 2), 5), BigNumber("2", 5))
        self.assertEqual(convert_by_substitution(BigNumber("102201", 3), 8), BigNumber("474", 8))
        self.assertEqual(convert_by_substitution(BigNumber("102300332", 4), 16), BigNumber("12C3E", 16))
        self.assertEqual(convert_by_substitution(BigNumber("10011100032615", 8), 10), BigNumber("550980564365", 10))
        self.assertEqual(convert_by_substitution(BigNumber("64331297107510432817", 10), 16), BigNumber("37CC6ADE0A1461431", 16))

    def test_convert_by_division(self):
        self.assertEqual(convert_by_division(BigNumber("0", 16), 10), BigNumber("0", 10))
        self.assertEqual(convert_by_division(BigNumber("1", 16), 10), BigNumber("1", 10))
        self.assertEqual(convert_by_division(BigNumber("1ACF64", 16), 10), BigNumber("1757028", 10))
        self.assertEqual(convert_by_division(BigNumber("1ACF64", 16), 5), BigNumber("422211103", 5))
        self.assertEqual(convert_by_division(BigNumber("4216341278", 9), 8), BigNumber("14177132406", 8))
        self.assertEqual(convert_by_division(BigNumber("5410512340125102345314", 6), 3), BigNumber("211111011010120112102020102120202101", 3))
        self.assertEqual(convert_by_division(BigNumber("5410512340125102345314", 6), 2), BigNumber("110111100000111011001100000111100101101111011111110001110", 2))

    def test_convert_fast_from_2(self):
        self.assertEqual(convert_fast_from_2(BigNumber("0", 2), 4), BigNumber("0", 4))
        self.assertEqual(convert_fast_from_2(BigNumber("0", 2), 8), BigNumber("0", 8))
        self.assertEqual(convert_fast_from_2(BigNumber("0", 2), 16), BigNumber("0", 16))
        self.assertEqual(convert_fast_from_2(BigNumber("1010", 2), 16), BigNumber("A", 16))
        self.assertEqual(convert_fast_from_2(BigNumber("101010", 2), 16), BigNumber("2A", 16))
        self.assertEqual(convert_fast_from_2(BigNumber("100110010", 2), 8), BigNumber("462", 8))
        self.assertEqual(convert_fast_from_2(BigNumber("10010100100", 2), 8), BigNumber("2244", 8))
        self.assertEqual(convert_fast_from_2(BigNumber("10010100100", 2), 4), BigNumber("102210", 4))
        self.assertEqual(convert_fast_from_2(BigNumber("1100111", 2), 4), BigNumber("1213", 4))

    def test_convert_fast_to_2(self):
        self.assertEqual(convert_fast_to_2(BigNumber("0", 4)), BigNumber("0", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("0", 8)), BigNumber("0", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("0", 16)), BigNumber("0", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("A", 16)), BigNumber("1010", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("2A", 16)), BigNumber("101010", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("462", 8)), BigNumber("100110010", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("2244", 8)), BigNumber("10010100100", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("102210", 4)), BigNumber("10010100100", 2))
        self.assertEqual(convert_fast_to_2(BigNumber("1213", 4)), BigNumber("1100111", 2))