from typing import Any, Dict, Set

from config import is_day_success, TRUST_PREDICTORS_ANYWHERE, MAN_CNT, MIN_PERCENT_WHEN_MAN_BELIEVE, SHOW_PR_PUD
import json
import re
from exceptions import FunctionIsNotSpecified

# Набор использующихся предикторов
predictors = []

with open('predictors.json5', 'r', encoding="utf8") as f:
    # Делаем из json5 обычный json (выделяем всё, что внутри самых внешних фигурных скобок)
    json_str = re.search(r'\{(?:[^q]|q)*\}\n\}', f.read()).group(0)
    predictors_json = json.loads(json_str)


class Predictor:
    def __init__(self, name, attr):
        self.name = name

        # Определим дни, на основе которых предиктор будет принимать решение стоит идти в бар или не стоит
        self.__days = "all"
        if "days" in attr:
            self.__days = attr["days"]

        # Определим функцию, на основе которой будет приниматься решение стоит идти в бар или не стоит
        func_name = ''
        if len(self.__days) == 1:
            # тут может быть совершенно любая функция, которая выдает посещаемость в заданный день, например min
            func_name = 'min'
        if "func" in attr:
            func_name = attr["func"]
        if not func_name:
            raise FunctionIsNotSpecified(self.name)
        self.__func = globals()[func_name + "_"]

        self.__trust_anywhere = True
        if "can_trust_anywhere" in attr:
            self.__trust_anywhere = attr["trust_anywhere"]

        self.__success_cnt = 0
        self.__active_cnt = 0

    def __repr__(self):
        return self.get_str_state()

    def get_func_result(self, today, bar_attendance):
        """
        :param today: сегодняшний день. (не используется для определения совета)
        :param bar_attendance: посещаемость, список. Не обязательно последний день списка -- today
        :return: Значение функции
        """
        if today == 0:
            return None
        elif self.__days == 'all':
            return self.__func(bar_attendance[:today])
        else:
            # соберем необходимые посещаемости дней
            attendance_in_days = []
            for day in self.__days:
                if today >= -day:
                    attendance_in_days.append(bar_attendance[today + day])
            if attendance_in_days:
                return self.__func(attendance_in_days)
        return None

    def decide_go(self, today, bar_attendance, trust=False):
        """
        получить совет идти или не идти в бар
        :param today: сегодняшний день. (не используется для определения совета)
        :param bar_attendance: посещаемость, список. Не обязательно последний день списка -- today
        :param trust: bool Eсли False и ПУД меньше минимального, вернет совет наоборот (если can_trust_anywhere=True)
        :return:
        """
        result = self.get_func_result(today, bar_attendance)
        advice = True if result is None else is_day_success(result)

        # Если не доверять совету, не доверять любому совету предиктора, не доверять советам любого предиктора и ПУД низкий
        # Поменяем совет
        if not trust and not self.__trust_anywhere and not TRUST_PREDICTORS_ANYWHERE and \
                self.persent_success() < MIN_PERCENT_WHEN_MAN_BELIEVE:
            advice = not advice
        return advice

    def analyze_day(self, today, bar_attendance):
        self.__active_cnt += 1
        if self.is_day_success(today, bar_attendance):
            self.__success_cnt += 1

    def is_day_success(self, today, bar_attendance):
        # Совет пердиктора был правильным?
        return is_day_success(bar_attendance[today]) == self.decide_go(today, bar_attendance, trust=True)

    def success_cnt(self):
        return self.__success_cnt

    def active_cnt(self):
        return self.__active_cnt

    def persent_success(self):
        return (self.__success_cnt / self.__active_cnt) if self.__active_cnt else 0.

    def get_trust_anywhere(self):
        return self.__trust_anywhere

    def get_str_state(self, today=None, bar_attendance=None):
        if SHOW_PR_PUD:
            state = "{} ({};{:.0%})".format(self.name, self.__active_cnt, self.persent_success())
        else:
            state = "{}".format(self.name)
        if today is not None and bar_attendance is not None:
            result = self.get_func_result(today, bar_attendance)
            if result is None:
                state += " ND"
            else:
                state += " {}".format(round(float(self.get_func_result(today, bar_attendance)), 4))
        return state

    def is_active(self, people):
        return self in get_active_predictors(people)


def get_active_predictors(people):
    active_predictors: Set[Predictor] = set()
    for man in people:
        active_predictors.update(man.get_predictors())
    return active_predictors


def upload_predictors_in_life():
    for pred_name, pred_attr in predictors_json.items():
        if "use" in pred_attr and not pred_attr["use"]:
            continue
        pred_obj = Predictor(pred_name, pred_attr)
        predictors.append(pred_obj)
    return predictors


# функции предикторов
def min_(attendance):
    return min(attendance)


def max_(attendance):
    return max(attendance)


def average_(attendance):
    return sum(attendance) / len(attendance)


def mirror_average_(attendance):
    return MAN_CNT - average_(attendance)


def median_(attendance):
    attendance = sorted(attendance)
    if len(attendance) % 2 == 1:
        return attendance[len(attendance) // 2]
    else:
        return 0.5 * (attendance[len(attendance) // 2 - 1] + attendance[len(attendance) // 2])

# последняя точка линии тренда. Тут какая то ошибка... надо исправить
# def trend_(attendance):
#     z = np.polyfit(range(len(attendance)), attendance, 1)
#     # y = x * a + b
#     y_0 = (len(attendance) - 1) * z[0] + z[1]
#     return y_0
