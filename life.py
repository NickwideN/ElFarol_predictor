from typing import Set
from man import Man
from config import *
from predictor import Predictor, predictors, upload_predictors_in_life
import matplotlib as mpl
import matplotlib.pyplot as plt
import output
import check_config


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
    check_config.check_config_parameters()
    bar_attendance = []
    people = [Man(i) for i in range(MAN_CNT)]
    output.print_predictor_cnt()

    for day in range(DAY_CNT):
        output.print_progress(day, DAY_CNT)
        live_day(day, people, bar_attendance)
    print()

    output.print_bar_attandance(bar_attendance)

    day_cnt_in_bar_cnt_map = {}
    for day in range(DAY_CNT):
        if bar_attendance[day] not in day_cnt_in_bar_cnt_map:
            day_cnt_in_bar_cnt_map[bar_attendance[day]] = 0
        day_cnt_in_bar_cnt_map[bar_attendance[day]] += 1

    print()
    output.print_day_cnt_in_bar_cnt_map(day_cnt_in_bar_cnt_map)

    print()
    output.print_predictors(predictors)

    if DRAW_PLOT_in_bar_cnt:
        output.draw_plot_in_bar_cnt(day_cnt_in_bar_cnt_map)

    if DRAW_PLOT_attendance:
        output.draw_plot_attendance(bar_attendance)
