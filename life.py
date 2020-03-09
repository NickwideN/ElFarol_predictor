from typing import Set
from man import Man
from config import *
from predictor import Predictor, predictors
import matplotlib as mpl
import matplotlib.pyplot as plt

people = [Man(i) for i in range(MAN_CNT)]

bar_attendance = []


def live_day(today):
    bar_attendance.append(0)
    for man in people:
        if man.decide_go(today, bar_attendance):
            bar_attendance[today] += 1
    active_predictors: Set[Predictor] = set()
    for man in people:
        active_predictors.update(man.get_predictors())
        man.analyze_day(today, bar_attendance)
    for predictor in active_predictors:
        predictor.analyze_day(today, bar_attendance)


if __name__ == '__main__':
    report = [in_bar_cnt for in_bar_cnt in range(MAN_CNT + 1)]
    for day in range(DAY_CNT):
        live_day(day)
        print("day:", day, "in_bar:", bar_attendance[day])
        # for man in people:
        #     print(man)
        report[bar_attendance[day]] += 1
        print("#########################################")
    print()
    print("колчество дней, когда в баре было in_bar_cnt человек")
    for in_bar_cnt in range(len(report)):
        print("in_bar_cnt:", in_bar_cnt, "day_cnt:", report[in_bar_cnt])
    print()
    print("predictors")
    for pr in predictors:
        print(pr)

    if DRAW_PLOT_in_bar_cnt:
        dpi = 200
        fig = plt.figure()
        mpl.rcParams.update({'font.size': 10})

        plt.title('количество дней, когда в баре было in_bar_cnt человек')

        ax = plt.axes()
        ax.yaxis.grid(True, zorder=1)

        #  Добавляем подписи к осям:
        ax.set_xlabel('in_bar_cnt')
        ax.set_ylabel('Количество дней')

        plt.bar([in_bar_cnt for in_bar_cnt in range(len(report))], [report[in_bar_cnt] for in_bar_cnt in range(len(report))],
                width=0.2, color='blue', alpha=0.7, label='in_bar_cnt',
                zorder=2)

        fig.autofmt_xdate(rotation=25)

        plt.legend(loc='upper right')

        plt.show()

    if DRAW_PLOT_attendance:
        dpi = 80
        fig = plt.figure()
        mpl.rcParams.update({'font.size': 10})

        plt.title('Посещаемость')

        ax = plt.axes()
        ax.yaxis.grid(True, zorder=1)

        #  Добавляем подписи к осям:
        ax.set_xlabel('День')
        ax.set_ylabel('Количество в баре')

        plt.plot([day for day in range(len(bar_attendance))], bar_attendance, color='blue', alpha=0.7, label='in_bar_cnt')

        fig.autofmt_xdate(rotation=25)

        plt.legend(loc='upper right')

        plt.show()

