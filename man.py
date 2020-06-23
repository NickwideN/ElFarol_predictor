from typing import List, Set

from config import *
from predictor import predictors
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
        # Если совет пердиктора в наборе был правильным
        if is_day_success(bar_attendance[today]) == self.predictor.decide_go(today, bar_attendance, trust=True):
            self.__success_cnt += 1
            self.__day_cnt_with_percent_under_min = 0
        elif self.persent_success() < MIN_PERCENT_SUCCESS_FOR_PredictorInSet:
            self.__day_cnt_with_percent_under_min += 1

    # следующие функции нужны для уникальности предикторов в наборе
    def __eq__(self, other):
        return self.predictor == other.predictor

    def __ne__(self, other):
        return self.predictor != other.predictor

    def __hash__(self):
        return hash(self.predictor.name)

    def day_cnt_with_percent_under_min(self):
        return self.__day_cnt_with_percent_under_min

    def active_cnt(self):
        return self.__active_cnt

    def persent_success(self):
        return (self.__success_cnt / self.__active_cnt) if self.__active_cnt else 0

    def get_str_state(self):
        return "({};{:.0%};{})".format(self.__active_cnt, self.persent_success(), self.__day_cnt_with_percent_under_min)


class Man:
    predictor_set: Set or List[PredictorInSet]

    def __init__(self, name=''):
        self.name = name
        if ARE_UNIQUE_PREDICTORS_IN_SET:
            self.predictor_set = set()
        else:
            self.predictor_set = list()
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
        if FOLLOW_TYPE == 0:
            # получим то решение, за которое проголосовало большинство предикторов в наборе
            decide_go_cnt = 0
            for predictor_in_set in self.predictor_set:
                if predictor_in_set.predictor.decide_go(today, bar_attendance):
                    decide_go_cnt += 1
            decision = round(decide_go_cnt / PREDICTOR_IN_SET_CNT)
        elif FOLLOW_TYPE == 1:
            # Найдем предиктор с наибольшим процентом успехов
            max_success_pr = list(self.predictor_set)[0].predictor
            for predictor_in_set in self.predictor_set:
                if predictor_in_set.predictor.persent_success() > max_success_pr.persent_success():
                    max_success_pr = predictor_in_set.predictor
            # Сделаем список предикторов у которых наибольший процент успехов
            predictors_with_max_success_percent = []
            for predictor_in_set in self.predictor_set:
                if predictor_in_set.predictor.persent_success() == max_success_pr.persent_success():
                    predictors_with_max_success_percent.append(predictor_in_set.predictor)
            # получим то решение, за которое проголосовало большинство предикторов в полученном списке
            decide_go_cnt = 0
            for predictor in predictors_with_max_success_percent:
                if predictor.decide_go(today, bar_attendance):
                    decide_go_cnt += 1
            decision = round(decide_go_cnt / len(predictors_with_max_success_percent))
        return decision

    def analyze_day(self, today, bar_attendance):
        for predictor_in_set in self.predictor_set:
            predictor_in_set.analyze_day(today, bar_attendance)

    def update_predictors(self):
        # удаление неугодный предикторов
        if REMOVE_TYPE == 0:
            predictors_for_remove = []
            for predictor_in_set in self.predictor_set:
                if predictor_in_set.day_cnt_with_percent_under_min() > MAX_DAY_CNT_WITH_PERCENT_UNDER_MIN:
                    predictors_for_remove.append(predictor_in_set)
            for predictor_in_set in predictors_for_remove:
                self.predictor_set.remove(predictor_in_set)
        elif REMOVE_TYPE == 1:
            min_predictor_in_set = None  # предиктор в наборе, у которого минимальный ПУД
            # найдем сначала такой потенциальный предиктор
            for predictor_in_set in self.predictor_set:
                if predictor_in_set.active_cnt() > SAFE_ACTIVE_DAY_CNT:
                    min_predictor_in_set = predictor_in_set
                    break
            # А теперь найдем предиктор с min ПУД
            if min_predictor_in_set:
                for predictor_in_set in self.predictor_set:
                    if predictor_in_set.active_cnt() > SAFE_ACTIVE_DAY_CNT and predictor_in_set.persent_success() > min_predictor_in_set.persent_success():
                        min_predictor_in_set = predictor_in_set
                self.predictor_set.remove(min_predictor_in_set)
        # добавляем в набор случайные предикторы, пока их количество не будет равно PREDICTOR_IN_SET_CNT
        while len(self.predictor_set) < PREDICTOR_IN_SET_CNT:
            if ARE_UNIQUE_PREDICTORS_IN_SET:
                self.predictor_set.add(PredictorInSet())
            else:
                self.predictor_set.append(PredictorInSet())

    def is_day_success(self, today, bar_attendance):
        return self.decide_go(today, bar_attendance) == is_day_success(bar_attendance[today])

    def get_predictors(self):
        """
        Возвращает предикторы, которые используются в наборе у человека
        :return: set(Predictor)
        """
        active_predictors = set()
        for predictor_in_set in self.predictor_set:
            active_predictors.add(predictor_in_set.predictor)
        return active_predictors
