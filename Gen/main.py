import pandas as pd
from random import shuffle, random
import sys
import numpy as np

MAX_WORD_LENGTH = 30
MAX_BYTE_FILE_SIZE = 102400


class Letter:
    letter = ""
    count = 0

    def __init__(self, letter, count):
        self.letter = letter
        self.count = count

    def count_percentage(self, all_count):
        return self.count / all_count

    def remove_one(self):
        self.remove_count(1)

    def remove_count(self, count):
        self.count -= count

    def __str__(self):
        return f"{self.letter} = {self.count}"


class Alphabet:
    list_percentages = list()
    list_letters = list()
    count_all = 0

    def __init__(self, list_letters):
        self.list_letters = list_letters
        self.init_count_all()
        self.init_percentages()

    def init_count_all(self):
        ans = 0
        for letter in self.list_letters:
            ans += letter.count
        self.count_all = ans

    def remove_one_symbol(self, indx):
        self.list_letters[indx].remove_one()
        self.remove_one_from_count_all()
        self.recalculate_percentages()

    def remove_one_from_count_all(self):
        self.remove_from_count_all(1)

    def remove_from_count_all(self, value):
        self.count_all -= value

    def remove_zeros_letters(self):
        for letter in self.list_letters:
            if letter.count == 0:
                self.list_letters.remove(letter)

    def init_percentages(self):
        self.list_percentages = list()
        prev = 0
        self.remove_zeros_letters()
        for letter in self.list_letters:
            prev += letter.count_percentage(self.count_all)
            self.list_percentages.append(prev)

    def recalculate_percentages(self):
        self.init_percentages()

    def get_one_symbol(self):
        value = random()
        rnd = 0
        if len(self.list_percentages) == 0:
            print(self.list_percentages)
        while rnd < len(self.list_percentages) and self.list_percentages[rnd] < value:
            rnd += 1
        ans = self.list_letters[rnd].letter
        self.remove_one_symbol(rnd)
        return ans

    def __str__(self):
        return f"{self.list_letters} = {self.count_all} = {self.list_percentages}"


def get_value_by_index(i, j):
    return df.to_numpy()[i][j]


def get_index(letter):
    if ord('а') <= ord(letter) <= ord('я'):
        return int(ord(letter) - ord('а'))
    elif letter == 'z':
        return 32
    elif letter == '!':
        return 33
    elif letter == '?':
        return 34
    elif letter == '.':
        return 35
    elif letter == ',':
        return 36


def generate_dict_with_frequency(copy_list, np_array):
    ans = dict()
    for i in np_array:
        new_list = list()
        for j in copy_list:
            if get_value_by_index(get_index(i[0]), get_index(j) + 1) != 0:
                new_list.append(Letter(j, get_value_by_index(get_index(i[0]), get_index(j) + 1)))
        ans[str(i[0])] = Alphabet(new_list)
    return ans


def generate_start_symbols(alphabet: dict):
    ans = list()
    for alph in alphabet:
        if alphabet[alph].count_all != 0 and get_index(alph) < 32:
            ans.append(alph)
    return ans


def need_stop_generate(length, curr_symbol):
    if length >= MAX_WORD_LENGTH or get_index(curr_symbol) >= 32:
        return True
    return False


def check_space_and_append(curr):
    if curr == 'z':
        return ' '
    return curr + ' '


def print_into_file(data, counter):
    my_file = open("/home/jupyter/datasphere/project/Gen/synthetic" + str(counter) + ".txt", "w+")
    my_file.write(data)
    my_file.close()


def generate_files(alphabet: dict):
    start_symbols = generate_start_symbols(alphabet)
    data = ''
    counter = 0
    while len(start_symbols) > 0:
        curr_length = 0
        shuffle(start_symbols)
        curr_symbol = start_symbols[0]
        while alphabet[curr_symbol].count_all != 0 and not need_stop_generate(curr_length, curr_symbol):
            data += curr_symbol
            curr_symbol = alphabet[curr_symbol].get_one_symbol()
        data += check_space_and_append(curr_symbol)
        if len(data) > MAX_BYTE_FILE_SIZE:
            print_into_file(data, counter)
            counter += 1
            data = ''
        start_symbols = generate_start_symbols(alphabet)


if __name__ == '__main__':
    np.set_printoptions(threshold=sys.maxsize)
    df = pd.read_csv("/home/jupyter/datasphere/project/Gen/data.csv", delimiter=";")
    alphabet_list = df.columns[0:38].to_list()[1:len(df.columns[0:38].to_list())]
    generate_files(
        generate_dict_with_frequency(alphabet_list, df.to_numpy()))
