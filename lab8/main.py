import random
from tqdm import tqdm


def generate_interarrival_time():
    return random.uniform(2, 4)  # Средний интервал поступления 3 ± 1 минуты


def generate_processing_time(machine):
    if machine == 1:
        return random.uniform(3, 5)  # T1 = 4 ± 1 мин
    elif machine == 2:
        return random.uniform(2, 4)  # T2 = 3 ± 1 мин
    elif machine == 3:
        return random.uniform(3, 7)  # T3 = 5 ± 2 мин


def simulate_system(task_count):
    queues = {1: [], 2: [], 3: []}  # Очереди перед ЭВМ
    tasks_processed = {1: 0, 2: 0, 3: 0}  # Обработанные задания

    current_time = 0
    next_arrival = generate_interarrival_time()

    processing_times = {1: 0, 2: 0, 3: 0}  # Время завершения обработки для каждой ЭВМ
    avg_queue = {1: 0, 2: 0, 3: 0}

    tasks_left = task_count

    while sum(tasks_processed.values()) - tasks_processed[1] < task_count:
        # Поступление задания
        if current_time >= next_arrival and tasks_left > 0:
            destination = random.choices([1, 2, 3], weights=[0.4, 0.3, 0.3])[0]
            queues[destination].append(current_time)
            next_arrival = current_time + generate_interarrival_time()
            tasks_left -= 1

        # Обработка на первой ЭВМ
        if queues[1] and current_time >= processing_times[1]:
            processing_times[1] = current_time + generate_processing_time(1)
            queues[1].pop(0)

            if random.random() < 0.3:  # 30% идет ко второй ЭВМ
                queues[2].append(processing_times[1])
            else:  # 70% идет к третьей ЭВМ
                queues[3].append(processing_times[1])

            tasks_processed[1] += 1

        # Обработка на второй ЭВМ
        if queues[2] and current_time >= processing_times[2]:
            processing_times[2] = current_time + generate_processing_time(2)
            queues[2].pop(0)
            tasks_processed[2] += 1

        # Обработка на третьей ЭВМ
        if queues[3] and current_time >= processing_times[3]:
            processing_times[3] = current_time + generate_processing_time(3)
            queues[3].pop(0)
            tasks_processed[3] += 1

        for i in range(1, 4):
            avg_queue[i] += len(queues[i])
        
        current_time += TIME_STEP  # Шаг времени для моделирования

    for i in range(1, 4):
        avg_queue[i] /= (current_time * (1/TIME_STEP))

    return tasks_processed, avg_queue, current_time
        
def test_simulations(tests, task_count):
    time_ratios = {1: 0, 2: 0, 3: 0}
    queue_ratios = {1: 0, 2: 0, 3: 0}
    avg_time = 0
    
    for i in tqdm(range(tests), desc="Проведение симуляций", ncols=100):
        tasks, queues, time = simulate_system(task_count)
        total_tasks = sum(task_count for task_count in tasks.values())
        total_avg_queues = sum(avg_queue for avg_queue in queues.values())
        
        for j in range(1, 4):
            time_ratios[j] += tasks[j] / total_tasks
            queue_ratios[j] += queues[j] / total_avg_queues 
            avg_time += time
    
    # Расчет средних значений
    for i in range(1, 4):
        time_ratios[i] /= tests
        queue_ratios[i] /= tests
    
    avg_time /= tests

    return time_ratios, queue_ratios, avg_time


print("Симуляция работы системы массового обслуживания")
TIME_STEP = 0.01
TASK_COUNT = None

while True:
    print("\n----Меню----")
    user_input = int(input("Введите номер команды:\n1 - Выбор количества заданий\n2 - Начать моделирование\n3 - Провести комплекс симуляций\n4 - Выход\nНомер: "))
    
    print()

    match user_input:
        case 1: 
            TASK_COUNT = int(input("Введите количество заданий: "))
        case 2:
            if TASK_COUNT is None:
                print("Сначала введите количество заданий")
                continue

            tasks, queues, time = simulate_system(TASK_COUNT)

            print("\n----Результаты моделирования----")
            for i in range(1, 4):
                print(f"ЭВМ №{i}")
                print(f"Заданий обработано: {tasks[i]}")
                print(f"Средняя длина очереди: {queues[i]:.4f}")
                print("------------")
            print(f"Все задания обработаны за {time:.1f} мин")
            print(f"Процессов обработки выполнено: {sum(task_count for task_count in tasks.values())}")
        case 3:
            tests_num = int(input("Введите количество симуляций: "))
            tr, qr, at = test_simulations(tests_num, TASK_COUNT)
            print("----Результаты симуляций----")
            print(f"Всего симуляций: {tests_num}")
            print(f"Заданий в одной симуляции: {TASK_COUNT}")
            for i in range(1, 4):
                print("------------")
                print(f"ЭВМ №{i}:")
                print(f"Средняя доля выполненных заданий: {tr[i]*100:.2f}%")
                print(f"Средняя доля длины очереди: {qr[i]*100:.2f}%")
                print("------------")
            print(f"Среднее время выполнения всех заданий: {at:.2f} мин")
            print(f"Среднее время нахождения задания в системе: {at/TASK_COUNT:.2f} мин")
        case 4:
            print("Выход")
            break
        case _:
            print("Неверный ввод")
        
        