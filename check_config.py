# Модуль для проверки параметров из config

from config import *
from predictor import predictors


class PredictorInSetCntExceedsPredictorCnt(Exception):
    def __init__(self, predictor_cnt: int = ''):
        self.message = "Количество предикторов в наборе предикторов превышает количество всех предикторов (" + str(predictor_cnt) + ")"

    def __str__(self):
        return self.message


def check_config_parameters():
    if PREDICTOR_IN_SET_CNT > len(predictors):
        raise PredictorInSetCntExceedsPredictorCnt(len(predictors))
