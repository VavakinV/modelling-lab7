def transportation_problem_min_cost(supply, demand, costs):
    # Результат распределения
    result = [[0 for _ in range(len(demand))] for _ in range(len(supply))]

    # Пока есть поставки и спрос
    while any(supply) and any(demand):
        # Найти минимальную стоимость в матрице
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(len(supply)):
            for j in range(len(demand)):
                if supply[i] > 0 and demand[j] > 0 and costs[i][j] < min_cost:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        # Определить объем для транспортировки
        allocation = min(supply[min_i], demand[min_j])

        # Записать результат
        result[min_i][min_j] = allocation

        # Обновить остатки поставок и спроса
        supply[min_i] -= allocation
        demand[min_j] -= allocation
    
    
    # Метод потенциалов
    def calculate_potentials():
        u = [0] * len(supply)
        v = [0] * len(demand)

        checked_u = [0 for _ in range(len(supply))]
        checked_v = [0 for _ in range(len(demand))]

        u[0] = 0  # Фиксируем потенциал первой строки
        checked_u[0] = 1

        while (0 in checked_u) or (0 in checked_v):
            # Вычисляем потенциалы для строк и столбцов
            for i in range(len(supply)):
                for j in range(len(demand)):
                    if result[i][j] > 0 and ((checked_u[i] == 1) and (checked_v[j] == 0)):
                        v[j] = result[i][j] - u[i]
                        checked_v[j] = 1
                    elif result[i][j] > 0 and ((checked_u[i] == 0) and (checked_v[j] == 1)):
                        u[i] = result[i][j] - v[j]
                        checked_u[i] = 1
        return u, v

    def check_optimal():
        u, v = calculate_potentials()
        for i in range(len(supply)):
            for j in range(len(demand)):
                if result[i][j] == 0 and C[i][j] < u[i] + v[j]:
                    return False
        return True

    return result, check_optimal()

# Входные данные
A = [15, 15, 15, 15]  # Предложение
B = [11, 11, 11, 11, 16]  # Спрос
C = [                 # Стоимости
    [17, 20, 29, 26, 25],
    [3, 4, 5, 15, 24],
    [19, 2, 22, 4, 13],
    [20, 27, 1, 17, 19]
]

# Решение задачи
result, optimal = transportation_problem_min_cost(A, B, C)

# Вывод результатов
print("Результат распределения:")
for row in result:
    print(row)

print("Решение оптимально" if optimal else "Решение не оптимально, необходима оптимизация плана")