import time
import os
import sys

class basic:
    def __init__(self,sys_functions:dict):
        self.filename = "opened.txt"
        self.opened_file = open(self.filename,"r",encoding="utf-8")

        self.sys_functions = sys_functions

        self.functions  = {}

        self.variables = {}

    def get_bool(self,expression:str):
        words = expression.split(" ")
        result = ""
        for word in words:
            if self.get_type(word) == "var":
                type_var = type(self.variables[word[1::]])
                if type_var == str:
                    result += "'"
                    result += str(self.variables[word[1::]])
                    result += "'"
                elif type_var == int:
                    result += str(self.variables[word[1::]])
                continue
            result += str(word)
        return bool(eval(result))
    def get_type(self,var:str):
        if var[0] == "'" and var[-1] == "'":
            return str
        elif var[0] == "#":
            return int
        elif var[0] == "[" and var[-1] == "]":
            return list
        elif var[0] == "@":
            return "var"
        else:
            return None
    def init_list(self,name,data:list):
        for i, element in enumerate(data):
            type = self.get_type(element)
            if type == str:
                text = element[1::]
                text = text[:-1]
                data[i] = str(text)
                continue
            elif type == int:
                data[i] = int(element)
                continue
        self.variables[name] = data
    def execute(self,line:str,ii:int,name_space:dict,task:dict):
        try:
            self.variables = name_space
            word = line.split(" ")[0]
            args = line.split(" ")
            args = args[1::]
            text = ""
            for i in range(len(args)):
                text += args[i]
                if i+1 != len(args):
                    text += " "

            if word.isspace():
                return
            if word == "":
                return
            if word[0] == "#":
                return
            if word == "PRINT":
                print(text)
            elif word == "INT":
                self.variables[args[0]] = int(args[1])
            elif word == "STR":
                self.variables[args[0]] = str(args[1])
            elif word == "LIST":
                data = args[1::]
                self.init_list(args[0],data)
            elif word == "LET":
                var = ""
                arg2 = args[1::]
                for i,part in enumerate(arg2):
                    var += part
                    if i+1 != len(arg2):
                        var += " "
                typee = self.get_type(var)
                if typee == str:
                    text = var[1::]
                    text = text[:-1]
                    self.variables[args[0]] = str(text)
                elif typee == int:
                    var = var[1::]
                    self.variables[args[0]] = int(var)
                elif typee == list:
                    data = var[1::]
                    data = data[:-1]
                    data = data.split(",")
                    self.init_list(args[0],data)
                elif typee == None:
                    self.variables[args[0]] = None
            elif word == "PRINTVAR":
                print(self.variables[args[0]])
            elif word == "CLEAR":
                os.system("clear")
            elif word == "INPUT":
                self.variables[args[0]] = str(input(args[1]))
            elif word == "END":
                print("Программа успешно выполнена, код 0")
                exit(0)
            elif word == "LINES":
                self.variables[args[0]] = self.variables["LINES"]
            elif word == "TYPE":
                self.variables[args[1]] = str(type(self.variables[args[0]]))
            elif word == "SYSTEM":
                os.system(text)
            elif word == "OPEN":
                self.opened_file = open(args[0],args[1],encoding=args[2])
            elif word == "READ":
                self.variables[args[0]] = self.opened_file.read()
            elif word == "WRITE":
                self.opened_file.write(self.variables[args[0]])
            elif word == "CLOSE":
                self.opened_file.close()
                self.opened_file = open(self.filename,"r",encoding="utf-8")
            elif word == "IF":
                expression = line.split("/")[1]
                expression_bool = self.get_bool(expression)
                actions = line.split(":")[1]
                actions_lines = actions.split(",")
                if expression_bool:
                    for action in actions_lines:
                        self.execute(action,ii,self.variables,task)
            elif word == "FOR":
                i = line.split("|")[1]
                i = eval(i)
                actions = line.split(":")[1]
                actions_lines = actions.split(";")
                for i in range(i):
                    for action in actions_lines:
                        self.execute(action,ii,self.variables,task)
                        self.variables["i"] += 1
                self.variables["i"] = 0
                self.variables["i"] = 0
            elif word == "ADD":
                self.variables[args[0]] += int(args[1])
            elif word == "SUB":
                self.variables[args[0]] -= int(args[1])
            elif word == "MULT":
                res = self.variables[args[0]] * int(args[1])
                self.variables[args[0]] = res
            elif word == "DIV":
                res = self.variables[args[0]] // int(args[1])
                self.variables[args[0]] = res
            elif word == "DEF":
                name = line.split("<")[1]
                name = name.split(">")[0]
                actions = line.split("::")[1]
                actions_lines = actions.split(";;")
                self.functions[name] = actions_lines
            elif word == "CALL":
                for action in self.functions[args[0]]:
                    self.execute(action,ii,self.variables,task)
            elif word == "sleep_task":
                self.sys_functions[word](int(args[0]))
            elif word == "un_sleep_task":
                self.sys_functions[word](int(args[0]))
            elif word == "close_task":
                self.sys_functions[word](int(args[0]))
            elif word == "change_2_task":
                self.sys_functions[word](int(args[0]),int(args[0]))
            elif word == "stop":
                self.sys_functions[word]()
            elif word == "error":
                self.sys_functions[word](str(args[0]))
            elif word == "create_task":
                self.sys_functions[word](str(args[0]),str(args[1]))
            else:
                print(f"Неизвестное слово {word} ,строка {ii}")
                exit(1)

        except Exception as e:
            self.sys_functions["error"](f"Ошибка {e} ,строка {ii}")
            return


