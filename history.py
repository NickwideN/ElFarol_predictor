import copy


class History:
    def __init__(self):
        # dict of (day: people)
        self.people_states = {}
        self.predictors_states = {}
        self.bar_attendance = None

    def save_state(self, people, predictors, day):
        copied_predictors = copy.deepcopy(predictors)
        predictors_dict = dict([(predictor.name, predictor) for predictor in copied_predictors])
        copied_people = copy.deepcopy(people)
        for man in copied_people:
            for predictor_in_set in man.predictor_set:
                predictor_in_set.predictor = predictors_dict[predictor_in_set.predictor.name]
        self.predictors_states[day] = copied_predictors
        self.people_states[day] = copied_people

    def save_bar_attendance(self, bar_attendance):
        self.bar_attendance = bar_attendance

    def get_people_state(self, day=None):
        """
        Если day не установлен, вернет последнее состояние в истории,
            иначе состояние в день day
        """
        if day is None:
            return list(self.people_states.values())[-1]
        if day not in self.people_states:
            raise KeyError("Дня {} нет в people_states".format(day))
        return self.people_states[day]

    def get_predictors_state(self, day=None):
        """
        Если day не установлен, вернет последнее состояние в истории,
            иначе состояние в день day
        """
        if day is None:
            return list(self.predictors_states.values())[-1]
        if day not in self.predictors_states:
            raise KeyError("Дня {} нет в predictors_states".format(day))
        return self.predictors_states[day]

    # todo реализовать log_history
    def log_history(self):
        pass
