from man import Man
from config import *
from predictor import predictors, upload_predictors_in_life, get_active_predictors
import output
from exceptions import PredictorInSetCntExceedsPredictorCnt
import datetime


def live_day(today, people, bar_attendance):
    bar_attendance.append(0)
    # Утро. Люди решают идти либо не идти в бар и следуют своему решению
    for man in people:
        if man.decide_go(today, bar_attendance):
            bar_attendance[today] += 1
    # Вечер. Каждый активный предиктор анализирует день
    for predictor in get_active_predictors(people):
        predictor.analyze_day(today, bar_attendance)
    # Вечер. Каждый человек анализирует день и меняет свои предикторы при необходимости
    for man in people:
        man.analyze_day(today, bar_attendance)


if __name__ == '__main__':
    upload_predictors_in_life()
    if PREDICTOR_IN_SET_CNT > len(predictors):
        raise PredictorInSetCntExceedsPredictorCnt(len(predictors))
    bar_attendance = []
    people = [Man(i) for i in range(MAN_CNT)]
    output.print_predictor_cnt()

    now_str = datetime.datetime.now().strftime("%Y%m%dT%H-%M-%S")

    plot_data = dict(bar_attendance=bar_attendance, people=people)

    if SAVE_PLOTS and SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_parameters()
        output.save_fig(fig, plot_dir=now_str, name="Parameters.png")

    for day in range(DAY_CNT):
        output.print_progress(day, DAY_CNT)
        live_day(day, people, bar_attendance)

        # todo Надо добавить историю и исходя из нее сторить графики и после того как вся жизнь прошла
        if SAVE_PLOTS_OF_EVERY_DAY:
            fig = output.draw_plots(SAVE_PLOTS, plot_data, show=False)
            if fig:
                output.save_fig(fig, plot_dir=now_str, name="day" + str(day) + ".png")
    print()

    output.print_bar_attandance(bar_attendance)

    print()
    output.print_in_bar_cnt_day_cnt_map(bar_attendance)

    print()
    output.print_predictors(predictors)

    if SAVE_PLOTS and SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_plots([output.PLOT_TYPE_BAR_ATTENDANCE, output.PLOT_TYPE_IN_BAR_CNT], plot_data, show=False)
        output.save_fig(fig, plot_dir=now_str, name="Result.png")

    if SAVE_PLOTS and not SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_plots(SAVE_PLOTS, plot_data, show=False)
        if fig:
            output.save_fig(fig, plot_dir=None, name=now_str + ".png")

    if DRAW_PLOTS:
        output.draw_plots(DRAW_PLOTS, plot_data, show=True)
