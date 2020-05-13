"""
Модуль анализа жизней бара
"""
from config import *
import output
import multiprocessing
import life
import datetime
from predictor import upload_predictors_in_life


def analyze():
    now_str = datetime.datetime.now().strftime("%Y.%m.%d %H-%M-%S")

    with multiprocessing.Pool(processes=PROCESSES_CNT) as pool:
        res_map = pool.map(life.live_life, [False for _ in range(LIVE_LIFE_CNT)])
    # Далее все значения (с постфиксом av) средние для всех прожитых жизней
    average_attendance_av = round(sum([res[0] for res in res_map]) / LIVE_LIFE_CNT, 3)
    upper_limit_av = round(sum([res[1] for res in res_map]) / LIVE_LIFE_CNT, 3)
    lower_limit_av = round(sum([res[2] for res in res_map]) / LIVE_LIFE_CNT, 3)
    with open(ANALYZE_FILE_NAME, "a") as file:
        file.write("\n============================" + now_str + "=========================\n")
        file.write("Количество прожитых жизней: {}".format(LIVE_LIFE_CNT))
        file.write(output.get_parameters_str(upload_predictors_in_life()))
        file.write("\n")
        file.write("Cредняя средняя посещаемость: {}\n".format(average_attendance_av))
        file.write("Cредний верхний предел: {}\n".format(upper_limit_av))
        file.write("Cредний нижний предел: {}\n".format(lower_limit_av))


if __name__ == '__main__':
    analyze()



