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

    in_bar_cnt_day_cnt_map = {}

    now_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # todo надо поменять логику. В output.draw_plots передавать все 3 kwargsа, а рисовать то, что пользователь отметит
    save_plots_kwargs = dict()
    if 'attendance' in SAVE_PLOTS:
        save_plots_kwargs['bar_attendance'] = bar_attendance
    if 'in_bar_cnt' in SAVE_PLOTS:
        save_plots_kwargs['in_bar_cnt_day_cnt_map'] = in_bar_cnt_day_cnt_map
    if 'people_state' in SAVE_PLOTS:
        save_plots_kwargs['people'] = people

    if save_plots_kwargs and SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_parameters()
        output.save_fig(fig, plot_dir=now_str, name="Parameters.png")

    for day in range(DAY_CNT):
        output.print_progress(day, DAY_CNT)
        live_day(day, people, bar_attendance)

        # todo Надо добавить историю и исходя из нее сторить графики и после того как вся жизнь прошла
        if bar_attendance[day] not in in_bar_cnt_day_cnt_map:
            in_bar_cnt_day_cnt_map[bar_attendance[day]] = 0
        in_bar_cnt_day_cnt_map[bar_attendance[day]] += 1
        if SAVE_PLOTS_OF_EVERY_DAY:
            fig = output.draw_plots(**save_plots_kwargs, show=False)
            if fig:
                output.save_fig(fig, plot_dir=now_str, name="day" + str(day) + ".png")
    print()

    output.print_bar_attandance(bar_attendance)

    print()
    output.print_day_cnt_in_bar_cnt_map(in_bar_cnt_day_cnt_map)

    print()
    output.print_predictors(predictors)

    if save_plots_kwargs and SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_plots(bar_attendance=bar_attendance, in_bar_cnt_day_cnt_map=in_bar_cnt_day_cnt_map, show=False)
        output.save_fig(fig, plot_dir=now_str, name="Result.png")

    if not SAVE_PLOTS_OF_EVERY_DAY:
        fig = output.draw_plots(**save_plots_kwargs, show=False)
        if fig:
            output.save_fig(fig, plot_dir=None, name=now_str + ".png")

    save_draw_kwargs = dict()
    if 'attendance' in DRAW_PLOTS:
        save_draw_kwargs['bar_attendance'] = bar_attendance
    if 'in_bar_cnt' in DRAW_PLOTS:
        save_draw_kwargs['in_bar_cnt_day_cnt_map'] = in_bar_cnt_day_cnt_map
    if 'people_state' in DRAW_PLOTS:
        save_draw_kwargs['people'] = people
    output.draw_plots(**save_draw_kwargs)
