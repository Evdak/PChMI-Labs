import asyncio
from pywebio.input import input
from pywebio.output import put_info, put_markdown, clear, put_error, put_success
from pywebio import start_server
import time
import json

import random

numbers_icons = {
    1: """
─╔╗─
╔╝║─
╚╗║─
─║║─
╔╝╚╗
╚══╝
""",
    2: """
╔═══╗
║╔═╗║
╚╝╔╝║
╔═╝╔╝
║║╚═╗
╚═══╝
""",
    3: """
╔═══╗
║╔═╗║
╚╝╔╝║
╔╗╚╗║
║╚═╝║
╚═══╝
""",
    4: """
╔╗─╔╗
║║─║║
║╚═╝║
╚══╗║
───║║
───╚╝
""",
    5: """
╔═══╗
║╔══╝
║╚══╗
╚══╗║
╔══╝║
╚═══╝
""",
    6: """
╔═══╗
║╔══╝
║╚══╗
║╔═╗║
║╚═╝║
╚═══╝
""",
    7: """
╔═══╗
║╔═╗║
╚╝╔╝║
──║╔╝
──║║─
──╚╝─
""",
    8: """
╔═══╗
║╔═╗║
║╚═╝║
║╔═╗║
║╚═╝║
╚═══╝
""",
    9: """
╔═══╗
║╔═╗║
║╚═╝║
╚══╗║
╔══╝║
╚═══╝
""",
    0: """
╔═══╗
║╔═╗║
║║║║║
║║║║║
║╚═╝║
╚═══╝
"""
}


async def analyze_answer(numbers, numbers_guessed, type):
    if type == "numbers":
        return [
            {
                "number": num,
                "size": 7 - numbers.index(num)
            } for num in numbers_guessed if num in numbers
        ]
    elif type == "pictures":
        return [
            {
                "number": num,
                "size": "default" if numbers.index(num) % 2 == 0 else "picture"
            } for num in numbers_guessed if num in numbers
        ]


async def print_nums(numbers, numberscopy, type):
    if type == "numbers":
        for number in numberscopy:
            put_markdown(f"{'#' * numbers.index(number)} {number}")
            await asyncio.sleep(1)
            clear()
    elif type == "pictures":
        for number in numberscopy:
            if numbers.index(number) % 2 == 0:
                put_markdown(f"# {number}")
            else:
                put_markdown(f"{numbers_icons[number]}")
            await asyncio.sleep(1)
            clear()


async def number_guessing(name, type):

    numbers, numberscopy = await generate_numbers(type)

    put_info("Через 8 секунд вам поочередно будут показаны 6 чисел (по 1 секунде на каждое), постарайтесь их запомнить. После этого вам нужно будет ввести числа, которые вы запомните")
    await asyncio.sleep(8)
    clear()

    await print_nums(numbers, numberscopy, type)
    while True:
        try:
            numbers_guessed: str = await input(
                "Введите числа, которые вы запомнили через пробел: ")
            numbers_guessed = map(int, numbers_guessed.split())
            clear()
            break
        except:
            clear()
            put_error("Что-то пошло не так, попробуйте еще раз")

    numbers_guessed = await analyze_answer(numbers, numbers_guessed, type)
    await save_results(name, numbers_guessed, type)


async def generate_numbers(type):
    numbers = []
    if type == "numbers":
        for _ in range(6):
            num = random.randint(10, 99)
            while num in numbers:
                num = random.randint(10, 99)
            numbers.append(num)
    elif type == "pictures":
        for _ in range(6):
            num = random.randint(0, 9)
            while num in numbers:
                num = random.randint(0, 9)
            numbers.append(num)
    numberscopy = numbers.copy()
    random.shuffle(numberscopy)
    return numbers, numberscopy


async def save_results(name, numbers_guessed, type):
    if type == "numbers":
        path = "laba1/resultsNum.json"
    elif type == "pictures":
        path = "laba1/resultsPic.json"

    with open(path) as f:
        results = json.load(f)

    with open(path, "w") as write_file:
        results.append({
            "name": name,
            "numbersGuessed": numbers_guessed
        })
        json.dump(results, write_file)


async def show_results():
    path1 = "laba1/resultsNum.json"
    path2 = "laba1/resultsPic.json"

    with open(path1) as f:
        results1 = json.load(f)
        results1 = json.dumps(results1, indent=4)

    with open(path2) as f:
        results2 = json.load(f)
        results2 = json.dumps(results2, indent=4)

    clear()
    put_markdown(
        fr"""
# numbers:
    {results1}
        
        
# pictures:
    {results2}"""
    )


async def main():
    name: str = await input("Введите имя：")
    if name.lower() == "admin":
        await show_results()
    else:
        await number_guessing(name, "numbers")
        await number_guessing(name, "pictures")
        clear()
        put_success('Спасибо за прохождение опроса')
