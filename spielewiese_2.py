# Purpur Tentakel
# 10.04.2022
# Example Calculater
# Python 3.10

_possible_operators: tuple = (
    "+",
    "-",
    "*",
    "/",
)


def _is_valid_operator(operator_for_calculate: str) -> bool:
    if operator_for_calculate not in _possible_operators:
        return False
    return True


def _is_valid_var(vars_to_check: tuple) -> bool:
    for var_to_check in vars_to_check:
        try:
            float(var_to_check)
        except ValueError:
            print(f"Invalider Input ({var_to_check})")
            return False
        if len(var_to_check) > 20:
            print(f"Eingabe zu lang {var_to_check[:20]}")
            return False
    return True


def _is_next_calculation(var: str) -> bool:
    if var == "0":
        return True
    return False


def _calculate_with_round(var_1_to_calculate: float, var_2_to_calculate: float, operator_for_calculate: str,
                          round_: int) -> float:
    match operator_for_calculate:
        case "+":
            return round(_addition(var_1_to_calculate=var_1_to_calculate, var_2_to_calculate=var_2_to_calculate),
                         round_)
        case "-":
            return round(_subtraction(var_1_to_calculate=var_1_to_calculate, var_2_to_calculate=var_2_to_calculate),
                         round_)
        case "*":
            return round(_multiplication(var_1_to_calculate=var_1_to_calculate, var_2_to_calculate=var_2_to_calculate),
                         round_)
        case "/":
            return round(_division(var_1_to_calculate=var_1_to_calculate, var_2_to_calculate=var_2_to_calculate),
                         round_)


def _addition(var_1_to_calculate: float, var_2_to_calculate: float) -> float:
    return var_1_to_calculate + var_2_to_calculate


def _subtraction(var_1_to_calculate: float, var_2_to_calculate: float) -> float:
    return var_1_to_calculate - var_2_to_calculate


def _multiplication(var_1_to_calculate: float, var_2_to_calculate: float) -> float:
    return var_1_to_calculate * var_2_to_calculate


def _division(var_1_to_calculate: float, var_2_to_calculate: float) -> float:
    return var_1_to_calculate / var_2_to_calculate


if __name__ == "__main__":
    next_operation: bool = True
    while next_operation:
        print("\nNächste Rechnung:")

        operator: str = input("Welche Rechenart soll verwendet werden? (+,-,*,/)\n")
        if not _is_valid_operator(operator_for_calculate=operator):
            print("Kein Valider Operator")
            continue

        var_1: str = input("Erste Zahl\n")
        var_2: str = input("Zweite Zahl\n")
        if not _is_valid_var(vars_to_check=(var_1, var_2)):
            continue

        result: float = _calculate_with_round(var_1_to_calculate=float(var_1), var_2_to_calculate=float(var_2),
                                              operator_for_calculate=operator, round_=2)

        print(f"{var_1} {operator} {var_2} = {result}")

        if not _is_next_calculation(input("Noch eine Rechnung ausführen? '0' = Ja\n")):
            next_operation = False
