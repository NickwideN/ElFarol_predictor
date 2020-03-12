# Модуль вывода данных

import sys


def print_progress(count, total):
    percent = int(count * 100 / total)
    sys.stdout.write("\r" + "Барная жизнь: " + "... %d %%" % percent)
    sys.stdout.flush()
