# Модуль вывода данных
import sys
from config import *
from exceptions import ArgumentsNotAssigned
import matplotlib.pyplot as plt
import os
import datetime
import config
import util

# Типы графиков:
# Посещаемость бара
PLOT_TYPE_BAR_ATTENDANCE = 0
# График зависимости количества дней от числа человек в баре в этот день
PLOT_TYPE_IN_BAR_CNT = 1
# График состояния людей (наборы предикторов)
PLOT_TYPE_PEOPLE_STATE = 2

PLOT_APPLY_FUNCS = {PLOT_TYPE_BAR_ATTENDANCE: "apply_bar_attendance_plot",
                    PLOT_TYPE_IN_BAR_CNT: "apply_in_bar_cnt_plot",
                    PLOT_TYPE_PEOPLE_STATE: "apply_people_state_plot"}


def print_progress(description, count, total):
    percent = int(count * 100 / total)
    sys.stdout.write("\r" + description + ": " + "... %d %%" % percent)
    sys.stdout.flush()


def print_bar_attendance(bar_attendance):
    print("Посещаемость бара:")
    for day in range(DAY_CNT):
        if not day % 30:
            print('{:^5}|{:^7}'.format('day', 'in_bar_cnt'))
        print('{:^5}|{:^7}'.format(day, bar_attendance[day]))


def print_in_bar_cnt_day_cnt_map(bar_attendance):
    in_bar_cnt_day_cnt_map = create_in_bar_cnt_day_cnt_map(bar_attendance)
    print("Количество дней, когда в баре было in_bar_cnt человек:")
    i = 0
    for in_bar_cnt in sorted(in_bar_cnt_day_cnt_map):
        if not i % 30:
            print('{:^5}|{:^7}'.format('in_bar_cnt', 'day_cnt'))
        print('{:^10}|{:^7}'.format(in_bar_cnt, in_bar_cnt_day_cnt_map[in_bar_cnt]))
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
        processed_predictors = sorted(predictors, key=lambda predictor: predictor.persent_success())
    print(process_name)
    for pr in processed_predictors:
        print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_success()))
    if SORT_PREDICTORS == 'both':
        print('Неотсортированы:')
        for pr in predictors:
            print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_success()))


def apply_bar_attendance_plot(ax, data, last_day, drawing_3_plots=False):
    if "bar_attendance" in data:
        bar_attendance = data["bar_attendance"][:last_day + 1]
    else:
        raise ArgumentsNotAssigned('data["bar_attendance"]')

    ax.set_title("График посещаемости бара")
    ax.set_xlabel('День')
    ax.set_ylabel('Количество человек в баре')

    average_attendance = round(sum(bar_attendance) / DAY_CNT, 2)

    # рисуем линию, к которой надо стремиться
    x, y = [0, DAY_CNT], [MAX_MAN_CNT_WHEN_GOOD, MAX_MAN_CNT_WHEN_GOOD]
    ax.plot(x, y, color='red', label="Лимит бара: " + str(MAX_MAN_CNT_WHEN_GOOD))

    # рисуем границы области
    if len(bar_attendance) > 80:
        upper_limit = max(bar_attendance[-20:])
        x, y = [0, DAY_CNT], [upper_limit, upper_limit]
        ax.plot(x, y, color='green', label="Верхняя граница области: " + str(upper_limit))
        lower_limit = min(bar_attendance[-20:])
        x, y = [0, DAY_CNT], [lower_limit, lower_limit]
        ax.plot(x, y, color='green', label="Нижняя граница области: " + str(lower_limit))

    # рисуем основной график
    ax.plot(
        [day for day in range(len(bar_attendance))],
        bar_attendance,
        color='blue',
        linewidth=1,
        label='Среднее: ' + str(average_attendance)
    )

    ax.grid(which='major', axis='y', linestyle='-')
    ax.minorticks_on()
    if not drawing_3_plots:
        ax.legend()


def create_in_bar_cnt_day_cnt_map(bar_attendance, last_day=None):
    if last_day is None:
        last_day = len(bar_attendance) - 1
    in_bar_cnt_day_cnt_map = {}
    for day in range(last_day + 1):
        if bar_attendance[day] not in in_bar_cnt_day_cnt_map:
            in_bar_cnt_day_cnt_map[bar_attendance[day]] = 0
        in_bar_cnt_day_cnt_map[bar_attendance[day]] += 1
    return in_bar_cnt_day_cnt_map


