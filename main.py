import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from heapq import nlargest

# Загрузка стоп-слов
nltk.download('stopwords')


def generate_summary(text, num_sentences=3):
    # Разделение текста на предложения
    sentences = sent_tokenize(text)

    # Создание словаря частотности слов
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word.lower() not in stopwords.words('russian'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Нормализация частотности слов
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    # Вычисление взвешенной частотности предложений
    sentence_scores = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Выбор наиболее важных предложений
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary


def summarize_text():
    text = text_box.get("1.0", "end-1c")
    if text:
        summary = generate_summary(text)
        summary_box.config(state='normal')
        summary_box.delete(1.0, tk.END)
        summary_box.insert(tk.END, summary)
        summary_box.config(state='disabled')
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите текст для создания краткого содержания.")


def paste_text(event):
    text = root.clipboard_get()
    text_widget = root.focus_get()
    if isinstance(text_widget, tk.Text) or isinstance(text_widget, tk.scrolledtext.ScrolledText):
        text_widget.insert(tk.INSERT, text)


def clear_all():
    text_box.delete("1.0", tk.END)
    summary_box.config(state='normal')
    summary_box.delete(1.0, tk.END)
    summary_box.config(state='disabled')


# Создание графического интерфейса
root = tk.Tk()
root.title("Суммаризация текста")

# Оформление стилей
style = ttk.Style()
style.configure('Custom.TButton', font=('Arial', 12, 'bold'), foreground='black', background='#19ace2')
style.configure('Custom.TLabel', font=('Arial', 12), foreground='#333')  # Изменено на черный текст
style.configure('Custom.TText', font=('Arial', 11), foreground='#333',
                background='#fff')  # Изменено на черный текст на белом фоне

# Создание текстового поля для ввода текста
text_label = ttk.Label(root, text="Введите текст:", style='Custom.TLabel')
text_label.pack()
text_box = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD, font=('Arial', 11))
text_box.pack()

# Привязываем событие вставки текста к корневому окну
root.bind("<Control-v>", paste_text)

# Создание кнопки для генерации краткого содержания
summarize_button = ttk.Button(root, text="Создать краткое содержание", command=summarize_text, style='Custom.TButton')
summarize_button.pack()

# Создание текстового поля для вывода краткого содержания
summary_label = ttk.Label(root, text="Краткое содержание:", style='Custom.TLabel')
summary_label.pack()
summary_box = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD, font=('Arial', 11))
summary_box.pack()
summary_box.config(state='disabled')

# Кнопка для очистки всего содержимого
clear_button = ttk.Button(root, text="Очистить всё", command=clear_all, style='Custom.TButton')
clear_button.pack()

root.mainloop()