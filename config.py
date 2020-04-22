
###### life config ######
"""
Представим, что вы живем в городе, где строят хороший бар, в который вы регулярно будете ходить.
Однако помимо вас в этот бар будет ходить обедать весь город в количестве MAN_CNT человек.
В этом баре находится тем лучше, чем меньше там народу.
Но есть некоторый предел MAX_MAN_CNT_WHEN_GOOD, когда в баре всё еще хорошо.
Если в баре больше людей, чем этот предел, то, кто в баре находится плохо и дома им было бы много лучше, чем в людном баре.
И вот каждый день с момента открытия бара каждый человек предполагает, сколько будет человек в баре в этот день.
И в зависимости от своего предположения он идет или не идет в бар.
"""

# Количество человек в городе
MAN_CNT = 200
# максимальное количество человек в баре, когда там еще хорошо
MAX_MAN_CNT_WHEN_GOOD = 120
# Количество дней существования бара
DAY_CNT = 300
# Минимальный процент дней, успешных для предиктора, при которых человек будет верить предиктору (Работает при CAN_PREDICTORS_CHANGE_CONDITION=True)
MIN_PERCENT_WHEN_MAN_BELIEVE = 0.5

###### man config ######
"""
Каждый человек во время предположения, сколько в баре будет человек, опирается на так называемые предикторы.

Каждый человек характеризуется набором предикторов PredictorSet, состоящий из PREDICTOR_IN_SET_CNT предикторов. 
Предиктор в таком наборе называется PredictorInSet(предиктор в наборе), не путать с обычным предиктором.

Каждый PredictorInSet считает, сколько дней он угадывал, что надо идти в бар. 
Если PredictorInSet угадал, то этот день для него считается успешным.

Человек пойдет в бар, если большинство PredictorInSet в PredictorSet решат, что надо идти в бар.

Если в течении MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN дней процент успешных дней меньше чем MIN_PERCENT_SUCCESS_FOR_PredictorInSet, то PredictorInSet заменяется на новый случайный.
"""
# количество предикторов в наборе предикторов человека
PREDICTOR_IN_SET_CNT = 7
# предикторы в наборе предикторов уникальны?
ARE_UNIQUE_PREDICTORS_IN_SET = True

# минимальный процент успешных дней для PredictorInSet
MIN_PERCENT_SUCCESS_FOR_PredictorInSet = 0.6
# Максимальное количество дней подряд с процентом ниже минимального для PredictorInSet
MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN = 3

###### predictor config ######
"""
Каждый предиктор состоит из:
функции decide_go -- решает, стоит ли идти в бар или нет
condition -- некоторое условие
name -- имя предиктора

Предиктор считает, сколько раз выполнение условия совпадало с тем, что идти в бар стоит. 
Будем называть такие дни успешними для предикатора.
Если CAN_PREDICTORS_CHANGE_CONDITION == True, 
    то если процент успешных дней по отношению к дням, когда предиктор что-то решал, больше 50%, 
        то decide_go вернет True, если выполняется condition
            в противном случае вернет True, если condition не выполняется
"""
# Может ли предикторы менять значение своего условия на противоположное
# положение True не гарантирует включение параметра у всех предикторов
CAN_PREDICTORS_CHANGE_CONDITION = False

###### output config ######
# рисовать диаграмму количество дней, когда пришло in_bar_cnt людей в этот день?
DRAW_PLOT_in_bar_cnt = True
# рисовать график посещаемости?
DRAW_PLOT_attendance = True
# сортировать вывод предикторов? (True, False или 'both')
SORT_PREDICTORS = 'both'


def is_day_success(in_bar_cnt):
    """
    успешен ли день для бара сегодня
    :param in_bar_cnt: int
    :return: bool
    """
    return in_bar_cnt <= MAX_MAN_CNT_WHEN_GOOD - (MAN_CNT - MAX_MAN_CNT_WHEN_GOOD) * 0.01


"""
Больше про систему предикторов:

У каждого предиктора есть условие, которое определяется параментрами func и days. Каждый день, когда условие предиктора выдает правильное решение (совпадающееMAX_MAN_CNT_WHEN_GOOD с is_day_success в config.py), день считается успешным для предиктора.

Сам же предиктор выдает либо значение своего условия, либо его отрицание в зависимости от процента успешных для предиктора дней.

Если процент больше 50%, то предиктор будет выдавать то, что дает его условие, если меньше, то предиктор будет выдавать отрицание условия.

А представьте, что каждый день этот процент меняется то больше 50, то меньше 50, тогда предиктор каждый день будет выдавать разные значения, поэтому будет не постоянен, он будет ошибаться и в наборе предикторов его в конце концов заменят, из за чего на графике произойдет скачок.

Поэтому разрешать менять условие на противоположное разумно только тем предикторам, процент успешных у которого сильно меньше 50%
"""