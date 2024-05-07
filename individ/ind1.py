#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys

def display_flights(flights):
    """
    Отобразить список рейсов.
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print('| {:^30} | {:^20} | {:^15} |'.format(
            "Название пункта назначения",
            "Номер рейса",
            "Тип самолета"
        ))
        print(line)

        for idx, flight in enumerate(flights, 1):
            print('| {:<30} | {:<20} | {:<15} |'.format(
                flight.get('название пункта назначения', ''),
                flight.get('номер рейса', ''),
                flight.get('тип самолета', '')
            ))
        print(line)

    else:
        print("Список рейсов пуст.")

def add_flight(flights, destination, flight_number, aircraft_type):
    """
    Добавить данные о рейсе.
    """
    flights.append(
        {
            "название пункта назначения": destination,
            "номер рейса": flight_number,
            "тип самолета": aircraft_type
        }
    )
    return flights

def save_flights(file_name, flights):
    """
    Сохранить рейсы в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)

def load_flights(file_name):
    """
    Загрузить рейсы из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)

def search_flights_by_destination(flights, destination):
    """
    Выбрать рейсы по пункту назначения.
    """
    matching_flights = [flight for flight in flights if flight['название пункта назначения'] == destination]
    return matching_flights

def main():
    os.environ.setdefault("FLIGHTS_DATA", "flights.json")

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--filename",
        action="store",
        help="Имя файла данных"
    )

    parser = argparse.ArgumentParser("flight_manager")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавить новый рейс"
    )
    add_parser.add_argument(
        "-d", "--destination",
        action="store",
        required=True,
        help="Пункт назначения"
    )
    add_parser.add_argument(
        "-n", "--number",
        action="store",
        required=True,
        help="Номер рейса"
    )
    add_parser.add_argument(
        "-t", "--type",
        action="store",
        required=True,
        help="Тип самолета"
    )

    display_parser = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Отобразить все рейсы"
    )

    search_parser = subparsers.add_parser(
        "search",
        parents=[file_parser],
        help="Выбрать рейсы по пункту назначения"
    )
    search_parser.add_argument(
        "-d", "--destination",
        action="store",
        required=True,
        help="Пункт назначения"
    )

    args = parser.parse_args()
    data_file = args.filename
    if not data_file:
        data_file = os.environ.get("FLIGHTS_DATA")
    if not data_file:
        print("Отсутствует имя файла данных", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        flights = load_flights(data_file)
    else:
        flights = []

    if args.command == "add":
        flights = add_flight(
            flights,
            args.destination,
            args.number,
            args.type
        )
        is_dirty = True

    elif args.command == "display":
        display_flights(flights)

    elif args.command == "search":
        selected_flights = search_flights_by_destination(flights, args.destination)
        display_flights(selected_flights)

    if is_dirty:
        save_flights(data_file, flights)

if __name__ == "__main__":
    main()
