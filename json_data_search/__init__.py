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


# def query_execute(path, clean_query):
#     with open(path, 'r') as f:
#         data = json.load(f)
#     try:
#         for elem in clean_query:
#             data = data[elem]
#     except KeyError:
#         print("File don't have such key")
#         logging.info(f"File don't have such key: {elem}")
#         exit(-1)
#     json_str = clean_query[-1] + ': ' + json.dumps(data, indent="   ")
#     json_list = json_str.split('\n')
#     response = ''
#     for n, line in enumerate(json_list, start=1):
#         response += str(n) + ': ' + line + '\n'
#     return response


# def query_parsing(console_query):
#     return console_query[1:-1].split(':')


def json_file_parser(path, query):
    with open(path, 'r') as f:
        file = f.read()
    # print(file)
    query_in_file_pos = [i for i in range(len(file)) if file.startswith(query, i)]  # номера вхождения подстроки
    for sub_str_count in query_in_file_pos:
        print(f"{get_parent(file, sub_str_count)}: string count: {get_str_count(file, sub_str_count)} fullname: {get_substr(file, sub_str_count)}")


def get_parent(file, substr_pos):
    prev_sym = ''
    parent_found = False
    parent = ''
    for i in range(substr_pos, 0, -1):
        bracket_count = 0
        if file[i] == '{' or file[i] == '[':
            bracket_count += 1
        elif file[i] == '}' or file[i] == ']':
            bracket_count -= 1
        if file[i] == ':' and (prev_sym == '[' or prev_sym == '{') and bracket_count == 0:
            parent_found = True
        elif parent_found and not file[i-1].isalnum():
            parent = file[i] + parent
            break
        elif parent_found:
            parent = file[i] + parent
        if file[i] != ' ':
            prev_sym = file[i]
    return parent.replace('"', '')


def get_str_count(file, substr_pos):
    count = 1
    for i in range(substr_pos):
        if file[i] == '\n':
            count += 1
    return count


def get_substr(file, substr_pos):
    i = 0
    substr = ''
    while True:
        if not file[substr_pos+i].isalnum():
            break
        substr += file[substr_pos+i]
        i += 1
    return substr


def main():
    FORMAT = '%(asctime)-15s %(message)s'
    log_file_name = "/home/comazzo/PycharmProjects/exam_python/exam.log"
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format=FORMAT)

    args_dict = arguments_parsing()
    # query_execute(args_dict["path"], query_parsing(args_dict["query"]))
    json_file_parser(args_dict["path"],args_dict["query"])
    logging.info(f"Query completed successfully")
