import json

import configargparse
import logging


"""
Используя package configargparse напишите cli инструмент для поиска данных внутри json файлов 
< program > --path < путь до json > [query] 
вывод 
родитель: номер строки что нашел (может быть несколько)
"""


def arguments_parsing():
    p = configargparse.ArgParser()
    p.add('--path', required=True, help='JSON file path')
    p.add('query', help='JSON query. Example: [parent:child:child_1]')
    response = vars(p.parse_args())
    logging.info(f'CL Args:\n\tJSON file path: {response["path"]},\n\tJSON query: {response["query"]}')
    return response


def query_execute(path, clean_query):
    with open(path, 'r') as f:
        data = json.load(f)
    try:
        for elem in clean_query:
            data = data[elem]
    except KeyError:
        print("File don't have such key")
        logging.info(f"File don't have such key: {elem}")
        exit(-1)
    json_str = clean_query[-1] + ': ' + json.dumps(data, indent="   ")
    json_list = json_str.split('\n')
    response = ''
    for n, line in enumerate(json_list, start=1):
        response += str(n) + ': ' + line + '\n'
    return response


def query_parsing(console_query):
    return console_query[1:-1].split(':')


def main():
    FORMAT = '%(asctime)-15s %(message)s'
    log_file_name = "/home/comazzo/PycharmProjects/exam/exam.log"
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format=FORMAT)

    args_dict = arguments_parsing()
    print(query_execute(args_dict["path"], query_parsing(args_dict["query"])))
    logging.info(f"Query completed successfully")
