from man import Man
from config import *
from predictor import predictors, upload_predictors_in_life, get_active_predictors
import output
from exceptions import PredictorInSetCntExceedsPredictorCnt
import datetime
from history import History
import analysis


def live_day(today, people, bar_attendance, history):
    bar_attendance.append(0)
    # День. Люди решают идти либо не идти в бар и следуют своему решению
    for man in people:
        if man.decide_go(today, bar_attendance):
            bar_attendance[today] += 1

    # Вечер. Каждый активный предиктор анализирует день (подсчитывает активные и успешные дни)
    for predictor in get_active_predictors(people):
        predictor.analyze_day(today, bar_attendance)
    # Вечер. Каждый человек анализирует день (каждый предиктор в наборе человека подсчитывает активные и успешные дни)
    for man in people:
        man.analyze_day(today, bar_attendance)

    # Сохраним состояние людей и предикторов в историю
    history.save_state(people, predictors, today)

    # Утро. Каждый человек меняет свои предикторы, которые вчера посоветовали ему ересь(идти, когда в баре полно людей или не идти, когда в баре куча свободных мет)
    for man in people:
        man.update_predictors()


def live_life(log=True):
    upload_predictors_in_life()
    if PREDICTOR_IN_SET_CNT > len(predictors):
        raise PredictorInSetCntExceedsPredictorCnt(len(predictors))
    bar_attendance = []
    people = [Man(i) for i in range(MAN_CNT)]
    history = History()

    if log:
        print("Количество использующихся предикторов: %d" % len(predictors))
    for day in range(DAY_CNT):
        if log:
            output.print_progress("Барная жизнь", day, DAY_CNT)
        live_day(day, people, bar_attendance, history)
        # history.save_bar_attendance(bar_attendance)
        # fig = output.draw_plots([0, 1, 2], history, last_day=day, show=True)
        # continue

    history.save_bar_attendance(bar_attendance)

    if log:
        output.print_bar_attendance(bar_attendance)

        print()
        output.print_in_bar_cnt_day_cnt_map(bar_attendance)

        print()
        output.print_predictors(predictors)

        print()
        print(output.get_parameters_str(predictors))

        now_str = datetime.datetime.now().strftime("%Y%m%dT%H-%M-%S")

        if DRAW_PLOTS or SAVE_PLOTS:
            print("Отрисовка графиков")
        if DRAW_PLOTS:
            output.draw_plot(DRAW_PLOTS, history, show=True)

        if SAVE_PLOTS and SAVE_PLOTS_OF_EVERY_DAY:
            fig = output.draw_parameters(predictors)
            output.save_fig(fig, plot_dir=now_str, name="Parameters.png")
            fig = output.draw_plot([output.PLOT_TYPE_BAR_ATTENDANCE, output.PLOT_TYPE_IN_BAR_CNT], history, show=False)
            output.save_fig(fig, plot_dir=now_str, name="Result.png")
            output.draw_and_save_plots(SAVE_PLOTS, history, range(DAY_CNT), plot_dir=now_str)

        if SAVE_PLOTS and not SAVE_PLOTS_OF_EVERY_DAY:
            fig = output.draw_plot(SAVE_PLOTS, history, show=False)
            if fig:
                output.save_fig(fig, plot_dir=None, name=now_str + ".png")

    average_attendance = round(sum(bar_attendance) / DAY_CNT, 2)
    upper_limit = max(bar_attendance[-20:])
    lower_limit = min(bar_attendance[-20:])
    return average_attendance, upper_limit, lower_limit


if __name__ == '__main__':
    live_life()

