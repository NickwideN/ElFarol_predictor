from typing import Set
from man import Man
from config import *
from predictor import Predictor, predictors, upload_predictors_in_life
import matplotlib as mpl
import matplotlib.pyplot as plt
import output


def live_day(today, people, bar_attendance):
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
    upload_predictors_in_life()
    bar_attendance = []
    people = [Man(i) for i in range(MAN_CNT)]
    for day in range(DAY_CNT):
        output.print_progress(day, DAY_CNT)
        live_day(day, people, bar_attendance)

    # output
    report = {}
    for day in range(DAY_CNT):
        print("day:", day, "in_bar:", bar_attendance[day])
        # for man in people:
        #     print(man)
        if bar_attendance[day] not in report:
            report[bar_attendance[day]] = 0
        report[bar_attendance[day]] += 1
        print("#########################################")
    print()
    print("колчество дней, когда в баре было in_bar_cnt человек")
    for in_bar_cnt in sorted(report):
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

        x = []
        y = []
        for in_bar_cnt in report:
            x.append(in_bar_cnt)
            y.append(report[in_bar_cnt])

        plt.bar(x, y,
                width=0.3, color='blue', alpha=0.7, label='in_bar_cnt',
                zorder=2)

        x1, y1 = [MAX_MAN_CNT_WHEN_GOOD, MAX_MAN_CNT_WHEN_GOOD], [0, max(report.values())]
        plt.plot(x1, y1, color='red', label=MAX_MAN_CNT_WHEN_GOOD)

        fig.autofmt_xdate(rotation=25)

        plt.legend(loc='upper right')

        plt.show()

    if DRAW_PLOT_attendance:
        dpi = 80
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