def apply_in_bar_cnt_plot(ax, data, last_day, drawing_3_plots=False):
    if "in_bar_cnt_day_cnt_map" not in data and "bar_attendance" not in data:
        raise ArgumentsNotAssigned("data")
    if "in_bar_cnt_day_cnt_map" in data:
        in_bar_cnt_day_cnt_map = data["in_bar_cnt_day_cnt_map"]
    else:
        in_bar_cnt_day_cnt_map = create_in_bar_cnt_day_cnt_map(data["bar_attendance"], last_day)

    if drawing_3_plots:
        ax.set_title("График зависимости количества дней\nот числа человек в баре в этот день")
    else:
        ax.set_title("График зависимости количества дней от числа человек в баре в этот день")
    ax.set_xlabel('Количество человек в баре')
    ax.set_ylabel('Количество дней')

    x = []
    y = []
    for in_bar_cnt in in_bar_cnt_day_cnt_map:
        x.append(in_bar_cnt)
        y.append(in_bar_cnt_day_cnt_map[in_bar_cnt])

    # рисуем основной график
    ax.bar(
        x, y,
        width=0.3, color='blue', alpha=0.7, label='in_bar_cnt',
        zorder=2
    )

    # рисуем линию, к которой надо стремиться
    x, y = [MAX_MAN_CNT_WHEN_GOOD, MAX_MAN_CNT_WHEN_GOOD], [0, max(in_bar_cnt_day_cnt_map.values())]
    ax.plot(x, y, color='red', label="Лимит бара: " + str(MAX_MAN_CNT_WHEN_GOOD))

    # отметим 5 максимальных по значению точки
    # выберем 5 самых наибольший посещаемостей
    if not drawing_3_plots:
        for in_bar_cnt in sorted(in_bar_cnt_day_cnt_map.keys(), key=lambda in_bar_cnt: in_bar_cnt_day_cnt_map[in_bar_cnt])[-5:]:
            height = in_bar_cnt_day_cnt_map[in_bar_cnt]
            ax.annotate('{}'.format(in_bar_cnt),
                        xy=(in_bar_cnt, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    ax.grid(which='both', axis='y', linestyle='-')
    if not drawing_3_plots:
        ax.legend()


# Характеристики прорисовки обозначений у точек
annotate_kwargs = [dict(xytext=(2, 2),
                        textcoords="offset points",
                        ha='left', va='bottom', fontsize=9),
                   dict(xytext=(2, -6),
                        textcoords="offset points",
                        ha='left', va='bottom', fontsize=9),
                   dict(xytext=(2, -14),
                        textcoords="offset points",
                        ha='left', va='bottom', fontsize=9),
                   dict(xytext=(-2, -6),
                        textcoords="offset points",
                        ha='right', va='bottom', fontsize=9)]
annotate_kwargs += [dict(xytext=(0, 2),
                         textcoords="offset points",
                         ha='left', va='bottom', fontsize=9) for _ in range(20)]


def apply_people_state_plot(ax, data, last_day, drawing_3_plots=False):
    if "people" in data:
        people = data["people"]
    else:
        raise ArgumentsNotAssigned('data["people"]')
    if "bar_attendance" in data:
        bar_attendance = data["bar_attendance"]
    else:
        raise ArgumentsNotAssigned('data["bar_attendance"]')
    if "predictors" in data:
        predictors = data["predictors"]
    else:
        raise ArgumentsNotAssigned('data["predictors"]')

    if not drawing_3_plots:
        ax.set_title("Наборы предикторов у людей в день" + str(last_day))
    ax.set_xlabel('Человек')
    ax.set_ylabel('Предикторы')

    # отметим на ординате все предикторы в нужных цветах
    ax.set_yticks([predictor_i for predictor_i in range(len(predictors))])
    labels = ax.get_yticklabels()
    for i in range(len(ax.get_yticklabels())):
        color = 'red'
        if predictors[i].is_day_success(last_day, bar_attendance):
            color = 'green'
        labels[i].set_color(color)

    # отметим на абсцисе всех людей в нужных цветах
    ax.set_xticks([man.name for man in people])
    labels = ax.get_xticklabels()
    for i in range(len(ax.get_xticklabels())):
        color = 'red'
        if people[i].is_day_success(last_day, bar_attendance):
            color = 'green'
        labels[i].set_color(color)

    # костыль: нарисуем невидимые точки для каждого предиктора, чтобы они все отображались на графике
    x = [0 for _ in predictors]
    # Если предиктор неактивен, он зачеркнут
    y = [(predictor.get_str_state() if predictor.is_active(people) else util.cross_text(predictor.get_str_state())) for predictor in predictors]
    ax.scatter(x, y, marker='')

    for man in people:
        x = [man.name for _ in man.predictor_set]
        # Здесь нет неактивных предикторов, значит все предикторы не зачеркнуты
        y = [predictor_in_set.predictor.get_str_state() for predictor_in_set in man.predictor_set]
        point_title = [predictor_in_set.get_str_state() for predictor_in_set in man.predictor_set]
        ax.scatter(x, y, marker='o', color='blue')

        # Нарисуем обозначения к точкам в месте, определенном в annotate_kwargs
        annotated_points_cnt = {}
        for i in range(len(point_title)):
            if y[i] not in annotated_points_cnt:
                annotated_points_cnt[y[i]] = 0
            else:
                annotated_points_cnt[y[i]] += 1
            ax.annotate(point_title[i], xy=(x[i], y[i]), **annotate_kwargs[annotated_points_cnt[y[i]]])

    ax.grid(which='major', axis='both', linestyle='--')
    ax.tick_params(axis='both', labelsize=14)


def draw_plot(plot_types, history, last_day=None, show=True):
    """
    :param plot_types: [TYPE_PLOT]
        список типов графиков, которые надо прорисовать
    :param history: object of History
    :param show: Рисовать ли график
    :param last_day: Последний день графика, который будет прорисован
    :return:
    """
    if not plot_types:
        return None

    if last_day is None and history.bar_attendance:
        last_day = len(history.bar_attendance) - 1
    if last_day is None:
        raise ArgumentsNotAssigned("last_day")

    plot_data = {"bar_attendance": history.bar_attendance,
                 "people": history.get_people_state(last_day),
                 "predictors": history.get_predictors_state(last_day)}

    drawing_3_plots = False
    if len(plot_types) == 3:
        drawing_3_plots = True

    if drawing_3_plots:
        gridsize = (3, 3)
        fig = plt.figure(figsize=(14, 11))
        ax = [plt.subplot2grid(gridsize, (0, 1), colspan=1, rowspan=1),
              plt.subplot2grid(gridsize, (0, 2), colspan=1, rowspan=1),
              plt.subplot2grid(gridsize, (1, 0), colspan=3, rowspan=2)]

        title = "Наборы предикторов у людей. День: " + str(last_day)
        fig.suptitle(title, x=0.04, horizontalalignment='left', fontsize=17)
        text = "Числа у точек (для предиктора в наборе):\n"
        text += "(кол-во активаций;\n"
        text += "процент успешных дней (ПУТ);\n"
        text += "количество дней подряд, когда\n"
        text += "ПУТ ниже допустимого минимального)\n\n"
        text += "Числа у предикторов (для предикторов):\n"
        text += "(кол-во активаций;\n"
        text += "процент успешных дней)\n\n"
        text += "Цвета означают успешность дня\n"
        text += "для бара, предиктора и человека"
        fig.text(0.04, 0.725, text, horizontalalignment='left', fontsize=12)
        color = 'red'
        if is_day_success(plot_data["bar_attendance"][last_day]):
            color = 'green'
        fig.text(0.04, 0.695, "Количество человек в баре: {}".format(plot_data["bar_attendance"][last_day]), fontsize=15, color=color)
        average_attendance = round(sum(plot_data["bar_attendance"][:last_day + 1]) / (last_day + 1), 2)
        fig.text(0.04, 0.665, "Среднее количество в баре: {} ↗".format(average_attendance), fontsize=15, color="blue")
    elif len(plot_types) == 2:
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    elif len(plot_types) == 1:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        ax = [ax]

    plot_types = sorted(plot_types)
    for i in range(len(ax)):
        # Прорисуем график plot_type на аксесе ax[plot_type]
        globals()[PLOT_APPLY_FUNCS[plot_types[i]]](ax[i], plot_data, last_day, drawing_3_plots=drawing_3_plots)
    if show:
        plt.show()
    plt.close()
    return fig


def draw_parameters(show=False):
    fig = plt.figure(figsize=(14, 11))
    text = "Параметры жизни:\n\n"
    for param in dir(config):
        if param[0].isupper():
            text += "{}: {}\n".format(param, globals()[param])
    fig.text(0.04, 0.6, text, fontsize=15)
    if show:
        plt.show()
    return fig


def save_fig(fig, plot_dir=None, name=None):
    plot_root_dir = 'life_screens'
    if not os.path.isdir(plot_root_dir):
        os.makedirs(plot_root_dir)
    path = plot_root_dir
    if plot_dir is not None:
        path += "/" + plot_dir
        if not os.path.isdir(plot_root_dir + "/" + plot_dir):
            os.makedirs(path)
    if name is None:
        name = datetime.datetime.now().strftime('%H:%M:%S') + ".png"
    path += "/" + name
    fig.savefig(path, bbox_inches='tight')
