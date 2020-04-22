# Модуль вывода данных
from predictor import predictors
import sys
from config import *
import matplotlib as mpl
import matplotlib.pyplot as plt


def print_progress(count, total):
    percent = int(count * 100 / total)
    sys.stdout.write("\r" + "Барная жизнь: " + "... %d %%" % percent)
    sys.stdout.flush()


def print_predictor_cnt():
    print("Количество использующихся предикторов: %d" % len(predictors))


def print_bar_attandance(bar_attendance):
    print("Посещаемость бара:")
    for day in range(DAY_CNT):
        if not day % 30:
            print('{:^5}|{:^7}'.format('day', 'in_bar_cnt'))
        print('{:^5}|{:^7}'.format(day, bar_attendance[day]))


def print_day_cnt_in_bar_cnt_map(day_cnt_in_bar_cnt_map):
    print("Количество дней, когда в баре было in_bar_cnt человек:")
    i = 0
    for in_bar_cnt in sorted(day_cnt_in_bar_cnt_map):
        if not i % 30:
            print('{:^5}|{:^7}'.format('in_bar_cnt', 'day_cnt'))
        print('{:^10}|{:^7}'.format(in_bar_cnt, day_cnt_in_bar_cnt_map[in_bar_cnt]))
        i += 1


def print_predictors(predictors):
    print("Предикторы:")
    print("Колонка 1: Имя")
    print("Колонка 2: Колво успешных для предиктора дней")
    print("Колонка 3: Колво дней, когда предиктор использовали")
    print("Колонка 4: Процент успешных дней для предиктора")
    # w -- width
    w1 = '20'
    w2 = '5'
    w3 = '5'
    w4 = '7'
    format_str = "{:^" + w1 + "}|{:^" + w2 + "}|{:^" + w3 + "}|{:^" + w4 + ".1%}"
    processed_predictors = predictors
    # if SORT_PREDICTORS == True or SORT_PREDICTORS=='both'
    process_name = 'Неотсортированы:'
    if SORT_PREDICTORS:
        process_name = 'Отсортированы по проценту успешных дней:'
        processed_predictors = sorted(predictors, key=lambda predictor: predictor.persent_seccess())
    print(process_name)
    for pr in processed_predictors:
        print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_seccess()))
    if SORT_PREDICTORS == 'both':
        print('Неотсортированы:')
        for pr in predictors:
            print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_seccess()))


def draw_plot_in_bar_cnt(day_cnt_in_bar_cnt_map):
    fig = plt.figure()

    mpl.rcParams.update({'font.size': 10})

    plt.title('количество дней, когда в баре было in_bar_cnt человек')

    ax = plt.axes()
    ax.yaxis.grid(True, zorder=1)

    #  Добавляем подписи к осям:
    ax.set_xlabel('in_bar_cnt')
    ax.set_ylabel('Количество дней')

    x1, y1 = [MAX_MAN_CNT_WHEN_GOOD, MAX_MAN_CNT_WHEN_GOOD], [0, max(day_cnt_in_bar_cnt_map.values())]
    plt.plot(x1, y1, color='red', label=MAX_MAN_CNT_WHEN_GOOD)

    x = []
    y = []
    for in_bar_cnt in day_cnt_in_bar_cnt_map:
        x.append(in_bar_cnt)
        y.append(day_cnt_in_bar_cnt_map[in_bar_cnt])

    plt.bar(x, y,
            width=0.3, color='blue', alpha=0.7, label='in_bar_cnt',
            zorder=2)

    fig.autofmt_xdate(rotation=25)


def draw_plot_attendance(bar_attendance):
    fig = plt.figure(figsize=(10, 5), dpi=200)
    mpl.rcParams.update({'font.size': 10})

    plt.title("People : " + str(MAN_CNT) + "\nmax_good_attendance: " + str(MAX_MAN_CNT_WHEN_GOOD) + "\n CAN_PREDICTORS_CHANGE_CONDITION: " + str(CAN_PREDICTORS_CHANGE_CONDITION) + "\n PREDICTOR_IN_SET_CNT: " + str(PREDICTOR_IN_SET_CNT) + "\nARE_UNIQUE_PREDICTORS_IN_SET: " + str(ARE_UNIQUE_PREDICTORS_IN_SET))

    ax = plt.axes()
    ax.yaxis.grid(True, zorder=1)

    #  Добавляем подписи к осям:
    ax.set_xlabel('День')
    ax.set_ylabel('Количество в баре')

    average_attendance = sum(bar_attendance) / DAY_CNT

    plt.plot([day for day in range(len(bar_attendance))], bar_attendance, color='blue', alpha=0.7, linewidth=1, label='in_bar_cnt. average=' + str(average_attendance))

    x1, y1 = [0, DAY_CNT], [MAX_MAN_CNT_WHEN_GOOD, MAX_MAN_CNT_WHEN_GOOD]
    plt.plot(x1, y1, color='red', label=MAX_MAN_CNT_WHEN_GOOD)

    fig.autofmt_xdate(rotation=25)

    plt.legend(loc='upper right')

    plt.show()
