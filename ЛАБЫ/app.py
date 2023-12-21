import heapq
from collections import defaultdict, Counter
import math
from prettytable import PrettyTable
import codecs
from tabulate import tabulate

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_compression_ratio(original_size, compressed_size):
    return (1 - compressed_size / original_size) * 100

file_path = "sample3.txt"
input_text = read_text_from_file(file_path)

def Counter(iterable):
    counter_dict = defaultdict(int)
    for element in iterable:
        counter_dict[element] += 1
    return counter_dict

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

def generate_fano_code(data):
    tree = build_fano_tree(data)
    return tree

def generate_huffman_code(data):
    tree = build_huffman_tree(data)
    return {symbol: code for symbol, code in tree}

def calculate_entropy(data):
    probabilities = [count / float(len(data)) for count in Counter(data).values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def check_kraft_mcmillan(code_lengths):
    code_lengths = [int(length) for length in code_lengths]
    kraft_sum = sum(2**(-length) for length in code_lengths)
    return kraft_sum <= 1

fano_code = generate_fano_code([[symbol, input_text.count(symbol)] for symbol in set(input_text)])
shannon_code = build_shannon_tree(input_text)
huffman_code = generate_huffman_code(input_text)

table = PrettyTable()
table.field_names = ["Symbol", "Frequency", "Code", "Code Length"]
for symbol, code in huffman_code.items():
    table.add_row([symbol, input_text.count(symbol), code, len(code)])
print("\nКод Хаффмана")
print(table)
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

if check_kraft_mcmillan([len(code) for code in huffman_code.values()]):
    print("Неравенство Крафта-МакМиллана для Хаффмана выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Хаффмана не выполнено.")
if check_kraft_mcmillan([len(code) for code in shannon_code.values()]):
    print("Неравенство Крафта-МакМиллана для Шеннона выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Шеннона не выполнено.")
if check_kraft_mcmillan([len(code) for code in fano_code.values()]):
    print("Неравенство Крафта-МакМиллана для Фано выполнено.")
else:
    print("Неравенство Крафта-МакМиллана для Фано не выполнено.")

entropy_original = calculate_entropy(input_text)
average_code_length = sum(len(huffman_code[symbol]) * input_text.count(symbol) for symbol in huffman_code) / len(input_text)
average_code_length_shannon = sum(len(shannon_code[symbol]) * input_text.count(symbol) for symbol in shannon_code) / len(input_text)
average_code_length_fano = sum(len(fano_code[symbol]) * input_text.count(symbol) for symbol in fano_code) / len(input_text)

encoded_text_huffman = ''.join(huffman_code[symbol] for symbol in input_text)
encoded_text_shannon = ''.join(shannon_code[symbol] for symbol in input_text)
encoded_text_fano = ''.join(fano_code[symbol] for symbol in input_text)

entropy_encoded_huffman = calculate_entropy(encoded_text_huffman)
entropy_encoded_shannon = calculate_entropy(encoded_text_shannon)
entropy_encoded_fano = calculate_entropy(encoded_text_fano)

print(f"\nЭнтропия исходного файла: {entropy_original}")
print(f"\nСредняя длина кодового слова (Хаффман): {average_code_length}")
print(f"Средняя длина кодового слова (Шеннон): {average_code_length_shannon}")
print(f"Средняя длина кодового слова (Фано): {average_code_length_fano}")
print(f"\nЭнтропия закодированного файла (Хаффман): {entropy_encoded_huffman}")
print(f"Энтропия закодированного файла (Шеннон): {entropy_encoded_shannon}")
print(f"Энтропия закодированного файла (Фано): {entropy_encoded_fano}")

adaptive_huffman_coder = codecs.getincrementalencoder('utf-8')()
adaptive_huffman_encoded_text = adaptive_huffman_coder.encode(input_text) + adaptive_huffman_coder.encode('', final=True)

original_size = len(input_text) * 8
huffman_compressed_size = len(''.join(generate_huffman_code(input_text).values()))
adaptive_huffman_compressed_size = len(adaptive_huffman_encoded_text)

huffman_compression_ratio = calculate_compression_ratio(original_size, huffman_compressed_size)
adaptive_huffman_compression_ratio = calculate_compression_ratio(original_size, adaptive_huffman_compressed_size)

compression_table = PrettyTable()
compression_table.field_names = ["Размер исходного файла", "Коэффициент сжатия Хаффмана", "Коэффициент сжатия адаптивного Хаффмана"]
compression_table.add_row([original_size, f"{huffman_compression_ratio:.2f}%", f"{adaptive_huffman_compression_ratio:.2f}%"])
print("\nКоэффициенты сжатия:")
print(compression_table)

def compress(text):
    dictionary = {chr(i): i for i in range(256)}
    current_code = 256
    result = []
    current_sequence = ""

    for char in text:
        current_sequence += char
        if current_sequence not in dictionary:
            result.append(dictionary.get(current_sequence[:-1], 0))
            dictionary[current_sequence] = current_code
            current_code += 1
            current_sequence = char

    if current_sequence in dictionary:
        result.append(dictionary[current_sequence])

    return result

def decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256
    result = []
    current_sequence = chr(compressed_data[0])
    result.append(current_sequence)

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == current_code:
            entry = current_sequence + current_sequence[0]
        else:
            raise ValueError("Invalid compressed data")

        result.append(entry)
        dictionary[current_code] = current_sequence + entry[0]
        current_code += 1
        current_sequence = entry

    return "".join(result)


# Пример использования
english_text = "This book is addressed to everyone who studies Russian. But it does not consist of rules, exercises and educational texts. Other great textbooks have been created for this purpose. This book has a completely different task. It will help you learn not only to speak, but also to think in Russian. The book you are holding in your hands is made up of aphorisms and reflections of great thinkers, writers, poets, philosophers and public figures of various eras. Their thoughts are about those issues that never cease to worry humanity. You can agree or disagree with what you read in this book. It may seem to you that some thoughts are already outdated. But you should definitely think about and justify why you think so. And you will also learn and feel how wonderful the words of love, compassion, wisdom and kindness sound in Russian."
russian_text = "Эта книга адресована всем, кто изучает русский язык. Но состоит она не из правил, упражнений и учебных текстов. Для этого созданы другие замечательные учебники.У этой книги совсем иная задача. Она поможет вам научиться не только разговаривать, но и размышлять по-русски. Книга, которую вы держите в руках, составлена из афоризмов и размышлений великих мыслителей, писателей, поэтов, философов и общественных деятелей различных эпох. Их мысли - о тех вопросах, которые не перестают волновать человечество.Вы можете соглашаться или не соглашаться с тем, что прочитаете в этой книге. Возможно, вам покажется, что какие-то мысли уже устарели. Но вы должны обязательно подумать и обосновать, почему вы так считаете.А еще вы узнаете и почувствуете, как прекрасно звучат слова любви, сострадания, мудрости и доброты на русском языке."
c_code = """
#include <stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}
{
 int i, last;
 void swap(int v[], int i, int j);
 if (left >= right) /* ничего не делается, если */
 return; /* в массиве менее двух элементов */
 swap(v, left, (left + right)/2); /* делящий элемент */
 last = left; /* переносится в v[0] */
 for(i = left+1; i <= right; i++) /* деление на части */
 if (v[i] < v[left])
 swap(v, ++last, i);
 swap(v, left, last); /* перезапоминаем делящий элемент */
 qsort(v, left, last-1);
 qsort(v, last+1, right);
}
{
 int temp;
 temp = v[i];
 v[i] = v[j];
 v[j] = temp;
}
#if SYSTEM == SYSV
#define HDR "sysv.h"
#elif SYSTEM == BSD
#define HDR "bsd.h"
#elif SYSTEM == MSDOS
#define HDR "msdos.h"
#else
#define HDR "default.h"
#endif
#include HDR
"""

compressed_english = compress(english_text)
compressed_russian = compress(russian_text)
compressed_c_code = compress(c_code)

print("\nАДАПТИВНЫЙ СЛОВАРЬ:")
table = [
    ["Текст на английском языке", len(english_text), len(compressed_english), len(compressed_english) / len(english_text)],
    ["Текст на русском языке", len(russian_text), len(compressed_russian), len(compressed_russian) / len(russian_text)],
    ["Текст программы на языке C", len(c_code), len(compressed_c_code), len(compressed_c_code) / len(c_code)],
]

headers = ["Тип текста", "Размер исходного файла", "Размер сжатого файла", "Коэффициент сжатия"]

print(tabulate(table, headers, tablefmt="grid"))