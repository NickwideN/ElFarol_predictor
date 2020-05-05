"""
Некоторое введение:
Строка, начинающаяся с "!", имеет определение термина
"""

###### life config ######
"""
Представим, что вы живете в городе, где строят хороший бар, в который вы регулярно будете ходить.
Однако помимо вас в этот бар будет ходить обедать весь город в количестве MAN_CNT человек.
В этом баре находится тем лучше, чем меньше там народу.
Но есть некоторый предел MAX_MAN_CNT_WHEN_GOOD, когда в баре всё еще хорошо.
Если в баре больше людей, чем этот предел, то, тем, кто находится в баре, плохо, и дома им было бы намного лучше, чем в людном баре.
!Назовем те дни, когда в баре всё еще хорошо, успешными для бара.
И вот каждое утро с момента открытия бара каждый человек решает для себя, а стоит ли ему идти в бар сегодня.
"""

# Количество человек в городе
MAN_CNT = 10
# максимальное количество человек в баре, когда там еще хорошо
MAX_MAN_CNT_WHEN_GOOD = MAN_CNT * 0.6
# Количество дней существования бара
DAY_CNT = 200

###### man config ######
"""
Каждый человек во время предположения, сколько в баре будет человек, опирается на так называемые предикторы.

Каждый человек характеризуется набором предикторов PredictorSet, состоящий из PREDICTOR_IN_SET_CNT предикторов. 
Предиктор в таком наборе называется PredictorInSet(предиктор в наборе), не путать с обычным предиктором(о нем ниже).

Каждый предиктор в наборе советует человеку идти или не идти в бар. Способ, которым человек будет слушаться устанавливается параметром FOLLOW_TYPE

Каждый предиктор в наборе считает, сколько дней он советовал человеку правильное решение.
!Будем считать такие дни успешными для предиктора в наборе

Если в течении MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN дней подряд процент успешных дней меньше чем MIN_PERCENT_SUCCESS_FOR_PredictorInSet, то человек поменяет свой предиктор на новый случайный.
"""
# количество предикторов в наборе предикторов человека
PREDICTOR_IN_SET_CNT = 3
# предикторы в наборе предикторов уникальны?
ARE_UNIQUE_PREDICTORS_IN_SET = True

# как человек будет использовать советы предикторов?
# 0 - слушается мнению большинства предикторов
# 1 - слушаться мнения самого успешного в своем наборе предиктора. Если таких предикторов несколько, слушаться мнения большинства из самых успешных
FOLLOW_TYPE = 0

# минимальный процент успешных дней (МПУД) для PredictorInSet. Если процент успешных дней предиктора в наборе меньше МПУД MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN дней подряд и предиктор в эти дни ошибался, предиктор заменится на новый случайный
MIN_PERCENT_SUCCESS_FOR_PredictorInSet = 0.7
# Максимальное количество дней подряд с процентом ниже минимального для PredictorInSet
MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN = 3

###### predictor config ######
"""
Предиктор -- некоторая сущность, которая советует человеку идти в бар или не идти.
Каждый предиктор состоит из:
1. name -- имя предиктора
2. func -- функция, на основе которой предиктор будет советовать человеку идти в бар или нет.
Примером функции может быть 'min' - минимальное количество в баре в некоторые дни. 
Другие примеры можно посмотреть в predictors.json5
3. days -- дни, на которые будет опираться func
По примеру выше предиктор посчитает минимальное количество в дни из days и скажет, а было бы такое количество успешным для бара

Предиктор считает, сколько раз его совет оказался правильным. 
!Будем называть такие дни успешними для предикатора.

Однако процент успешных дней (ПУД) для предиктора может оказаться настолько низким, что человек не будет верить совету такого предиктора и будет следовать его совету наоборот
"""
# Поставьте этот параметр на True, чтобы человек следовал советам всех предикторов какой бы низкий их ПУД не был.
# False не гарантирует, что люди перестанут беспрекословно следовать советам всех предикторам. Для этого надо установить всем предикторам параметр can_trust_anywhere=false в predictors.json5
TRUST_PREDICTORS_ANYWHERE = True
# Минимальный ПУД для предиктора, ниже которого человек перестанет слушаться своего предиктора и будет делать всё наоборот (Работает, если CAN_TRUST_PREDICTORS_ANYWHERE=False)
MIN_PERCENT_WHEN_MAN_BELIEVE = 0.5

###### output config ######
# todo написать про выводимые данные
"""
Есть 3 графика: 
0 -- График посещаемости бара
1 -- График зависимости количества дней от числа человек в баре в этот день
2 -- Наборы предикторов у людей в определенный день
Пример (советуется):
DRAW_PLOTS = [0, 1] 
SAVE_PLOTS = [0, 1, 2]
установите [], чтобы не рисовать или не сохранять график

Графики рисуются исходя из сохраненной истории. Ниже расписано, в какой момент происходит сохранение.
"""
# какие графики рисовать графики?
DRAW_PLOTS = [0, 1]
# какие графики сохранять графики?
SAVE_PLOTS = [0, 1, 2]
# сохранять ли график за каждый день жизни бара? Если False и SAVE_PLOTS не пустой, то прога сохранит только график на последний день
SAVE_PLOTS_OF_EVERY_DAY = True

# сортировать вывод предикторов? (True, False или 'both')
SORT_PREDICTORS = True


def is_day_success(in_bar_cnt):
    """
    успешен ли день для бара сегодня
    :param in_bar_cnt: int
    :return: bool
    """
    return in_bar_cnt <= MAX_MAN_CNT_WHEN_GOOD


"""
Отследим, как меняется состояния 
    людей(P),  (состояние людей определяется их набором предикторов в этот день)
    предикторов(Pr), 
    предикторов в наборе(PrInSet),
    график посещаемости(At)
Итак, один день из жизни бара:
Состояния: P0, Pr0, PrInSet0, At0
1. День. Каждый человек решает, идти ему в бар или не идти на основе своих предикторов и следует своему решению.
Состояния: P0, Pr0, PrInSet0, At0
2. Вечер. Подсчитывается количество человек, которые пришли в бар и записывается в посещаемость.
Состояния: P0, Pr0, PrInSet0, At1
---------!!! Состояние сохраняется в историю !!!---------
3. Ночь. Каждый активный предиктор (который есть хотя бы у одного человека) подсчитывает свои активные и успешные дни
Состояния: P0, Pr1, PrInSet0, At1
4. Ночь. Каждый предиктор в наборе каждого человека подсчитывает свои активные и успешные дни
Состояние: P0, Pr1, PrInSet1, At1
5. Утро. Человек меняет неугодные ему предикторы в своём наборе.
Состояние: P1, Pr1, PrInSet1, At1
"""
