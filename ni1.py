def f(s, target):
    if target <= 0:
        return 'Значение целевой суммы должно быть больше нуля'
    if len(s) < 2:
        return 'Введите минимум два целых положительных числа'
    for i in range(len(s)):
        for j in range(len(s)):
            if isinstance(s[i], int) and isinstance(s[j], int):
                if i != j:
                    if s[i] > 0 and s[j] > 0:
                        if s[i] + s[j] == target:
                            if s[i].is_integer() == 1 and s[j].is_integer() == 1:
                                return [i, j]
                    else:
                        return 'Введите только целые положительные числа'

            else:
                return 'Введите только целые положительные числа'
    return 'Нет подходящей пары для достижения целевой суммы'
print(f([3, 3, 3, 3], 1))