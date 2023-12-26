# Импортируем необходимые библиотеки
import heapq
from collections import defaultdict, Counter
import math
from prettytable import PrettyTable

# Функция для чтения текста из файла
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Функция для расчета коэффициента сжатия
def calculate_compression_ratio(original_size, compressed_size):
    return (1 - compressed_size / original_size) * 100

# Задаем путь к файлу
file_path = "sample3.txt"

# Считываем текст из файла
input_text = read_text_from_file(file_path)

# Переопределяем Counter для подсчета частоты символов в тексте
def Counter(iterable):
    counter_dict = defaultdict(int)
    for element in iterable:
        counter_dict[element] += 1
    return counter_dict

# Строим дерево Шеннона
def build_shannon_tree(data):
    data_probabilities = {symbol: count / float(len(data)) for symbol, count in Counter(data).items()}
    sorted_symbols = sorted(data_probabilities, key=data_probabilities.get, reverse=True) 
    def build_tree(symbols):
        if len(symbols) == 1:
            return {symbols[0]: '0'}
        split = len(symbols) // 2
        left_tree = build_tree(symbols[:split])
        right_tree = build_tree(symbols[split:])
        for symbol in left_tree:
            left_tree[symbol] = '0' + left_tree[symbol]
        for symbol in right_tree:
            right_tree[symbol] = '1' + right_tree[symbol]
        return {**left_tree, **right_tree}    
    return build_tree(sorted_symbols)

# Строим дерево Фано
def build_fano_tree(data):
    if len(data) == 1:
        return {data[0][0]: '0'}
    data.sort(key=lambda x: x[0], reverse=True)
    mid = len(data) // 2
    left = data[:mid]
    right = data[mid:]
    fano_tree = {}
    for symbol, code in build_fano_tree(left).items():
        fano_tree[symbol] = '0' + code
    for symbol, code in build_fano_tree(right).items():
        fano_tree[symbol] = '1' + code
    return fano_tree

# Генерируем коды Фано
def generate_fano_code(data):
    tree = build_fano_tree(data)
    return tree

# Рассчитываем энтропию текста
def calculate_entropy(data):
    probabilities = [count / float(len(data)) for count in Counter(data).values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

# Проверяем неравенство Крафта-МакМиллана
def check_kraft_mcmillan(code_lengths):
    code_lengths = [int(length) for length in code_lengths]
    kraft_sum = sum(2**(-length) for length in code_lengths)
    return kraft_sum <= 1

# Строим дерево Хаффмана
def build_huffman_tree(data):
    heap = [[weight, [symbol, ""]] for symbol, weight in Counter(data).items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return heap[0][1:]

# Генерируем коды Хаффмана
def generate_huffman_code(data):
    tree = build_huffman_tree(data)
    return {symbol: code for symbol, code in tree}

# Генерируем коды Фано для входного текста
fano_code = generate_fano_code([[symbol, input_text.count(symbol)] for symbol in set(input_text)])

# Генерируем коды Шеннона для входного текста
shannon_code = build_shannon_tree(input_text)

# Рассчитываем энтропию исходного текста
entropy_original = calculate_entropy(input_text)

# Рассчитываем среднюю длину кодовых слов для Шеннона и Фано
average_code_length_shannon = sum(len(shannon_code[symbol]) * input_text.count(symbol) for symbol in shannon_code) / len(input_text)
average_code_length_fano = sum(len(fano_code[symbol]) * input_text.count(symbol) for symbol in fano_code) / len(input_text)

# Кодируем текст используя Шеннона и Фано
encoded_text_shannon = ''.join(shannon_code[symbol] for symbol in input_text)
encoded_text_fano = ''.join(fano_code[symbol] for symbol in input_text)

# Рассчитываем энтропию закодированного текста для Шеннона и Фано
entropy_encoded_shannon = calculate_entropy(encoded_text_shannon)
entropy_encoded_fano = calculate_entropy(encoded_text_fano)

# Генерируем коды Хаффмана для входного текста
huffman_code = generate_huffman_code(input_text)

# Рассчитываем энтропию исходного текста
entropy_original = calculate_entropy(input_text)

# Рассчитываем среднюю длину кодовых слов для Хаффмана
average_code_length_huffman = sum(len(huffman_code[symbol]) * input_text.count(symbol) for symbol in huffman_code) / len(input_text)

# Кодируем текст используя Хаффмана
encoded_text_huffman = ''.join(huffman_code[symbol] for symbol in input_text)

# Рассчитываем энтропию закодированного текста для Хаффмана
entropy_encoded_huffman = calculate_entropy(encoded_text_huffman)

# Выводим таблицы с результатами
table_shannon_fano = PrettyTable()
table_shannon_fano.field_names = ["Symbol", "Frequency", "Code", "Code Length"]
for symbol, code in shannon_code.items():
    table_shannon_fano.add_row([symbol, input_text.count(symbol), code, len(code)])
print("\nШеннон код:")
print(table_shannon_fano)

table = PrettyTable()
table.field_names = ["Symbol", "Frequency", "Code", "Code Length"]
for symbol, code in fano_code.items():
    table.add_row([symbol, input_text.count(symbol), code, len(code)])
print("\nКод Фано:")
print(table)

table1 = PrettyTable()
table1.field_names = ["", "Энтропия исходного текста", "Средняя длина кодового слова", "Энтропия закодированного текста"]
table1.add_row(["Значение", entropy_original, average_code_length_fano, entropy_encoded_fano])
print("\nФано:")
print(table1)

table2 = PrettyTable()
table2.field_names = ["", "Энтропия исходного текста", "Средняя длина кодового слова", "Энтропия закодированного текста"]
table2.add_row(["Значение", entropy_original, average_code_length_shannon, entropy_encoded_shannon])
print("\nШеннон:")
print(table2)

table3 = PrettyTable()
table3.field_names = ["","Энтропия исходного текста", "Средняя длина кодового слова Хаффмана", "Средняя длина кодового слова Фано", "Средняя длина кодового слова Шеннона",]
table3.add_row(["Значение", entropy_original, average_code_length_huffman, average_code_length_fano, average_code_length_shannon])

print(table3)

# Проверяем неравенство Крафта-МакМиллана для Шеннона и Фано
if check_kraft_mcmillan([len(code) for code in shannon_code.values()]):
    print("Неравенство Крафта-МакМиллана для Шеннона выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Шеннона не выполнено.")

if check_kraft_mcmillan([len(code) for code in fano_code.values()]):
    print("Неравенство Крафта-МакМиллана для Фано выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Фано не выполнено.")
