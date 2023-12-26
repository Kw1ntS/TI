import heapq
from collections import defaultdict, Counter
import math
from prettytable import PrettyTable

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
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

# Проверяем выполнение неравенства Крафта-МакМиллана
def check_kraft_mcmillan(code_lengths):
    code_lengths = [int(length) for length in code_lengths]
    kraft_sum = sum(2**(-length) for length in code_lengths)
    return kraft_sum <= 1

# Рассчитываем энтропию текста
def calculate_entropy(data):
    probabilities = [count / float(len(data)) for count in Counter(data).values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

# Генерируем коды Хаффмана для входного текста
huffman_code = generate_huffman_code(input_text)
# Рассчитываем энтропию исходного текста
entropy_original = calculate_entropy(input_text)
# Рассчитываем среднюю длину кодовых слов
average_code_length = sum(len(huffman_code[symbol]) * input_text.count(symbol) for symbol in huffman_code) / len(input_text)
# Закодированный текст с использованием кодов Хаффмана
encoded_text_huffman = ''.join(huffman_code[symbol] for symbol in input_text)
# Рассчитываем энтропию закодированного текста
entropy_encoded_huffman = calculate_entropy(encoded_text_huffman)

# Создаем таблицу для отображения кодов Хаффмана
table = PrettyTable()
table.field_names = ["Символ", "Частота", "Код", "Длина кода"]
for symbol, code in huffman_code.items():
    table.add_row([symbol, input_text.count(symbol), code, len(code)])
print("\nКод Хаффмана")
print(table)

# Создаем таблицу с информацией о тексте и кодировании
table1 = PrettyTable()
table1.field_names = ["", "Энтропия исходного текста", "Средняя длина кодового слова", "Энтропия закодированного текста"]
table1.add_row(["Значение", entropy_original, average_code_length, entropy_encoded_huffman])

print(table1)

# Проверяем выполнение неравенства Крафта-МакМиллана
if check_kraft_mcmillan([len(code) for code in huffman_code.values()]):
    print("Неравенство Крафта-МакМиллана для Хаффмана выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Хаффмана не выполнено.")
