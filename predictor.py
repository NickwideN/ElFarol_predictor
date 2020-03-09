from config import is_day_success, MAX_MAN_CNT_WHEN_GOOD, DAY_CNT, CAN_PREDICTORS_CHANGE_CONDITION
import random

predictors = []


class Predictor:
    def __init__(self):
        self.__success_cnt = 0
        self.__active_cnt = 0
        # давать имя предикатору обязательно, так как на нем основано хеширование
        self.name = ''
        self.can_change_condition = True
        predictors.append(self)

    def __repr__(self):
        return self.name + ":\t\t\t" + str(self.__success_cnt) + " " + str(self.__active_cnt)

    def decide_go(self, today, bar_attendance):
        """
        принять решение, идти или не идти в бар
        """
        if not self.can_change_condition or not CAN_PREDICTORS_CHANGE_CONDITION or \
                (self.__active_cnt and self.__success_cnt / self.__active_cnt > 0.5):
            return self.condition_go(today, bar_attendance)
        else:
            return not self.condition_go(today, bar_attendance)

    def analyze_day(self, today, bar_attendance):
        self.__active_cnt += 1
        if is_day_success(bar_attendance[today]) == self.condition_go(today, bar_attendance):
            self.__success_cnt += 1

    def condition_go(self, today, bar_attendance):
        pass


########################################################################################################
########################################################################################################

prev_day = Predictor()


def condition_go(today, bar_attendance):
    if today >= 1:
        return is_day_success(bar_attendance[today - 1])
    return random.randint(0, 1)


prev_day.condition_go = condition_go
prev_day.name = "prev_day"

########################################################################################################

prev_prev_day = Predictor()


def condition_go(today, bar_attendance):
    if today >= 2:
        return is_day_success(bar_attendance[today - 2])
    return random.randint(0, 1)


prev_prev_day.condition_go = condition_go
prev_prev_day.name = "prev_prev_day"

########################################################################################################

average_3_last_days = Predictor()


def condition_go(today, bar_attendance):
    if today >= 3:
        return is_day_success(sum(bar_attendance[today - 3:today]) / 3)
    return random.randint(0, 1)


average_3_last_days.condition_go = condition_go
average_3_last_days.name = "average_3_last_days"

########################################################################################################

average_4_last_days = Predictor()


def condition_go(today, bar_attendance):
    if today >= 4:
        return is_day_success(sum(bar_attendance[today - 4:today]) / 4)
    return random.randint(0, 1)


average_4_last_days.condition_go = condition_go
average_4_last_days.name = "average_4_last_days"

########################################################################################################

average_5_last_days = Predictor()


def condition_go(today, bar_attendance):
    if today >= 5:
        return is_day_success(sum(bar_attendance[today - 5:today]) / 5)
    return random.randint(0, 1)


average_5_last_days.condition_go = condition_go
average_5_last_days.name = "average_5_last_days"

########################################################################################################

average_6_last_days = Predictor()


def condition_go(today, bar_attendance):
    if today >= 6:
        return is_day_success(sum(bar_attendance[today - 6:today]) / 6)
    return random.randint(0, 1)


average_6_last_days.condition_go = condition_go
average_6_last_days.name = "average_6_last_days"

########################################################################################################

# for i in range(2, DAY_CNT):
#     average_last_days = Predictor()
#
#
#     def condition_go(today, bar_attendance):
#         last_day_cnt = random.randint(2, DAY_CNT)
#         if today >= last_day_cnt:
#             return is_day_success(sum(bar_attendance[today - last_day_cnt:today]) / last_day_cnt)
#         return True
#
#
#     average_last_days.condition_go = condition_go
