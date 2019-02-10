import os

from big_number import parse_to_bignumber
from controller import Controller
from validator import validate_number, validate_base


class ConsoleUI:
    def __init__(self, platform):
        self.platform = platform
        self.is_running = False
        self.controller = Controller()
        self.menu = {
            '1':  (self.add_numbers, "Adunati 2 numere"),
            '2':  (self.subtract_numbers, "Scadeti 2 numere"),
            '3':  (self.multiply_numbers, "Inmultiti 2 numere"),
            '4':  (self.divide_numbers, "Impartiti 2 numere"),
            '5':  (self.convert_general, "Convertiti dintr-o baza in alta prin detectare automata"),
            '6':  (self.convert_intermediary, "Convertiti dintr-o baza in alta folosind o baza intermediara"),
            '7':  (self.convert_substitution, "Convertiti dintr-o baza in alta prin substitutie"),
            '8':  (self.convert_division, "Convertiti dintr-o baza in alta prin impartiri succesive"),
            '9':  (self.convert_fast, "Convertiti dintr-o baza in alta prin conversie rapida"),
            '10': (self.print_start_message, "Afisati mesajul initial"),
            'x':  (self.close, "Inchide aplicatia")
        }

    def close(self):
        self.is_running = False

    def add_numbers(self):
        """
            Adds 2 numbers read from the console in a given base and outputs the result

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        B = input("Introduceti numarul B: ")
        B = parse_to_bignumber(B)
        validate_number(B)

        try:
            base = int(input("Introduceti baza pentru a efectua A + B: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        A = self.controller.convert_general(A, base)
        B = self.controller.convert_general(B, base)

        print(A, "+", B, "=", A + B)

    def subtract_numbers(self):
        """
            Subtracts 2 numbers read from the console in a given base and outputs the result

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        B = input("Introduceti numarul B: ")
        B = parse_to_bignumber(B)
        validate_number(B)

        try:
            base = int(input("Introduceti baza pentru a efectua A - B: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        A = self.controller.convert_general(A, base)
        B = self.controller.convert_general(B, base)

        print(A, "-", B, "=", A - B)

    def multiply_numbers(self):
        """
            Multiplies 2 numbers read from the console in a given base and outputs the result

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        B = input("Introduceti cifra B: ")
        B = parse_to_bignumber(B)
        validate_number(B)

        try:
            base = int(input("Introduceti baza pentru a efectua A * B: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        A = self.controller.convert_general(A, base)
        B = self.controller.convert_general(B, base)

        print(A, "*", B, "=", A * B)

    def divide_numbers(self):
        """
            Divides 2 numbers read from the console in a given base and outputs the result and the remainder

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        B = input("Introduceti cifra B: ")
        B = parse_to_bignumber(B)
        validate_number(B)

        try:
            base = int(input("Introduceti baza pentru a efectua A / B: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        A = self.controller.convert_general(A, base)
        B = self.controller.convert_general(B, base)

        result, remainder = A // B
        print(A, "/", B, "=", str(result) + ", rest =", remainder)

    def convert_general(self):
        """
            Converts a number to a given base in the most optimal approach

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        try:
            base = int(input("Introduceti baza destinatie: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        self.controller.convert_general(A, base)

    def convert_intermediary(self):
        """
            Converts a number to a given base using an intermediary base

            Raises:
                ValueError: if either the number or the base is wrong
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        try:
            intermediary_base = int(input("Introduceti baza intermediara: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(intermediary_base)

        try:
            base = int(input("Introduceti baza destinatie: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        self.controller.convert_intermediary(A, base, intermediary_base)

    def convert_substitution(self):
        """
            Converts a number to a given base using the substitution method

            Raises:
                ValueError: if either the number or the base is wrong
                            if the number base is bigger than the given base
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        try:
            base = int(input("Introduceti baza destinatie: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        self.controller.convert_substitution(A, base)

    def convert_division(self):
        """
            Converts a number to a given base using the division method

            Raises:
                ValueError: if either the number or the base is wrong
                            if the number base is smaller than the given base
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        try:
            base = int(input("Introduceti baza destinatie: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        self.controller.convert_division(A, base)

    def convert_fast(self):
        """
            Converts a number to a given base using the fast conversion method

            Raises:
                ValueError: if either the number or the base is wrong
                            if the number base or the destination base are not powers of 2
        """
        A = input("Introduceti numarul A: ")
        A = parse_to_bignumber(A)
        validate_number(A)

        try:
            base = int(input("Introduceti baza destinatie: "))
        except ValueError:
            raise ValueError("Baza trebuie sa fie din multimea {2, 3, 4, 5, 6, 7, 8, 9, 10, 16}")
        validate_base(base)

        self.print_delimiter()

        self.controller.convert_fast(A, base)

    def print_menu(self):
        for id, task in self.menu.items():
            print(str(id) + '.' + task[1])

    def print_delimiter(self):
        print("-" * 30)

    def print_start_message(self):
        self.print_delimiter()
        print("Aplicatie realizata de Cazaciuc Valentin, grupa 211")
        print("Indicatii de utilizare:")
        print("    -la fiecare iteratie va aparea un meniu; introduceti cifra sau litera respectiva si apasati Enter")
        print("    -cand aveti de introdus un numar, el trebuie sa fie de forma [numar(baza)]; de exemplu pentru a introduce pe 13 in baza 10 si 16 se va scrie 13(10), respectiv 13(16)")
        print("    -cand aveti de introdus o baza, ea trebuie sa fie de forma [baza]; de exemplu pentru baza 10 introduceti 10 si apasati Enter")
        print("    -daca se fac greseli(cum ar fi o baza diferita de cele posibile, un numar cu cifrele mai mari sau egale decat baza, caractere indisponibile sau format gresit) ele vor fi semnalate, iar programul va continua")
        self.print_delimiter()

    def run(self):
        """
            Runs the console application

            Steps:
                -print menu
                -take input
                -call functions based on input
                -clear screen
        """
        self.print_start_message()
        self.is_running = True
        while self.is_running:
            self.print_menu()
            self.print_delimiter()
            cmd = input("Introduceti comanda: ").strip()
            try:
                self.menu[cmd][0]()
            except KeyError:
                print("Introduceti o comanda valida")
            except ValueError as error:
                print(error)
            cmd = input("Apasati tasta Enter pentru a continua...")
            #print("\n" * 20)
            if self.platform == "Windows":
                os.system("cls")
            else:
                os.system("clear")