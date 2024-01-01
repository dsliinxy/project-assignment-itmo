try:
    with open('employees.txt', 'r', encoding='utf-8') as employees_file:
        lines1 = employees_file.readlines()
except (FileNotFoundError, IOError):
    print("Ошибка при открытии или чтении файла.")

employees = []
def employees_foo(lines1):
    """
    Функция обрабатывает список строк и возвращает список словарей с информацией о сотрудниках.
    :param lines1: список исходных значений в файле employees
    :return: список словарей с данными о работниках
    """
    for line in lines1:
        values = line.split()
        fio = []
        technologies = []
        num = [0] # Счетчик для индексов

        for value in values: # Проверка каждого слова
            if value != 'junior' and value != 'middle' and value != 'senior':
                fio.append(value)
                num[0] += 1
            else:
                level = value
                num[0] += 1
                break

        fio_str = ' '.join(fio) # Строчный тип для ФИО
        num1 = num[0] # Берем последнее значение индекса и с помощью срезов читаем список до конца
        technologies = values[num1:]

        employees.append({
            'ФИО': fio_str,
            'Уровень': level,
            'Технологии': technologies
        })
    return employees
employees_foo(lines1)

try:
    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        lines2 = tasks_file.readlines()
except (FileNotFoundError, IOError):
    print("Ошибка при открытии или чтении файла.")

tasks = []
def tasks_foo(lines2):
    """
    Функция обрабатывает список строк и возвращает список словарей с информацией о задачах.
    :param lines2: список исходных значений в файле tasks
    :return: список словарей с данными о задачах
    """
    for line in lines2:
        values = line.split()
        task_name = []
        technologies_name = []
        num = [0]

        for value in values: # Схема такая же, как и в первой функции
            if value != 'junior' and value != 'middle' and value != 'senior':
                task_name.append(value)
                num[0] += 1
            else:
                level = value
                num[0] += 1
                break

        task_name_str = ' '.join(task_name)
        num1 = num[0]
        technologies_name = values[num1:-1]
        time = values[-1]

        tasks.append({
            'Имя задачи': task_name_str,
            'Уровень': level,
            'Технологии': technologies_name,
            'Время': time
        })
    return tasks
tasks_foo(lines2)

employee_plans = {}
unassigned_tasks = []
def assign_tasks(employees, tasks):
    """
    Функция распределяет задачи между сотрудниками и возвращает словарь с планами сотрудников и список нераспределенных задач.
    :param employees: список словарей с данными о сотрудниках
    :param tasks: список словарей с данными о задачах
    :return: кортеж с распределенными и нераспределенными задачами
    """
    for task in tasks:
        task_assigned = False
        for employee in employees: # Проходим по каждому сотруднику и проверяем, может ли он решить задачу
            if employee["Уровень"] >= task["Уровень"] and all(tech in employee["Технологии"] for tech in task["Технологии"]):
                if employee["ФИО"] not in employee_plans: # Сотрудник может решить эту задачу
                    employee_plans[employee["ФИО"]] = []
                employee_plans[employee["ФИО"]].append(task)
                task_assigned = True
                break # Если не может - переходим к следующему сотруднику
        if not task_assigned: # Никто не может решить задачу
            unassigned_tasks.append(task)
    return employee_plans, unassigned_tasks
assign_tasks(employees, tasks)

with open("plans.txt", "w", encoding="utf-8") as file:
    for employee, employee_tasks in sorted(employee_plans.items()):
        file.write(f"{employee} - {sum(int(task['Время']) for task in employee_tasks)}\n")
        for index, task in enumerate(employee_tasks, start=1): # Нумерация с 1
            file.write(f"{index}. {task['Имя задачи']} - {task['Время']}\n")
        file.write("\n")

    if unassigned_tasks:
        file.write("Задачи, которые никто не может решить:\n")
        for idx, task in enumerate(unassigned_tasks, start=1):
            file.write(f"{idx}. {task['Имя задачи']} - {task['Уровень']} {' '.join(task['Технологии'])} {task['Время']}\n")
        file.write("\n")