from fractions import Fraction
from decimal import Decimal

def simplex_method(c, A, b):

    def pivot(matrix, row, col):
        pivot_element = matrix[row][col]

        for r in range(len(matrix)):
            if r != row:
                matrix[r] = [(matrix[r][i] - Fraction((matrix[r][col] * matrix[row][i]), (pivot_element))) for i in range(len(matrix[0]))]

        matrix[row] = [Fraction(x, pivot_element) for x in matrix[row]]

        basis[row] = col
        

    # Построение начальной симплекс-таблицы
    num_vars = len(c)
    num_constraints = len(b)

    basis = list(range(num_constraints, num_constraints*2))

    tableau = [A[i] + [0] * i + [1] + [0] * (num_constraints - i - 1) + [b[i]] for i in range(num_constraints)]
    tableau.append([-x for x in c] + [0] * num_constraints + [0])

    # Печать таблицы для отладки
    def print_tableau():
        for row in tableau:
            print("\t".join(map(str, row)))
        print()

    print("Начальная таблица:")
    print_tableau()

    # Симплекс-алгоритм
    while True:
        if min(tableau[-1]) >= 0:
            break
        # Поиск входящего столбца
        pivot_col = min(range(len(c)), key=lambda col: tableau[-1][col])

        # Поиск выходящей строки
        ratios = []
        for row in range(num_constraints):
            element = tableau[row][pivot_col]
            if element > 0:
                ratios.append(tableau[row][-1] / element)
            else:
                ratios.append(float('inf'))

        pivot_row = min(range(num_constraints), key=lambda r: ratios[r])
        if ratios[pivot_row] == float('inf'):
            raise ValueError("Задача не имеет решения (неограниченная целевая функция)")

        # Выполнить операцию сводки
        pivot(tableau, pivot_row, pivot_col)

        print(f"После приведения строки {pivot_row + 1} и столбца {pivot_col + 1}:")
        print_tableau()

    # Получение решения
    solution = [0] * num_vars
    for i in range(num_constraints):
        basic_var_index = next((j for j in range(num_vars) if tableau[i][j] == 1), None)
        if basic_var_index is not None:
            solution[basic_var_index] = tableau[i][-1]

    return list(map(float, solution)), tableau[-1][-1]

# Данные задачи
c = [-3, 4, -1]  # Целевая функция
A = [
    [1, 2, 1],
    [2, 1, 2],
    [3, 1, 2],
]
b = [10, 6, 12]



solution, max_value = simplex_method(c, A, b)
print("Оптимальное решение:", solution)
print("Максимальное значение целевой функции:", max_value)


