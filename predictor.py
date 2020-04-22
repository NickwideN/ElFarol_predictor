from typing import Any, Dict

from config import is_day_success, CAN_PREDICTORS_CHANGE_CONDITION, MAN_CNT, MIN_PERCENT_WHEN_MAN_BELIEVE
import json
import re

# Набор использующихся предикторов
predictors = []

with open('predictors.json5', 'r', encoding="utf8") as f:
    # Делаем из json5 обычный json (убираем комментарии)
    json_str = re.search(r'\{[^qq]*\}\n\}', f.read()).group(0)
    predictors_json = json.loads(json_str)


class Predictor:
    def __init__(self):
        self.__success_cnt = 0
        self.__active_cnt = 0
        self.name = ''
        self.can_change_condition = False
        predictors.append(self)

    def __repr__(self):
        return self.name

    def decide_go(self, today, bar_attendance):
        """
        принять решение, идти или не идти в бар
        """
        if not self.can_change_condition or not CAN_PREDICTORS_CHANGE_CONDITION or \
                (self.__active_cnt and self.__success_cnt / self.__active_cnt > MIN_PERCENT_WHEN_MAN_BELIEVE):
            return condition_go(self.name, today, bar_attendance)
        else:
            return not condition_go(self.name, today, bar_attendance)

    def analyze_day(self, today, bar_attendance):
        self.__active_cnt += 1
        if is_day_success(bar_attendance[today]) == condition_go(self.name, today, bar_attendance):
            self.__success_cnt += 1

    def success_cnt(self):
        return self.__success_cnt

    def active_cnt(self):
        return self.__active_cnt

    def persent_seccess(self):
        return (self.success_cnt() / self.active_cnt()) if self.active_cnt() else 0


def upload_predictors_in_life():
    for pred_name, pred_attr in predictors_json.items():
        if "use" in pred_attr and not pred_attr["use"]:
            continue
        pred_obj = Predictor()
        pred_obj.name = pred_name
        if "change_condition" in pred_attr:
            pred_obj.can_change_condition = pred_attr["change_condition"]


# функции для condition
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


def condition_go(predictor_name, today, bar_attendance):
    # тут len(bar_attendance) = today
    pred_attr: Dict[str, Any] = predictors_json[predictor_name]
    if "func" in pred_attr:
        func_name = pred_attr["func"]
    else:
        func_name = "min"
    if pred_attr["days"] == "all":
        return is_day_success(globals()[func_name + "_"](bar_attendance))
    earliest_day = min(pred_attr["days"])
    if today >= -earliest_day:
        attendance_in_days = [bar_attendance[today + day] for day in pred_attr["days"]]
        return is_day_success(globals()[func_name + "_"](attendance_in_days))
    return True
