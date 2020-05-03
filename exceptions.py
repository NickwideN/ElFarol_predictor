# Модуль для проверки параметров из config


class PredictorInSetCntExceedsPredictorCnt(Exception):
    def __init__(self, predictor_cnt: int = ''):
        self.message = "Количество предикторов в наборе предикторов превышает количество всех предикторов (" + str(predictor_cnt) + ")"

    def __str__(self):
        return self.message


class FunctionIsNotSpecified(Exception):
    def __init__(self, predictor_name=''):
        self.message = "Не указана функция у предиктора " + predictor_name

    def __str__(self):
        return self.message


class ArgumentsNotAssigned(Exception):
    def __init__(self, argument_name=''):
        self.message = "Аргумент " + argument_name + " не передан"

    def __str__(self):
        return self.message
