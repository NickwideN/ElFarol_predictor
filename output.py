# Модуль вывода данных
from predictor import predictors
import sys
from config import *
import matplotlib.pyplot as plt
import os
import datetime
import config


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
        processed_predictors = sorted(predictors, key=lambda predictor: predictor.persent_success())
    print(process_name)
    for pr in processed_predictors:
        print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_success()))
    if SORT_PREDICTORS == 'both':
        print('Неотсортированы:')
        for pr in predictors:
            print(format_str.format(pr.name, pr.success_cnt(), pr.active_cnt(), pr.persent_success()))


def apply_bar_attendance_plot(ax, bar_attendance, drawing_3_plots=False, **kwargs):
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


def apply_in_bar_cnt_plot(ax, in_bar_cnt_day_cnt_map, drawing_3_plots=False, **kwargs):
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


def apply_people_state_plot(ax, people, drawing_3_plots=False, day=None):
    if not drawing_3_plots:
        ax.set_title("Наборы предикторов у людей в день" + str(day))
    ax.set_xlabel('Человек')
    ax.set_ylabel('Предикторы')

    annotate_kwargs = [dict(xytext=(0, 2),
                            textcoords="offset points",
                            ha='left', va='bottom', fontsize=9),
                       dict(xytext=(0, -14),
                            textcoords="offset points",
                            ha='left', va='bottom', fontsize=9),
                       dict(xytext=(0, -6),
                            textcoords="offset points",
                            ha='left', va='bottom', fontsize=9),
                       dict(xytext=(0, -6),
                            textcoords="offset points",
                            ha='right', va='bottom', fontsize=9)]
    annotate_kwargs += [dict(xytext=(0, 2),
                             textcoords="offset points",
                             ha='left', va='bottom', fontsize=9) for _ in range(20)]

    # отметим на ординате всех предикторов
    # костыль: нарисуем невидимые точки для каждого предиктора
    x = [0 for _ in predictors]
    y = [predictor.get_str_state() for predictor in predictors]
    ax.scatter(x, y, marker='', color='blue')

    for man in people:
        x = [man.name for _ in man.predictor_set]
        y = [predictor_in_set.predictor.get_str_state() for predictor_in_set in man.predictor_set]
        point_title = [predictor_in_set.get_str_state() for predictor_in_set in man.predictor_set]
        ax.scatter(x, y, marker='o', color='blue')

        annotated_points_cnt = {}
        for i in range(len(point_title)):
            if y[i] not in annotated_points_cnt:
                annotated_points_cnt[y[i]] = 0
            else:
                annotated_points_cnt[y[i]] += 1
            ax.annotate(point_title[i], xy=(x[i], y[i]), **annotate_kwargs[annotated_points_cnt[y[i]]])

    ax.grid(which='major', axis='both', linestyle='--')


def draw_plots(bar_attendance=None, in_bar_cnt_day_cnt_map=None, people=None, show=True, last_day=None):
    plot_data = []
    if bar_attendance is not None:
        plot_data.append(dict(data=bar_attendance, apply_plot_func=apply_bar_attendance_plot))
    if in_bar_cnt_day_cnt_map is not None:
        plot_data.append(dict(data=in_bar_cnt_day_cnt_map, apply_plot_func=apply_in_bar_cnt_plot))
    if people is not None:
        plot_data.append(dict(data=people, apply_plot_func=apply_people_state_plot))

    if not plot_data:
        return None

    if len(plot_data) == 3:
        gridsize = (3, 3)
        fig = plt.figure(figsize=(14, 11))
        ax = [plt.subplot2grid(gridsize, (0, 1), colspan=1, rowspan=1),
              plt.subplot2grid(gridsize, (0, 2), colspan=1, rowspan=1),
              plt.subplot2grid(gridsize, (1, 0), colspan=3, rowspan=2)]

        title = "Наборы предикторов у людей \n"
        title += "День: " + str(len(bar_attendance) - 1)
        fig.suptitle(title, x=0.04, horizontalalignment='left', fontsize=17)
        text = "Числа у точек (для предиктора в наборе):\n"
        text += "(кол-во активаций;\n"
        text += "процент успешных дней (ПУТ);\n"
        text += "количество дней подряд, когда\n"
        text += "ПУТ ниже допустимого минимального)\n\n"
        text += "Числа у предикторов (для предикторов):\n"
        text += "(кол-во активаций;\n"
        text += "процент успешных дней)"
        fig.text(0.04, 0.7, text, horizontalalignment='left', fontsize=12)

    elif len(plot_data) == 2:
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    elif len(plot_data) == 1:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        ax = [ax]

    drawing_3_plots = False
    if len(plot_data) == 3:
        drawing_3_plots = True
    if last_day is None and bar_attendance is not None:
        last_day = len(bar_attendance) - 1
    for i in range(len(plot_data)):
        plot_data[i]['apply_plot_func'](ax[i], plot_data[i]['data'], drawing_3_plots=drawing_3_plots, day=last_day)

    if show:
        plt.show()
    plt.close()
    return fig


def draw_parameters():
    fig = plt.figure(figsize=(14, 11))
    text = "Параметры жизни:\n\n"
    for param in dir(config):
        if param[0].isupper():
            text += "{}: {}\n".format(param, globals()[param])
    fig.text(0.04, 0.6, text, fontsize=15)
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
