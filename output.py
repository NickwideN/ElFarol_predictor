# Модуль вывода данных
from predictor import predictors
import sys


def print_progress(count, total):
    percent = int(count * 100 / total)
    sys.stdout.write("\r" + "Барная жизнь: " + "... %d %%" % percent)
    sys.stdout.flush()


def print_predictor_cnt():
    print("Количество использующихся предикторов: %d" % len(predictors))
