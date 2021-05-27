"""

G. Интересное путешествие

Не секрет, что некоторые программисты очень любят путешествовать.
Хорошо всем известный программист Петя тоже очень любит путешествовать,
посещать музеи и осматривать достопримечательности других городов.

Для перемещений между из города в город он предпочитает использовать машину.
При этом он заправляется только на станциях в городах, но не на станциях
по пути. Поэтому он очень аккуратно выбирает маршруты, чтобы машина
не заглохла в дороге. А ещё Петя очень важный член команды, поэтому
он не может себе позволить путешествовать слишком долго. Он решил написать
программу, которая поможет ему с выбором очередного путешествия.
Но так как сейчас у него слишком много других задач, он попросил
вас помочь ему.

Расстояние между двумя городами считается как сумма модулей разности
по каждой из координат. Дороги есть между всеми парами городов.


Формат ввода

В первой строке входных данных записано количество городов n (2≤n≤1000).
В следующих n строках даны два целых числа: координаты каждого города,
не превосходящие по модулю миллиарда. Все города пронумерованы
числами от 1 до n в порядке записи во входных данных.

В следующей строке записано целое положительное число k, не превосходящее
двух миллиардов, — максимальное расстояние между городами,
которое Петя может преодолеть без дозаправки машины.

В последней строке записаны два различных числа — номер города,
откуда едет Петя, и номер города, куда он едет.


Формат вывода

Если существуют пути, удовлетворяющие описанным выше условиям,
то выведите минимальное количество дорог, которое нужно проехать,
чтобы попасть из начальной точки маршрута в конечную.
Если пути не существует, выведите -1.


Пример 1
Ввод:
7
0 0
0 2
2 2
0 -2
2 -2
2 -1
2 1
2
1 3
	
Вывод:
2


Пример 2
Ввод:
4
0 0
1 0
0 1
1 1
2
1 4

Вывод:
1


Задача: G.Интересное путешествие
Компилятор: Python 3.7.3
Вердикт: Превышен лимит времени исполнения
Статус: Частичное решение
№	Вердикт	Ресурсы	Баллы
	1	ok	46ms / 3.95Mb	-
	2	ok	47ms / 3.95Mb	-
	3	ok	47ms / 3.95Mb	-
	4	ok	47ms / 3.94Mb	-
	5	ok	47ms / 3.95Mb	-
	6	ok	47ms / 3.97Mb	-
	7	ok	47ms / 3.95Mb	-
	8	ok	47ms / 3.95Mb	-
	9	ok	47ms / 3.96Mb	-
	10	ok	47ms / 3.96Mb	-
	11	ok	47ms / 3.95Mb	-
	12	ok	47ms / 3.95Mb	-
	13	ok	47ms / 3.95Mb	-
	14	ok	371ms / 11.49Mb	-
	15	time-limit-exceeded	1.09s / 16.21Mb	-

"""

import sys
import math


def distance_t(t1 :dict, t2 :dict):
    return math.sqrt(
        (t2["x"] - t1["x"]) ** 2 + (t2["y"] - t1["y"]) ** 2)


def foo(towns :dict, t_from :dict, t_to :dict, t_exclude: list):
    result_list = []
    self_idx = t_from["idx"]
    dest_idx = t_to["idx"]
    t_exclude_new = list(t_exclude)  # new list for save old
    t_exclude_new.append(self_idx)  # self exclude
    for near_town in t_from["L"].keys():
        if near_town == dest_idx:
            result_list.append([near_town, ])  # one step to win
        else:
            if near_town not in t_exclude_new:
                result = foo(
                    towns=towns, t_from=towns[near_town],
                    t_to=t_to, t_exclude=t_exclude_new)
                if result is None:
                    t_exclude_new.append(near_town)  # block
                else:
                    for x in result:
                        x.insert(0, near_town)  # claim leg
                    result_list.extend(result)
    del t_exclude_new
    if len(result_list) > 0:
        return result_list
    del result_list
    return None


towns = dict()
town_len = int(sys.stdin.readline().strip())  # read len

for i in range(town_len):
    xv, yv = sys.stdin.readline().strip().split(' ')  # read x y
    towns[i+1] = {"x": int(xv), "y": int(yv), "idx": i+1, "L": {}, }

tank_len = int(sys.stdin.readline().strip())  # read tank
tovn_1v, tovn_2v = sys.stdin.readline().strip().split(' ')  # read from to

for town_i_k, town_i_v in towns.items():
    for town_j_k, town_j_v in towns.items():
        distance = distance_t(t1=town_i_v, t2=town_j_v)
        if (distance <= tank_len) and (distance > 0):
            town_i_v["L"][town_j_k] = distance
            town_j_v["L"][town_i_k] = distance

# print("towns:", towns)
# print("tank_len:", tank_len)
# print("tovn_1v:", tovn_1v, "; tovn_2v", tovn_2v)

result = foo(
    towns=towns, t_from=towns[int(tovn_1v)],
    t_to=towns[int(tovn_2v)], t_exclude=[])

if result is None:
    print(-1)
else:
    # print("DEBUG", result)
    print(min([len(x) for x in result]))