start_time = time.time()
def search_blocks(lines):
    """
    Автоматически определяет и объединяет строки в блоки кода
    перед выполнением через exec()
    """
    blocks = []  # Список блоков кода для выполнения
    current_block = []  # Текущий собираемый блок
    expected_indent = 0  # Ожидаемый уровень отступа для следующей строки

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Пропускаем пустые строки и комментарии
        if not stripped or stripped.startswith('#'):
            continue

        # Определяем текущий уровень отступа
        current_indent = len(line) - len(line.lstrip())

        # Если это начало нового блока (двоеточие в конце)
        if stripped.endswith(':') and not current_block:
            current_block.append(line)
            expected_indent = current_indent + 4
            continue

        # Если это продолжение текущего блока
        if current_block and current_indent >= expected_indent:
            current_block.append(line)
            # Обновляем expected_indent если нашли вложенный блок
            if stripped.endswith(':'):
                expected_indent = current_indent + 4
            continue

        # Если текущий блок закончен, сохраняем его
        if current_block:
            blocks.append("\n".join(current_block))
            current_block = []
            expected_indent = 0

        # Если это одиночная команда
        if not stripped.endswith(':'):
            blocks.append(line)
        else:
            # Начало нового блока
            current_block.append(line)
            expected_indent = current_indent + 4

    # Добавляем последний блок если есть
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks

def sys_time():
    return int(time.time()-int(start_time))

class kernel:
    def __init__(self):
        self.sleep_task_example = {
            "name":"-----",
            "blocks":["pass"],
            "time":sys_time(),
            "counter":0,
        }

        self.sys_functions = {
            "create_task": self.create_task,
            "close_task": self.close_task,
            "sleep_task": self.sleep_task,
            "un_sleep_task": self.un_sleep_task,
            "change_2_tasks": self.change_2_tasks,
            "stop": self.stop,
            "error": self.error,
        }

        self.run = True

        self.interpriteter = basic(self.sys_functions)

        self.virtual_name_space = {}
        self.task_stack = []
        self.task_sleep = []
        for i in range(20):
            self.task_sleep.append(self.sleep_task_example)
    def create_task(self,name:str,path:str):
        with open(path,"r",encoding="utf-8") as file:
            code = file.read()
            file.close()
        lines = code.split("\n")
        blocks = search_blocks(lines)
        task = {
            "name":name,
            "blocks":blocks,
            "time":sys_time(),
            "name_space":{"i":-1},
            "counter":0,
        }
        self.task_stack.append(task)
    def close_task(self,i):
        self.task_stack.pop(i)
    def sleep_task(self,i):
        if i >= 20:
            return
        self.task_sleep[i] = self.task_stack[i]
        self.task_stack.pop(i)
    def un_sleep_task(self,i):
        if i >= 20:
            return
        self.task_stack.append(self.task_sleep[i])
        self.task_sleep[i] = self.sleep_task_example
    def stop(self):
        print("Stoping the kernel...")
        self.run = False
    def error(self,text:str):
        print(text)
    def change_2_tasks(self,i_1,i_2):
        task1 = self.task_stack[i_1]
        task2 = self.task_stack[i_2]
        self.task_stack[i_1] = task2
        self.task_stack[i_2] = task1
    def start_user_tasks(self):
        while self.run:
            if self.task_stack == []:
                self.stop()
                continue
            task = self.task_stack[0]
            try:
                self.interpriteter.execute(task["blocks"][task["counter"]],task["counter"],task["name_space"],task)
            except Exception as e:
                self.error(f"Error in task {task["name"]}, in block {task["blocks"][task["counter"]]} -- {e}")
            if task["counter"] < len(task["blocks"])-1:
                task["counter"] += 1
            else:
                self.close_task(0)


Kernel = kernel()
Kernel.create_task("terminal","terminal.bsl")
Kernel.start_user_tasks()

