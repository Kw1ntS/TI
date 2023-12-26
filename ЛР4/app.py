import heapq
from collections import Counter
from prettytable import PrettyTable
import codecs

# Функция для чтения текста из файла
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Функция для вычисления коэффициента сжатия
def calculate_compression_ratio(original_size, compressed_size):
    return (1 - compressed_size / original_size) * 100

# Задаем путь к файлу
file_path = "sample3.txt"
# Считываем текст из файла
input_text = read_text_from_file(file_path)

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

# Создаем кодировщик адаптивного Хаффмана
adaptive_huffman_coder = codecs.getincrementalencoder('utf-8')()
# Кодируем текст адаптивным Хаффманом
adaptive_huffman_encoded_text = adaptive_huffman_coder.encode(input_text) + adaptive_huffman_coder.encode('', final=True)

# Вычисляем размеры исходного текста и сжатых текстов
original_size = len(input_text) * 8
huffman_compressed_size = len(''.join(generate_huffman_code(input_text).values()))
adaptive_huffman_compressed_size = len(adaptive_huffman_encoded_text)

# Вычисляем коэффициенты сжатия
huffman_compression_ratio = calculate_compression_ratio(original_size, huffman_compressed_size)
adaptive_huffman_compression_ratio = calculate_compression_ratio(original_size, adaptive_huffman_compressed_size)

# Создаем таблицу для вывода результатов
compression_table = PrettyTable()
compression_table.field_names = ["Размер исходного файла", "Коэффициент сжатия Хаффмана", "Коэффициент сжатия адаптивного Хаффмана"]
compression_table.add_row([original_size, f"{huffman_compression_ratio:.2f}%", f"{adaptive_huffman_compression_ratio:.2f}%"])

# Выводим результаты на экран
print("\nКоэффициенты сжатия:")
print(compression_table)
