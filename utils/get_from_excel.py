import pandas as pd
import os


def get_data_from_excel(file: str):
    df = pd.read_excel("C:\\Users\\alvir\\PycharmProjects\\etpbot\\utils\\{}".format(file))
    os.remove("C:\\Users\\alvir\\PycharmProjects\\etpbot\\utils\\{}".format(file))
    data = df.values.tolist()
    res = ""
    for el in data:
        res += (f"<b>Вид продукции: {el[0]}</b>\n"
                f"<b>Наименование закупки:</b> {el[1]}\n"
                f"<b>Сумма НМЦК: </b>{el[2]}\n"
                f"<b>Дата окончания: </b>{el[3]}\n"
                f"<b>Ссылка: </b>{el[4]}\n\n")
    return res


#print(get_data_from_excel("Пример закупок для бота.xlsx"))
