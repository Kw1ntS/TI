from tabulate import tabulate

# Функция для сжатия текста с использованием адаптивного словаря
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

# Тексты на разных языках и программный код на языке C
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

# Сжатие текстов и программного кода
compressed_english = compress(english_text)
compressed_russian = compress(russian_text)
compressed_c_code = compress(c_code)

# Вывод результатов в виде таблицы
print("\nАДАПТИВНЫЙ СЛОВАРЬ:")
table = [
    ["Текст на английском языке", len(english_text), len(compressed_english), 
     f"{(len(compressed_english) / len(english_text)) * 100:.2f}%"],
    ["Текст на русском языке", len(russian_text), len(compressed_russian), 
     f"{(len(compressed_russian) / len(russian_text)) * 100:.2f}%"],
    ["Текст программы на языке C", len(c_code), len(compressed_c_code), 
     f"{(len(compressed_c_code) / len(c_code)) * 100:.2f}%"],
]
headers = ["Тип текста", "Размер исходного файла", "Размер сжатого файла", "Коэффициент сжатия"]

# Вывод таблицы с результатами
print(tabulate(table, headers, tablefmt="grid"))