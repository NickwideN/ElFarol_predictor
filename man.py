from typing import List, Set

from config import *
from predictor import predictors, condition_go
import random


class PredictorInSet:
    def __init__(self):
        """
        Предиктор в наборе предикторов человека
        """
        predictor_id = random.randint(0, len(predictors) - 1)
        self.predictor = predictors[predictor_id]
        # количество успехов
        self.__success_cnt = 0
        # количество дней, когда предиктор использовался в наборе
        self.__active_cnt = 0
        # количество дней подряд, когда процент успешных дней ниже допустимого минимального
        self.__day_cnt_with_percent_under_min = 0

    def analyze_day(self, today, bar_attendance):
        self.__active_cnt += 1
        if is_day_success(bar_attendance[today]) == condition_go(self.predictor.name, today, bar_attendance):
            self.__success_cnt += 1
            self.__day_cnt_with_percent_under_min = 0
        elif self.persent_success() < MIN_PERCENT_SUCCESS_FOR_PredictorInSet:
            self.__day_cnt_with_percent_under_min += 1

    def need_to_change(self):
        return self.__day_cnt_with_percent_under_min > MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN

    def change(self):
        """
            Поменять предиктор
        """
        self.__init__()

    # следующие функции нужны для уникальности предикторов в наборе
    def __eq__(self, other):
        return self.predictor == other.predictor

    def __ne__(self, other):
        return self.predictor != other.predictor

    def __hash__(self):
        return hash(self.predictor.name)

    def persent_success(self):
        return (self.__success_cnt / self.__active_cnt) if self.__active_cnt else 0

    def get_str_state(self):
        return "({};{:.0%};{})".format(self.__active_cnt, self.persent_success(), self.__day_cnt_with_percent_under_min)


class Man:
    predictor_set: Set or List[PredictorInSet]

    def __init__(self, name=''):
        if ARE_UNIQUE_PREDICTORS_IN_SET:
            self.predictor_set = set()
        else:
            self.predictor_set = list()
        self.name = name
        while len(self.predictor_set) < PREDICTOR_IN_SET_CNT:
            if ARE_UNIQUE_PREDICTORS_IN_SET:
                self.predictor_set.add(PredictorInSet())
            else:
                self.predictor_set.append(PredictorInSet())

    def __repr__(self):
        return str(self.name) + " " + str([pr.predictor for pr in self.predictor_set])

    def decide_go(self, today, bar_attendance):
        """
        принять решения, идти в бар или не идти
        :return: bool
        """
        decide_go_cnt = 0
        for predictor_in_set in self.predictor_set:
            if predictor_in_set.predictor.decide_go(today, bar_attendance):
                decide_go_cnt += 1
        return round(decide_go_cnt / PREDICTOR_IN_SET_CNT)

    def analyze_day(self, today, bar_attendance):
        for predictor_in_set in self.predictor_set:
            predictor_in_set.analyze_day(today, bar_attendance)
            if predictor_in_set.need_to_change():
                self.predictor_set.remove(predictor_in_set)
                while len(self.predictor_set) < PREDICTOR_IN_SET_CNT:
                    if ARE_UNIQUE_PREDICTORS_IN_SET:
                        self.predictor_set.add(PredictorInSet())
                    else:
                        self.predictor_set.append(PredictorInSet())

    def get_predictors(self):
        """
        Возвращает предикторы, которые используются в наборе у человека
        :return: set(Predictor)
        """
        active_predictors = set()
        for predictor_in_set in self.predictor_set:
            active_predictors.add(predictor_in_set.predictor)
        return active_predictors
