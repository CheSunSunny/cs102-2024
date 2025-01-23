# Задание 1 на множества
import random

a = set()
b = set()
for i in range(10):
    a.add(random.randint(1, 16))
    b.add(random.randint(1, 16))
print(a, b)
if a == b:
    print("Множества равны")
elif a.issubset(b):
    print("Множество a является подмножеством b")
elif b.issubset(a):
    print("Множество b является подмножеством a")
elif a.intersection(b) != set():
    print("Общие элементы множеств: ", a.intersection(b))
else:
    print(a.union(b))

# Множество множеств
# a = set()
# for i in range(random.randint(1, 11)):
#     k = set()
#     for j in range(random.randint(1, 11)):
#         k.add(random.randint(1, 51))
#     a.add(k)

# Анаграммы


def isanagram(word1: str, word2: str):
    dict1, dict2 = dict(), dict()
    for k in word1:
        dict1[k] = word1.count(k)
    for k in word2:
        dict2[k] = word1.count(k)

        if word1.count(k) != word2.count(k):
            return False
    return True

# не подходит, нужно учесть количество одинаковых букв


# Кубики


def throw():
    return random.randint(1, 7) + random.randint(1, 7)


sum_frequency = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
for i in range(1000):
    sum_frequency[throw()] += 1
