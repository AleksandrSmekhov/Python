#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math
import itertools
import random
import os
import sys


def read_input(input_path):
    input_vector = []
    classes = []
    
    input_exist = os.path.exists(input_path)
    if input_exist:
        with open(input_path, 'r') as file:
            i = 0
            for line in file:
                if i == 0:
                    for var in range(len(line) - 1):
                        input_vector.append(int(line[var]))
                    i += 1
                elif i == 1:
                    for var in line.split(','):
                        classes.append(var)
                    i += 1

        input_vector = np.array(input_vector, dtype = np.int32)
        classes = np.array(classes)
        
    return input_vector, classes





#Проверка на Т0, Т1, Т2
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
T_type - 0: T0, 1: T1, 2: T2
"""
def T0_T1_T2_check(vector, check_type, T_type):
    check_pos, correct_digit, wrong_digit_1, wrong_digit_2 = 0, 0, 1, 2
    
    if T_type == 1:
        check_pos, correct_digit, wrong_digit_1, wrong_digit_2 = int(len(vector) / 2), 1, 0, 2
    elif T_type == 2:
        check_pos, correct_digit, wrong_digit_1, wrong_digit_2 = len(vector) - 1, 2, 0, 1
    
    if check_type == 0:
        if vector[check_pos] == 3:
            return 2
        elif vector[check_pos] != correct_digit:
            return 0
        else:
            return 1
        
    elif check_type == 1:
        add_amount = 0
        if (vector[check_pos] != wrong_digit_1) and (vector[check_pos] != wrong_digit_2):
            add_amount += 1
            for i in range(len(vector)):
                if (vector[i] == 3) and (i != check_pos):
                    add_amount *= 3
        return add_amount
    
    elif check_type == 2:
        poss_vectors = []
        
        if (vector[check_pos] != wrong_digit_1) and (vector[check_pos] != wrong_digit_2):
            poss_vectors.append(np.copy(vector))
            
            for i in range(len(vector)):
                if i == check_pos and vector[i] == 3:
                    for temp in poss_vectors:
                        temp[i] = correct_digit
                elif vector[i] == 3:
                    new_vectors = []
                    for temp in poss_vectors:
                        temp[i] = 0
                        new_vectors.append(np.copy(temp))
                        
                        temp[i] = 1
                        new_vectors.append(np.copy(temp))
                        
                        temp[i] = 2
                        new_vectors.append(np.copy(temp))
                        
                    poss_vectors = new_vectors
                    
        poss_vectors = np.array(poss_vectors)
        return poss_vectors





#Построение векторов из двух значений
"""
Вход:
vector - вектор значений
а - первое значение
b - второе значение
"""
def build_vectors(vector, a, b):
    poss_vectors = []
    poss_vectors.append(np.copy(vector))
    
    for i in range(len(vector)):
        if vector[i] == 3:
            new_vectors = []
            for temp in poss_vectors:
                temp[i] = a
                new_vectors.append(np.copy(temp))
                        
                temp[i] = b
                new_vectors.append(np.copy(temp))
                        
            poss_vectors = new_vectors
    
    return poss_vectors

#Проверка на B
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
"""
def B_check(vector, check_type):
    pos_digit = []
    for i in range(len(vector)):
        if vector[i] not in pos_digit:
            pos_digit.append(vector[i])
    
    res = 0 
    
    if len(vector) == 3:
        res = 1
    elif len(pos_digit) == 4:
        res = 0
    elif len(pos_digit) == 3:
        if 3 in pos_digit:
            res = 2
        else:
            res = 0
    else:
        if 3 in pos_digit:
            res = 2
        else:
            res = 1
    
    if check_type == 0:
        return res
    
    elif check_type == 1:
        add_amount = 1
        if len(vector) == 3:
            for val in vector:
                if val == 3:
                    add_amount *= 3
        elif res == 0:
            add_amount = 0
        elif res == 2:
            for val in vector:
                if val == 3:
                    add_amount *= 2
            if len(pos_digit) == 2:
                add_amount *= 2
                add_amount -= 1
            if len(pos_digit) == 1:
                add_amount -= 1
                add_amount *= 3
        
        return add_amount
    
    elif check_type == 2:
        poss_vectors = []
        
        if len(vector) == 3:
            poss_vectors.append(vector)
            for i in range(len(vector)):
                if vector[i] == 3:
                    new_vectors = []
                    for temp in poss_vectors:
                        temp[i] = 0
                        new_vectors.append(np.copy(temp))
                        
                        temp[i] = 1
                        new_vectors.append(np.copy(temp))
                        
                        temp[i] = 2
                        new_vectors.append(np.copy(temp))
                        
                    poss_vectors = new_vectors
        elif res == 1:
            poss_vectors.append(vector)
        elif res == 2:
            if len(pos_digit) == 1:
                poss_vectors.extend(build_vectors(vector, 0, 1))
                poss_vectors.extend(build_vectors(vector, 0, 2)[1:])
                poss_vectors.extend(build_vectors(vector, 1, 2)[1:-1])
            elif len(pos_digit) == 2:
                a = 0
                for val in pos_digit:
                    if val != 3:
                        a = val
                if a == 0:
                    b, c = 1, 2
                elif a == 1:
                    b, c = 0, 2
                elif a == 2:
                    b, c = 0, 1
                    
                poss_vectors.extend(build_vectors(vector, a, b))
                poss_vectors.extend(build_vectors(vector, a, c)[1:])
            elif len(pos_digit) == 3:
                a, b = -1, -1
                for val in pos_digit:
                    if (val != 3) and (a == -1):
                        a = val
                    elif (val != 3) and (b == -1):
                        b = val
                poss_vectors.extend(build_vectors(vector, a, b))
        
        poss_vectors = np.array(poss_vectors)
        return poss_vectors





#Построение возможных векторов
"""
Вход:
vector - вектор значений
"""
def build_poss_vectors(vector, f_digit, s_digit, T_type, isType = False):
    poss_vectors = []
    poss_vectors.append(np.copy(vector))
    
    if len(vector) == 3:
        for i in range(len(vector)):
            if vector[i] == 3:
                new_vectors = []
                if i == T_type or isType:
                    for temp in poss_vectors:
                        temp[i] = 0
                        new_vectors.append(np.copy(temp))
                        temp[i] = 1
                        new_vectors.append(np.copy(temp))
                        temp[i] = 2
                        new_vectors.append(np.copy(temp))
                    poss_vectors = new_vectors
                else:
                    for temp in poss_vectors:
                        temp[i] = f_digit
                        new_vectors.append(np.copy(temp))

                        temp[i] = s_digit
                        new_vectors.append(np.copy(temp))
                    poss_vectors = new_vectors
    else:
        step = math.ceil(len(vector) / 3)
        k = 0
        for i in range(0, len(vector), step):
            temp = np.copy(vector[i:i + step])
            if 3 in temp:
                if k == T_type:
                    isType = True
                else:
                    isType = False
                temp_vectors = build_poss_vectors(temp, f_digit, s_digit, T_type, isType)
                new_vectors = []
                for vec in poss_vectors:
                    for new_vec in temp_vectors:
                        for j in range(len(new_vec)):
                            vec[i + j] = new_vec[j]
                        new_vectors.append(np.copy(vec))
                poss_vectors = new_vectors
            k += 1
    return poss_vectors
            
        
    

#Проверка на T12, T02, T01
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
T_type - 0: T12, 1: T02, 2: T01
"""
def T12_T02_T01_check(vector, check_type, T_type):
    f_digit, s_digit = -1, -1
    if T_type == 0:
        f_digit, s_digit = 1, 2
    elif T_type == 1:
        f_digit, s_digit = 0, 2
    elif T_type == 2:
        f_digit, s_digit = 0, 1
    
    res = 1
    if check_type == 1:
        add_amount = 1
    if len(vector) != 3:
        step = math.ceil(len(vector) / 3)
        j = 0
        res_arr = []
        for i in range(0, len(vector), step):
            temp = np.copy(vector[i:i + step])
            if (j == f_digit) or (j == s_digit):
                res_arr.append(T12_T02_T01_check(temp, 0, T_type))
                if check_type == 1: 
                    add_amount *= T12_T02_T01_check(temp, 1, T_type)
            elif check_type == 1:
                for ii in range(len(temp)):
                    if temp[ii] == 3:
                        add_amount *= 3
            j += 1
        if 0 in res_arr:
            res = 0
        elif 2 in res_arr:
            res = 2
    else:
        if (vector[f_digit] == T_type) or (vector[s_digit] == T_type):
            res = 0
            if check_type == 1:
                add_amount *= 0
        elif 3 in vector:
            if (vector[f_digit] == 3) or (vector[s_digit] == 3):
                res = 2
            if check_type == 1:
                for i in range(len(vector)):
                    if (i == T_type) and (vector[i] == 3):
                        add_amount *= 3
                    elif vector[i] == 3:
                        add_amount *= 2
    
    if check_type == 0:
        return res
    
    elif check_type == 1:
        return add_amount
    
    elif check_type == 2:
        poss_vectors = []
        
        if (res == 1) and (3 not in vector):
            poss_vectors.append(vector)
        elif (res == 1) or (res == 2):
            poss_vectors = build_poss_vectors(vector, f_digit, s_digit, T_type)
            
        poss_vectors = np.array(poss_vectors)
        return poss_vectors





#Проверка на S
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
"""
def S_check(vector, check_type):
    len_vec = len(vector)
    step = math.ceil(len_vec / 3)
    n = 0
    while len_vec != 1:
        len_vec = math.ceil(len_vec / 3)
        n += 1
        
    sets = list(itertools.product(range(3), repeat = n))
    sets = np.array(sets)
    
    if check_type == 0:
        res_arr = []
        for i in range(step):
            sft1 = (sets[i] + 1) % 3
            sft2 = (sets[i] + 2) % 3
                
            j1, j2 = 0, 0
            for j in range(len(vector) - step):
                if np.array_equal(sets[step + j], sft1):
                    j1 = step + j
                if np.array_equal(sets[step + j], sft2):
                    j2 = step + j
            
            res, res1, res2 = 0, 0, 0
            if vector[i] != 3:
                if vector[j1] == (vector[i] + 1) % 3:
                    res1 = 1
                elif vector[j1] == 3:
                    res1 = 2
                if vector[j2] == (vector[i] + 2) % 3:
                    res2 = 1
                elif vector[j2] == 3:
                    res2 = 2
            else:
                if (vector[j2] == (vector[j1] + 1) % 3) or (vector[j2] == 3) or (vector[j1] == 3):
                    res1 = 2
                    res2 = 2
            
            if (res1 == 0) or (res2 == 0):
                res = 0
                res_arr.append(res)
                break
            elif (res1 == 2) or (res2 == 2):
                res = 2
            else:
                res = 1
            res_arr.append(res)
        
        if 0 in res_arr:
            return 0
        elif 2 in res_arr:
            return 2
        else:
            return 1
        
    elif check_type == 1:
        res = S_check(vector, 0)
        if res != 2:
            return res
        else:
            add_amount = 1
            for i in range(step):
                if vector[i] == 3:
                    sft1 = (sets[i] + 1) % 3
                    sft2 = (sets[i] + 2) % 3
                    
                    j1, j2 = 0, 0
                    for j in range(len(vector) - step):
                        if np.array_equal(sets[step + j], sft1):
                            j1 = step + j
                        if np.array_equal(sets[step + j], sft2):
                            j2 = step + j
                    
                    if (vector[j1] == 3) and (vector[j2] == 3):
                        add_amount *= 3
            
            return add_amount
        
    elif check_type == 2:
        poss_vectors = []
        res = S_check(vector, 0)
        
        if res == 1:
            poss_vectors.append(vector)
        elif res == 2:
            poss_vectors.append(np.copy(vector))
            for i in range(step):
                sft1 = (sets[i] + 1) % 3
                sft2 = (sets[i] + 2) % 3
                    
                j1, j2 = 0, 0
                for j in range(len(vector) - step):
                    if np.array_equal(sets[step + j], sft1):
                        j1 = step + j
                    if np.array_equal(sets[step + j], sft2):
                        j2 = step + j
                if vector[i] == 3:
                    if (vector[j1] == 3) and (vector[j2] == 3):
                        new_vectors = []
                        for temp in poss_vectors:
                            for k in range(3):
                                temp[i] = k
                                temp[j1] = (k + 1) % 3
                                temp[j2] = (k + 2) % 3
                                new_vectors.append(np.copy(temp))
                        poss_vectors = new_vectors
                    elif vector[j1] != 3:
                        new_vectors = []
                        for temp in poss_vectors:
                            temp[i] = (vector[j1] + 2) % 3
                            temp[j2] = (vector[j1] + 1) % 3
                            new_vectors.append(np.copy(temp))
                        poss_vectors = new_vectors
                    else:
                        new_vectors = []
                        for temp in poss_vectors:
                            temp[i] = (vector[j2] + 1) % 3
                            temp[j1] = (vector[j2] + 2) % 3
                            new_vectors.append(np.copy(temp))
                        poss_vectors = new_vectors
                else:
                    new_vectors = []
                    for temp in poss_vectors:
                        temp[j1] = (vector[i] + 1) % 3
                        temp[j2] = (vector[i] + 2) % 3
                        new_vectors.append(np.copy(temp))
                    poss_vectors = new_vectors
        
        
        poss_vectors = np.array(poss_vectors)
        return poss_vectors





# Приведение вектора к "нормальному" виду
"""
vector - вектор значений
M_type - 0: M0, 1: M1, 2: M2
"""
def normalize(vector, M_type):
    new_vector = np.zeros(len(vector), dtype = np.int32)

    if len(vector) == 3:
        new_vector[0] = vector[(M_type - 1) % 3]
        new_vector[1] = vector[M_type]
        new_vector[2] = vector[(M_type + 1) % 3]
        
        for i in range(len(new_vector)):
            if new_vector[i] == M_type:
                new_vector[i] = 5
            elif new_vector[i] == (M_type - 1) % 3:
                new_vector[i] = 4
            elif new_vector[i] == (M_type + 1) % 3:
                new_vector[i] = 6
            
    else:
        j = 0
        step = math.ceil(len(vector) / 3)
        for i in range(0, len(vector), step):
            temp = np.copy(vector[i:i + step])
            if j == M_type:
                new_vector[step: 2*step] = normalize(temp, M_type)
            elif j == (M_type - 1) % 3:
                new_vector[0:step] = normalize(temp, M_type)
            elif j == (M_type + 1) % 3:
                new_vector[2*step:3*step] = normalize(temp, M_type)
            j += 1
            
    return new_vector

# Приведение вектора к изначальному виду
"""
vector - нормализованный вектор значений
M_type - 0: M0, 1: M1, 2: M2
"""
def back_normalize(vector, M_type):
    new_vector = np.zeros(len(vector), dtype = np.int32)

    if len(vector) == 3:
        new_vector[(M_type - 1) % 3] = vector[0]
        new_vector[M_type] = vector[1]
        new_vector[(M_type + 1) % 3] = vector[2]
        
        for i in range(len(new_vector)):
            if new_vector[i] == 5:
                new_vector[i] = M_type
            elif new_vector[i] == 4:
                new_vector[i] = (M_type - 1) % 3
            elif new_vector[i] == 6:
                new_vector[i] = (M_type + 1) % 3
            
    else:
        step = math.ceil(len(vector) / 3)
        if M_type == 0:
            new_vector[0:step] = back_normalize(np.copy(vector[step: 2*step]), M_type)
            new_vector[step: 2*step] = back_normalize(np.copy(vector[2*step:3*step]), M_type)
            new_vector[2*step:3*step] = back_normalize(np.copy(vector[0:step]), M_type)
        elif M_type == 1:
            new_vector[0:step] = back_normalize(np.copy(vector[0:step]), M_type)
            new_vector[step: 2*step] = back_normalize(np.copy(vector[step: 2*step]), M_type)
            new_vector[2*step:3*step] = back_normalize(np.copy(vector[2*step:3*step]), M_type)
        elif M_type == 2:
            new_vector[0:step] = back_normalize(np.copy(vector[2*step:3*step]), M_type)
            new_vector[step: 2*step] = back_normalize(np.copy(vector[0:step]), M_type)
            new_vector[2*step:3*step] = back_normalize(np.copy(vector[step: 2*step]), M_type)
            
    return new_vector

#Нахождение возможных значений
"""
Вход:
low - нижнее значение
high - верхнее значение
"""
def possible_M_values(low, high):
    poss_val = []
    while low <= high:
        poss_val.append(low)
        low += 1
    return poss_val

#Построение возможных векторов М
"""
Вход:
vector - вектор значений
"""
def build_M_vectors(vector):
    poss_vectors = []
    is_error = False
    step = math.ceil(len(vector) / 3)
    temp1 = np.copy(vector[0:step])
    temp2 = np.copy(vector[step:2*step])
    temp3 = np.copy(vector[2*step:3*step])
    new_vectors = []
    new_vectors.append(np.copy(vector))
    for i in range(len(temp1)):
        if ((temp1[i] > temp2[i]) or (temp2[i] > temp3[i])) and temp1[i] != 3 and temp2[i] != 3 and temp3[i] != 3:
            is_error = True
            break 
        elif (temp1[i] <= temp2[i]) and temp3[i] == 3 and temp1[i] != 3 and temp2[i] != 3:
            temp_vectors = []
            poss_vals = possible_M_values(temp1[i], 6)
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i + 2*step] = val
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp1[i] <= temp3[i]) and temp2[i] == 3 and temp1[i] != 3 and temp3[i] != 3:
            temp_vectors = []
            poss_vals = possible_M_values(temp1[i], temp3[i])
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i + step] = val
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp2[i] <= temp3[i]) and temp1[i] == 3 and temp2[i] != 3 and temp3[i] != 3:
            temp_vectors = []
            poss_vals = possible_M_values(4, temp2[i])
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i] = val
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif temp1[i] == 3 and temp2[i] == 3 and temp3[i] != 3:
            temp_vectors = []
            poss_vals = possible_M_values(4, temp3[i])
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i + step] = val
                    poss_vals1 = possible_M_values(4, val)

                    for val1 in poss_vals1:
                        temp[i] = val1
                        temp_vectors.append(np.copy(temp))
                
            new_vectors = temp_vectors
        elif temp1[i] == 3 and temp2[i] != 3 and temp3[i] == 3:
            temp_vectors = []
            poss_vals = possible_M_values(4, temp2[i])
            poss_vals1 = possible_M_values(temp2[i], 6)
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i] = val

                    for val1 in poss_vals1:
                        temp[i + 2*step] = val1
                        temp_vectors.append(np.copy(temp))
                
            new_vectors = temp_vectors
        elif temp1[i] != 3 and temp2[i] == 3 and temp3[i] == 3:
            temp_vectors = []
            poss_vals = possible_M_values(temp1[i], 6)
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i + step] = val
                    poss_vals1 = possible_M_values(val, 6)

                    for val1 in poss_vals1:
                        temp[i + 2*step] = val1
                        temp_vectors.append(np.copy(temp))
                
            new_vectors = temp_vectors
        elif temp1[i] == 3 and temp2[i] == 3 and temp3[i] == 3:
            temp_vectors = []
            poss_vals = possible_M_values(4, 6)
            
            for temp in new_vectors:
                for val in poss_vals:
                    temp[i] = val
                    poss_vals1 = possible_M_values(val, 6)

                    for val1 in poss_vals1:
                        temp[i + step] = val1
                        poss_vals2 = possible_M_values(val1, 6)

                        for val2 in poss_vals2:
                            temp[i + 2*step] = val2
                            temp_vectors.append(np.copy(temp))
                            
            new_vectors = temp_vectors
            
    if not is_error:
        poss_vectors = new_vectors
    return poss_vectors

#Проверка на M0, M1, M2
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
M_type - 0: M0, 1: M1, 2: M2
"""
def M0_M1_M2_check(vector, check_type, M_type, first_in = True):
    norm_vector = np.copy(vector)
    if first_in:
        norm_vector = normalize(vector, M_type)
    if 3 not in norm_vector:
        res = 0
        
        if len(norm_vector) == 3:
            if (norm_vector[0] <= norm_vector[1]) and (norm_vector[1] <= norm_vector[2]):
                res = 1
        else:
            step = math.ceil(len(norm_vector) / 3)
            temp1 = np.copy(norm_vector[0:step])
            temp2 = np.copy(norm_vector[step:2*step])
            temp3 = np.copy(norm_vector[2*step:3*step])
            
            arr_res = []
            for i in range(len(temp1)):
                if (temp1[i] <= temp2[i]) and (temp2[i] <= temp3[i]):
                    arr_res.append(1)
                else:
                    arr_res.append(0)
            
            if 0 not in arr_res:
                res = 1
            
            arr_res = []
            if res == 1:
                arr_res.append(M0_M1_M2_check(temp1, 0, M_type, False))
                arr_res.append(M0_M1_M2_check(temp2, 0, M_type, False))
                arr_res.append(M0_M1_M2_check(temp3, 0, M_type, False))
                if 0 in arr_res:
                    res = 0
        
        if check_type == 0 or check_type == 1:
            return res
        elif check_type == 2:
            poss_vectors = []
            if res == 1 and first_in:
                denorm_vector = back_normalize(norm_vector, M_type)
                poss_vectors.append(denorm_vector)
            elif res == 1:
                poss_vectors.append(norm_vector)
            poss_vectors = np.array(poss_vectors)
            return poss_vectors
    else:
        final_vectors = []
        poss_vectors = build_M_vectors(norm_vector)
        
        for vec in poss_vectors:
            res = M0_M1_M2_check(vec, 0, M_type, False)
            if res == 1:
                final_vectors.append(back_normalize(vec, M_type))
        
        if check_type == 0:
            if len(final_vectors) != 0:
                return 2
            else:
                return 0
        elif check_type == 1:
            return len(final_vectors)
        elif check_type == 2:
            final_vectors = np.array(final_vectors)
            return final_vectors





# Приведение вектора к "нормальному" виду
"""
vector - вектор значений
U_type - 0: U0, 1: U1, 2: U2
"""
def U_normalize(vector, U_type):
    new_vector = np.zeros(len(vector), dtype = np.int32)
    f_digit, s_digit = -1, -1
    if U_type == 0:
        f_digit, s_digit = 1, 2
    elif U_type == 1:
        f_digit, s_digit = 0, 2
    elif U_type == 2:
        f_digit, s_digit = 0, 1
    

    if len(vector) == 3:
        new_vector[0] = vector[U_type]
        new_vector[1] = vector[f_digit]
        new_vector[2] = vector[s_digit]
            
    else:
        j = 0
        step = math.ceil(len(vector) / 3)
        for i in range(0, len(vector), step):
            temp = np.copy(vector[i:i + step])
            if j == U_type:
                new_vector[0: step] = U_normalize(temp, U_type)
            elif j == f_digit:
                new_vector[step:2*step] = U_normalize(temp, U_type)
            elif j == s_digit:
                new_vector[2*step:3*step] = U_normalize(temp, U_type)
            j += 1
            
    return new_vector

# Приведение вектора к изначальному виду
"""
vector - нормализованный вектор значений
U_type - 0: U0, 1: U1, 2: U2
"""
def U_back_normalize(vector, U_type):
    new_vector = np.zeros(len(vector), dtype = np.int32)
    f_digit, s_digit = -1, -1
    if U_type == 0:
        f_digit, s_digit = 1, 2
    elif U_type == 1:
        f_digit, s_digit = 0, 2
    elif U_type == 2:
        f_digit, s_digit = 0, 1

    if len(vector) == 3:
        new_vector[U_type] = vector[0]
        new_vector[f_digit] = vector[1]
        new_vector[s_digit] = vector[2]
            
    else:
        step = math.ceil(len(vector) / 3)
        if U_type == 0:
            new_vector = np.copy(vector)
        elif U_type == 1:
            new_vector[0:step] = U_back_normalize(np.copy(vector[step:2*step]), U_type)
            new_vector[step: 2*step] = U_back_normalize(np.copy(vector[0: step]), U_type)
            new_vector[2*step: 3*step] = U_back_normalize(np.copy(vector[2*step: 3*step]), U_type)
        elif U_type == 2:
            new_vector[0:step] = U_back_normalize(np.copy(vector[step:2*step]), U_type)
            new_vector[step: 2*step] = U_back_normalize(np.copy(vector[2*step:3*step]), U_type)
            new_vector[2*step:3*step] = U_back_normalize(np.copy(vector[0: step]), U_type)
            
    return new_vector

#Построение возможных векторов U
"""
Вход:
vector - вектор значений
U_type - 0: U0, 1: U1, 2: U2
"""
def build_U_vectors(vector, U_type):
    poss_vectors = []
    is_error = False
    step = math.ceil(len(vector) / 3)
    temp1 = np.copy(vector[0:step])
    temp2 = np.copy(vector[step:2*step])
    temp3 = np.copy(vector[2*step:3*step])
    new_vectors = []
    new_vectors.append(np.copy(vector))
    f_digit, s_digit = -1, -1
    if U_type == 0:
        f_digit, s_digit = 1, 2
    elif U_type == 1:
        f_digit, s_digit = 0, 2
    elif U_type == 2:
        f_digit, s_digit = 0, 1
    
    for i in range(len(temp2)):
        if (temp2[i] != temp3[i]) and ((temp2[i] == U_type) or (temp3[i] == U_type)) and temp2[i] != 3 and temp3[i] != 3:
            is_error = True
            break 
        elif (temp2[i] == U_type) and temp3[i] == 3:
            temp_vectors = []
            
            for temp in new_vectors:
                temp[i + 2*step] = U_type
                temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp2[i] != U_type) and temp3[i] == 3 and temp2[i] != 3:
            temp_vectors = []

            for temp in new_vectors:
                temp[i + 2*step] = f_digit 
                temp_vectors.append(np.copy(temp))
                    
                temp[i + 2*step] = s_digit 
                temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp3[i] == U_type) and temp2[i] == 3:
            temp_vectors = []
            
            for temp in new_vectors:
                temp[i + step] = U_type
                temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp3[i] != U_type) and temp2[i] == 3 and temp3[i] != 3:
            temp_vectors = []

            for temp in new_vectors:
                temp[i + step] = f_digit 
                temp_vectors.append(np.copy(temp))
                    
                temp[i + step] = s_digit 
                temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif temp2[i] == 3 and temp3[i] == 3:
            temp_vectors = []
            
            for temp in new_vectors:
                temp[i + step] = f_digit
                temp[i + 2*step] = f_digit
                temp_vectors.append(np.copy(temp))
            
                temp[i + step] = s_digit
                temp[i + 2*step] = s_digit
                temp_vectors.append(np.copy(temp))
            
                temp[i + step] = U_type
                temp[i + 2*step] = U_type
                temp_vectors.append(np.copy(temp))
            
                temp[i + step] = f_digit
                temp[i + 2*step] = s_digit
                temp_vectors.append(np.copy(temp))
            
                temp[i + step] = s_digit
                temp[i + 2*step] = f_digit
                temp_vectors.append(np.copy(temp))
                
            new_vectors = temp_vectors
    
    if (len(temp1) == 1) and (temp1[0] == 3):
        temp_vectors = []
        for temp in new_vectors:
            temp[0] = 0
            temp_vectors.append(np.copy(temp))
            
            temp[0] = 1
            temp_vectors.append(np.copy(temp))
            
            temp[0] = 2
            temp_vectors.append(np.copy(temp))
                
        new_vectors = temp_vectors
        
    elif (len(temp1) != 1):
        temp_vectors = []
        short_vectors = build_U_vectors(temp1, U_type)
        
        for temp in new_vectors:
            for vec in short_vectors:
                temp[0:step] = vec
                temp_vectors.append(np.copy(temp))
                
        new_vectors = temp_vectors
            
            
    if not is_error:
        poss_vectors = new_vectors
    return poss_vectors

#Проверка на U0, U1, U2
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
U_type - 0: U0, 1: U1, 2: U2
"""
def U0_U1_U2_check(vector, check_type, U_type, first_in = True):
    norm_vector = np.copy(vector)
    if first_in:
        norm_vector = U_normalize(vector, U_type)
    if 3 not in norm_vector:
        res = 0
        
        if len(norm_vector) == 3:
            if (norm_vector[1] == norm_vector[2]) or ((norm_vector[1] != U_type) and (norm_vector[2] != U_type)):
                res = 1
        else:
            step = math.ceil(len(norm_vector) / 3)
            temp1 = np.copy(norm_vector[0:step])
            temp2 = np.copy(norm_vector[step:2*step])
            temp3 = np.copy(norm_vector[2*step:3*step])
            
            arr_res = []
            for i in range(len(temp1)):
                if (temp2[i] == temp3[i]) or ((temp2[i] != U_type) and (temp3[i] != U_type)):
                    arr_res.append(1)
                else:
                    arr_res.append(0)
            
            if 0 not in arr_res:
                res = 1
            
            arr_res = []
            if res == 1:
                arr_res.append(U0_U1_U2_check(temp1, 0, U_type, False))
                arr_res.append(U0_U1_U2_check(temp2, 0, U_type, False))
                arr_res.append(U0_U1_U2_check(temp3, 0, U_type, False))
                if 0 in arr_res:
                    res = 0
        
        if check_type == 0 or check_type == 1:
            return res
        
        elif check_type == 2:
            poss_vectors = []
            if res == 1 and first_in:
                denorm_vector = U_back_normalize(norm_vector, U_type)
                poss_vectors.append(denorm_vector)
            elif res == 1:
                poss_vectors.append(norm_vector)
            poss_vectors = np.array(poss_vectors)
            return poss_vectors
    else:
        final_vectors = []
        poss_vectors = build_U_vectors(norm_vector, U_type)
        
        for vec in poss_vectors:
            res = U0_U1_U2_check(vec, 0, U_type, False)
            if res == 1:
                final_vectors.append(U_back_normalize(vec, U_type))
                
        if check_type == 0:
            if len(final_vectors) == 0:
                return 0
            elif (norm_vector[0] == 3) and (3 not in norm_vector[1:]):
                return 1
            else:
                return 2
        elif check_type == 1:
            return len(final_vectors)
        elif check_type == 2:
            final_vectors = np.array(final_vectors)
            return final_vectors





#Построение возможных векторов C
"""
Вход:
vector - вектор значений
C_type - 0: C0, 1: C1, 2: C2
"""
def build_C_vectors(vector, C_type):
    poss_vectors = []
    is_error = False
    step = math.ceil(len(vector) / 3)
    temp1 = np.copy(vector[0:step])
    temp2 = np.copy(vector[step:2*step])
    temp3 = np.copy(vector[2*step:3*step])
    new_vectors = []
    new_vectors.append(np.copy(vector))
    f_digit, s_digit = -1, -1
    if C_type == 0:
        f_digit, s_digit = 1, 2
    elif C_type == 1:
        f_digit, s_digit = 0, 2
    elif C_type == 2:
        f_digit, s_digit = 0, 1
        
    for i in range(len(temp1)):
        cond1 = (temp1[i] != temp2[i]) and (temp2[i] != C_type) and (temp1[i] != C_type)
        cond2 = (temp1[i] != temp3[i]) and (temp3[i] != C_type) and (temp1[i] != C_type) 
        cond3 = (temp1[i] != temp2[0]) and (temp2[0] != C_type) and (temp1[i] != C_type)
        cond4 = (temp1[i] != temp3[0]) and (temp3[0] != C_type) and (temp1[i] != C_type)
        if (cond1 or cond2 or cond3 or cond4) and (temp1[i] != 3) and (temp2[i] != 3) and (temp3[i] != 3):
            is_error = True
            break 
        elif (temp1[i] == 3) and (temp2[i] != 3) and (temp3[i] != 3):
            temp_vectors = []
            
            if (temp2[i] != temp3[i]) and (temp2[i] != C_type) and (temp3[i] != C_type):
                for temp in new_vectors:
                    temp[i] = C_type
                    temp_vectors.append(np.copy(temp))
                    
            elif (temp2[i] != temp3[i]) and ((temp2[i] == C_type) and (temp3[i] == C_type)):
                for temp in new_vectors:
                    temp[i] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    if temp2[i] != C_type:
                        temp[i] = temp2[i]
                        temp_vectors.append(np.copy(temp))
                    else:
                        temp[i] = temp3[i]
                        temp_vectors.append(np.copy(temp))
                        
            elif (temp2[i] == temp3[i]) and (temp2[i] != C_type):
                for temp in new_vectors:
                    temp[i] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = temp2[i]
                    temp_vectors.append(np.copy(temp))
            
            elif (temp2[i] == temp3[i]) and (temp2[i] == C_type):
                for temp in new_vectors:
                    temp[i] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = f_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = s_digit
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif ((temp1[i] != 3) and (temp2[i] == 3) and (temp3[i] != 3)) or ((temp1[i] != 3) and (temp2[i] != 3) and (temp3[i] == 3)):
            temp_vectors = []
            
            plus_val = 0
            if temp2[i] == 3:
                plus_val = step
            else:
                plus_val = 2*step
            if temp1[i] == C_type:
                for temp in new_vectors:
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i + plus_val] = f_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i + plus_val] = s_digit
                    temp_vectors.append(np.copy(temp))
            else:
                for temp in new_vectors:
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i + plus_val] = temp1[i]
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif ((temp1[i] == 3) and (temp2[i] == 3) and (temp3[i] != 3)) or ((temp1[i] == 3) and (temp2[i] != 3) and (temp3[i] == 3)):
            temp_vectors = []
            
            plus_val = 0
            another_val = 0
            if temp2[i] == 3:
                plus_val = step
                another_val = temp3[i]
            else:
                plus_val = 2*step
                another_val = temp2[i]
                
            if another_val == C_type:
                for temp in new_vectors:
                    temp[i] = C_type
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = C_type
                    temp[i + plus_val] = f_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = C_type
                    temp[i + plus_val] = s_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = f_digit
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = f_digit
                    temp[i + plus_val] = f_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = s_digit
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = s_digit
                    temp[i + plus_val] = s_digit
                    temp_vectors.append(np.copy(temp))
            else:
                for temp in new_vectors:
                    temp[i] = C_type
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = C_type
                    temp[i + plus_val] = f_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = C_type
                    temp[i + plus_val] = s_digit
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = another_val
                    temp[i + plus_val] = C_type
                    temp_vectors.append(np.copy(temp))
                    
                    temp[i] = another_val
                    temp[i + plus_val] = another_val
                    temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp1[i] != 3) and (temp2[i] == 3) and (temp3[i] == 3):
            temp_vectors = []

            if temp1[i] == C_type:
                poss_vals = [C_type, f_digit, s_digit]
                for temp in new_vectors:
                    for val1 in poss_vals:
                        for val2 in poss_vals:
                            temp[i + step] = val1
                            temp[i + 2*step] = val2
                            temp_vectors.append(np.copy(temp))
                            
            else:
                poss_vals = [C_type, temp1[i]]
                for temp in new_vectors:
                    for val1 in poss_vals:
                        for val2 in poss_vals:
                            temp[i + step] = val1
                            temp[i + 2*step] = val2
                            temp_vectors.append(np.copy(temp))
                    
            new_vectors = temp_vectors
        elif (temp1[i] == 3) and (temp2[i] == 3) and (temp3[i] == 3):
            temp_vectors = []
            
            for temp in new_vectors:
                temp[i] = C_type
                poss_vals = [C_type, f_digit, s_digit]
                for val1 in poss_vals:
                    for val2 in poss_vals:
                        temp[i + step] = val1
                        temp[i + 2*step] = val2
                        temp_vectors.append(np.copy(temp))
                        
                temp[i] = f_digit
                poss_vals = [C_type, f_digit]
                for val1 in poss_vals:
                    for val2 in poss_vals:
                        temp[i + step] = val1
                        temp[i + 2*step] = val2
                        temp_vectors.append(np.copy(temp))
            
                temp[i] = s_digit
                poss_vals = [C_type, s_digit]
                for val1 in poss_vals:
                    for val2 in poss_vals:
                        temp[i + step] = val1
                        temp[i + 2*step] = val2
                        temp_vectors.append(np.copy(temp))
                
            new_vectors = temp_vectors
            
    if not is_error:
        poss_vectors = new_vectors
    return poss_vectors

#Проверка на C0, C1, C2
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
С_type - 0: C0, 1: C1, 2: C2
"""
def C0_C1_C2_check(vector, check_type, C_type, first_in = True):
    norm_vector = np.copy(vector)
    if first_in:
        norm_vector = U_normalize(vector, C_type)
    if 3 not in norm_vector:
        res = 0
        
        if len(norm_vector) == 3:
            cond1 = (norm_vector[0] == norm_vector[1]) or (norm_vector[1] == C_type)
            cond2 = (norm_vector[0] == norm_vector[2]) or (norm_vector[2] == C_type)
            if norm_vector[0] == C_type:
                res = 1
            elif cond1 and cond2:
                res = 1
        else:
            step = math.ceil(len(norm_vector) / 3)
            temp1 = np.copy(norm_vector[0:step])
            temp2 = np.copy(norm_vector[step:2*step])
            temp3 = np.copy(norm_vector[2*step:3*step])
            
            arr_res = []
            for i in range(len(temp2)):
                cond1 = (temp1[i] == temp2[i]) or (temp2[i] == C_type) or (temp1[i] == C_type)
                cond2 = (temp1[i] == temp3[i]) or (temp3[i] == C_type) or (temp1[i] == C_type)
                cond3 = (temp1[i] == temp2[0]) or (temp2[0] == C_type) or (temp1[i] == C_type)
                cond4 = (temp1[i] == temp3[0]) or (temp3[0] == C_type) or (temp1[i] == C_type)
                if cond1 and cond2 and cond3 and cond4:
                    arr_res.append(1)
                else:
                    arr_res.append(0)
            
            if 0 not in arr_res:
                res = 1
            
            arr_res = []
            if res == 1:
                arr_res.append(C0_C1_C2_check(temp1, 0, C_type, False))
                arr_res.append(C0_C1_C2_check(temp2, 0, C_type, False))
                arr_res.append(C0_C1_C2_check(temp3, 0, C_type, False))
                if 0 in arr_res:
                    res = 0
        
        if check_type == 0 or check_type == 1:
            return res
        
        elif check_type == 2:
            poss_vectors = []
            if res == 1 and first_in:
                denorm_vector = U_back_normalize(norm_vector, C_type)
                poss_vectors.append(denorm_vector)
            elif res == 1:
                poss_vectors.append(norm_vector)
            poss_vectors = np.array(poss_vectors)
            return poss_vectors
    else:
        final_vectors = []
        poss_vectors = build_C_vectors(norm_vector, C_type)
        
        for vec in poss_vectors:
            res = C0_C1_C2_check(vec, 0, C_type, False)
            if res == 1:
                final_vectors.append(U_back_normalize(vec, C_type))
                
        if check_type == 0:
            if len(final_vectors) == 0:
                return 0
            else:
                return 2
        elif check_type == 1:
            return len(final_vectors)
        elif check_type == 2:
            final_vectors = np.array(final_vectors)
            return final_vectors





#Проверка на L
"""
Вход:
vector - вектор значений
check_type - тип проверки:
    0:
    Проверяет принадлежит ли классу вектор
    Выход:
        0 - не принадлежит
        1 - принадлежит
        2 - можно дополнить
    
    1: 
    Если вектор принадлежит классу, то выдаёт количество возможных векторов
    Выход:
        0 - не принадлежит
        1 и больше - количество возможных векторов
    2:
    Если вектор принадлежит классу, то выдаёт возможные вектора
    Выход:
        Массив возможных векторов
"""
def L_check(vector, check_type):
    len_vec = len(vector)
    n = 0
    while len_vec >= 3:
        len_vec = math.ceil(len_vec / 3)
        n += 1
    sets = np.array(list(itertools.product(range(3), repeat = n)))
    checked_list = np.zeros(len(vector), dtype = np.int32)
    if 3 not in vector:
        a0 = vector[0]
        x_list = []
        checked_list[0] = 1
        res = 0
        for i in range(len(vector[1:])):
            if sum(sets[i + 1]) == 1:
                x_list.append(i+1)
                checked_list[i+1] = 1
        y_list = []
        res_arr = []
        for ind in x_list:
            if (vector[2*ind] == ((2 * (vector[ind] - a0) + a0) % 3)):
                res_arr.append(1)
                y_list.append(2*ind)
                checked_list[2*ind] = 1
            else:
                res_arr.append(0)
                checked_list[2*ind] = -1
                
        if 0 not in res_arr:
            i = 0
            flag = False
            for s in sets:
                if checked_list[i] == 0:
                    point_sum = a0
                    j = len(x_list) - 1
                    for digit in s:
                        if digit == 1:
                            point_sum += vector[x_list[j]] - a0
                        elif digit == 2:
                            point_sum += vector[y_list[j]] - a0
                        j -= 1
                    point_sum = point_sum % 3
                    if vector[i] == point_sum:
                        res_arr.append(1)
                        checked_list[i] = 1
                    else:
                        flag = True
                        res_arr.append(0)
                        checked_list[i] = -1
                if flag:
                    break
                i += 1

        if 0 not in res_arr:
            res = 1
        if (check_type == 0) or (check_type == 1):
            return res
        else:
            poss_vectors = []
            if res == 1:
                poss_vectors.append(vector)
            poss_vectors = np.array(poss_vectors)
            return poss_vectors
    else:
        poss_vectors = []
        poss_vectors.append(np.copy(vector))
        x_list = []
        is_error = False
        for i in range(len(vector)):
            if sum(sets[i]) == 1:
                x_list.append(i)
        x_list = np.array(x_list)
        y_list = x_list * 2
        if vector[0] == 3:
            k = 0
            for i in x_list:
                if vector[i] == 3 and vector[y_list[k]] == 3:
                    temp_vectors = []
                    poss_vals = [0, 1, 2]
                    for temp in poss_vectors:
                        for val1 in poss_vals:
                            for val2 in poss_vals:
                                temp[0] = val1
                                temp[i] = val2
                                temp[y_list[k]] = (2 * val2 - val1) % 3
                                temp_vectors.append(np.copy(temp))
                                    
                    poss_vectors = temp_vectors
                elif vector[i] == 3 and vector[y_list[k]] != 3:
                    temp_vectors = []
                    poss_vals = [0, 1, 2]
                    for val in poss_vals:
                        if vector[y_list[k]] == val:
                            for temp in poss_vectors:
                                temp[0] = val
                                temp[i] = val
                                temp_vectors.append(np.copy(temp))

                                temp[0] = (val + 1) % 3
                                temp[i] = (val + 2) % 3
                                temp_vectors.append(np.copy(temp))

                                temp[0] = (val + 2) % 3
                                temp[i] = (val + 1) % 3
                                temp_vectors.append(np.copy(temp))           
                    poss_vectors = temp_vectors
                elif vector[i] != 3 and vector[y_list[k]] == 3:
                    temp_vectors = []
                    poss_vals = [0, 1, 2]
                    for temp in poss_vectors:
                        for val in poss_vals:
                            temp[0] = val
                            temp[y_list[k]] = (2 * vector[i] - val) % 3
                            temp_vectors.append(np.copy(temp))
                    poss_vectors = temp_vectors
                elif vector[i] != 3 and vector[y_list[k]] != 3:
                    temp_vectors = []
                    for temp in poss_vectors:
                        temp[0] = (2 * vector[i] - vector[y_list[k]]) % 3
                        temp_vectors.append(np.copy(temp))
                    poss_vectors = temp_vectors
                k += 1
        else:
            k = 0
            for i in x_list:
                if vector[i] == 3 and vector[y_list[k]] == 3:
                    temp_vectors = []
                    poss_vals = [0, 1, 2]
                    for temp in poss_vectors:
                        for val in poss_vals:
                            temp[i] = val
                            temp[y_list[k]] = (2 * val - vector[0]) % 3
                            temp_vectors.append(np.copy(temp))
                    poss_vectors = temp_vectors
                elif vector[i] == 3 and vector[y_list[k]] != 3:
                    temp_vectors = []
                    for temp in poss_vectors:
                        temp[i] = (2 * (vector[0] + vector[y_list[k]])) % 3
                        temp_vectors.append(np.copy(temp))
                    poss_vectors = temp_vectors
                elif vector[i] != 3 and vector[y_list[k]] == 3:
                    temp_vectors = []
                    for temp in poss_vectors:
                        temp[y_list[k]] = (2 * vector[y_list[k]] - vector[0]) % 3
                        temp_vectors.append(np.copy(temp))
                    poss_vectors = temp_vectors
                k += 1
        
        i = 0
        for s in sets:
            if(poss_vectors[0][i] == 3):
                for temp in poss_vectors:
                    point_sum = temp[0]
                    j = len(x_list) - 1
                    for digit in s:
                        if digit == 1:
                            point_sum += temp[x_list[j]] - temp[0]
                        elif digit == 2:
                            point_sum += temp[y_list[j]] - temp[0]
                        j -= 1
                    point_sum = point_sum % 3
                    temp[i] = point_sum
            i += 1
            
        final_vectors = []
        
        for vec in poss_vectors:
            res = L_check(vec, 0)
            if res == 1:
                final_vectors.append(vec)
                
        if check_type == 0:
            if len(final_vectors) == 0:
                return 0
            else:
                return 2
        elif check_type == 1:
            return len(final_vectors)
        elif check_type == 2:
            final_vectors = np.array(final_vectors)
            return final_vectors





def test_for_class(test_class, vector, check_type):
    a = 0
    if test_class == 'T0':
        a = T0_T1_T2_check(vector, check_type, 0)
    elif test_class == 'T1':
        a = T0_T1_T2_check(vector, check_type, 1)
    elif test_class == 'T2':
        a = T0_T1_T2_check(vector, check_type, 2)
    elif test_class == 'T12':
        a = T12_T02_T01_check(vector, check_type, 0)
    elif test_class == 'T02':
        a = T12_T02_T01_check(vector, check_type, 1)
    elif test_class == 'T01':
        a = T12_T02_T01_check(vector, check_type, 2)
    elif test_class == 'B':
        a = B_check(vector, check_type)
    elif test_class == 'S':
        a = S_check(vector, check_type)
    elif test_class == 'L':
        a = L_check(vector, check_type)
    elif test_class == 'M0':
        a = M0_M1_M2_check(vector, check_type, 0)
    elif test_class == 'M1':
        a = M0_M1_M2_check(vector, check_type, 1)
    elif test_class == 'M2':
        a = M0_M1_M2_check(vector, check_type, 2)
    elif test_class == 'U0':
        a = U0_U1_U2_check(vector, check_type, 0)
    elif test_class == 'U1':
        a = U0_U1_U2_check(vector, check_type, 1)
    elif test_class == 'U2':
        a = U0_U1_U2_check(vector, check_type, 2)
    elif test_class == 'C0':
        a = C0_C1_C2_check(vector, check_type, 0)
    elif test_class == 'C1':
        a = C0_C1_C2_check(vector, check_type, 1)
    elif test_class == 'C2':
        a = C0_C1_C2_check(vector, check_type, 2)
    return a





def test_for_classes(input_path, check_type, union_type):
    vector, classes = read_input(input_path)
    is_input_correct = True
    if (len(vector) % 3 != 0):
        print("Неверная длина вектора!")
        is_input_correct = False
    else:
        for val in vector:
            if (val != 0) and (val != 1) and (val != 2) and (val != 3):
                print("Неверные значения вектора!")
                is_input_correct = False
    
    if (check_type != 0) and (check_type != 1) and (check_type != 2):
        print("Неверный тип проверки!")
        is_input_correct = False
                
    if (union_type != 0) and (union_type != 1) and (union_type != 2):
        print("Неверный тип объединения!")
        is_input_correct = False
    
    check_res = []
    for cl in classes:
        cond1 = (cl == 'T0') or (cl == 'T1') or (cl == 'T2') or (cl == 'T12') or (cl == 'T02') or (cl == 'T01')
        cond2 = (cl == 'C0') or (cl == 'C1') or (cl == 'C2') or (cl == 'U0') or (cl == 'U1') or (cl == 'U2')
        cond3 = (cl == 'M0') or (cl == 'M1') or (cl == 'M2') or (cl == 'S') or (cl == 'B') or (cl == 'L')
        if cond1 or cond2 or cond3:
            check_res.append(1)
        else:
            check_res.append(0)
    if 0 in check_res:
        print("Одно из названий класса неверное")
        is_input_correct = False
        
    if is_input_correct:
        result = 0
        unresult = 0
        fulresult = 0
        if len(classes) == 1:
            result = test_for_class(classes[0], vector, check_type)
        else:
            if check_type == 0:
                res_arr = []
                for cl in classes:
                    res_arr.append(test_for_class(cl, vector, 0))
                if union_type == 0:
                    result = np.copy(res_arr)
                elif union_type == 1:
                    if (0 not in res_arr) and (2 not in res_arr):
                        unresult = 1
                    elif (2 in res_arr) and (0 not in res_arr):
                        i = 0
                        final_vectors = []
                        for cl in classes:
                            temp_vectors = []
                            if i == 0:
                                temp_vectors = test_for_class(cl, vector, 2)
                            else:
                                for temp in final_vectors:
                                    if (test_for_class(cl, temp, 0) == 1):
                                        temp_vectors.append(temp)
                            final_vectors = temp_vectors.copy()
                            i += 1
                        if len(final_vectors) != 0:
                            unresult = 2
                else:
                    if 1 in res_arr:
                        fulresult = 1
                    elif 2 in res_arr:
                        fulresult = 2
            elif check_type == 1:
                if union_type == 0:
                    res_arr = []
                    for cl in classes:
                        res_arr.append(test_for_class(cl, vector, 1))
                    result = np.copy(res_arr)
                elif union_type == 1:
                    i = 0
                    final_vectors = []
                    for cl in classes:
                        temp_vectors = []
                        if i == 0:
                            temp_vectors = test_for_class(cl, vector, 2)
                        else:
                            for temp in final_vectors:
                                if (test_for_class(cl, temp, 0) == 1):
                                    temp_vectors.append(np.copy(temp))
                        final_vectors = temp_vectors.copy()
                        i += 1
                    unresult = len(final_vectors)
                else:
                    final_vectors = []
                    for cl in classes:
                        temp_vectors = []
                        temp_vectors = test_for_class(cl, vector, 2)
                        for temp in temp_vectors:
                            isnonew = False
                            for vec in final_vectors:
                                if (np.array_equal(temp, vec)):
                                    isnonew = True
                            if not isnonew:
                                final_vectors.append(np.copy(temp))
                    fulresult = len(final_vectors)
            elif check_type == 2:
                if union_type != 2:
                    i = 0
                    final_vectors = []
                    for cl in classes:
                        temp_vectors = []
                        if i == 0:
                            temp_vectors = test_for_class(cl, vector, 2)
                        else:
                            for temp in final_vectors:
                                if (test_for_class(cl, temp, 0) == 1):
                                    temp_vectors.append(temp)
                        final_vectors = temp_vectors.copy()
                        i += 1
                    unresult = np.array(final_vectors)
                else:
                    final_vectors = []
                    for cl in classes:
                        temp_vectors = []
                        temp_vectors = test_for_class(cl, vector, 2)
                        for temp in temp_vectors:
                            isnonew = False
                            for vec in final_vectors:
                                if (np.array_equal(temp, vec)):
                                    isnonew = True
                            if not isnonew:
                                final_vectors.append(np.copy(temp))
                    fulresult = np.array(final_vectors)
        if (len(classes) == 1):
            if check_type == 0:
                if result == 1:
                    print(f"Функция {vector} лежит в классе {classes[0]}")
                elif result == 2:
                    print(f"Функцию {vector} можно дополнить до принадлежности классу {classes[0]}")
                elif result == 0:
                    print(f"Функция {vector} не лежит в классе {classes[0]}")
            elif check_type == 1:
                if result == 0:
                    print(f"Функция {vector} не лежит в классе {classes[0]}")
                else:
                    print(f"Из вектора значений {vector} можно получить {result} функций, лежащих в классе {classes[0]}")
            elif check_type == 2:
                if len(result) == 0:
                    print(f"Функция {vector} не лежит в классе {classes[0]}")
                else:
                    print(f"Из вектора значений {vector} можно получить следующие функции, лежащие в классе {classes[0]}:")
                    for vec in result:
                        print(vec)
        
        elif (union_type == 0):
            if check_type == 0:
                print("Принадлежность классу: ")
                for i in range(len(classes)):
                    if result[i] == 1:
                        print(f"Функция {vector} лежит в классе {classes[i]}")
                    elif result[i] == 2:
                        print(f"Функцию {vector} можно дополнить до принадлежности классу {classes[i]}")
                    elif result[i] == 0:
                        print(f"Функция {vector} не лежит в классе {classes[i]}")
            elif check_type == 1:
                print("Количество возможных функций: ")
                for i in range(len(classes)):
                    if result[i] == 0:
                        print(f"Функция {vector} не лежит в классе {classes[i]}")
                    else:
                        print(f"Из вектора значений {vector} можно получить {result[i]} функций, лежащих в классе {classes[i]}")
            elif check_type == 2:
                if len(unresult) == 0:
                    print(f"Функция {vector} не лежит в пересечении классов {classes}")
                else:
                    print(f"Из вектора значений {vector} можно получить следующие функции, лежащие в пересечении классов {classes}:")
                    for vec in unresult:
                        print(vec)
        elif (union_type == 1):
            if check_type == 0:
                if unresult == 1:
                    print(f"Функция {vector} лежит в пересечении классов {classes}")
                elif unresult == 2:
                    print(f"Функцию {vector} можно дополнить до принадлежности пересечению классов {classes}")
                elif unresult == 0:
                    print(f"Функция {vector} не лежит в пересечении классов {classes}")
            elif check_type == 1:
                if unresult == 0:
                    print(f"Функция {vector} не лежит в пересечении классов {classes}")
                else:
                    print(f"Из вектора значений {vector} можно получить {unresult} функций, лежащих в пересечении классов {classes}")
            elif check_type == 2:
                if len(unresult) == 0:
                    print(f"Функция {vector} не лежит в пересечении классов {classes}")
                else:
                    print(f"Из вектора значений {vector} можно получить следующие функции, лежащие в пересечении классов {classes}:")
                    for vec in unresult:
                        print(vec)
        else:
            if check_type == 0:
                if fulresult == 1:
                    print(f"Функция {vector} лежит в объединении классов {classes}")
                elif fulresult == 2:
                    print(f"Функцию {vector} можно дополнить до принадлежности объединению классов {classes}")
                elif unresult == 0:
                    print(f"Функция {vector} не лежит в объединении классов {classes}")
            elif check_type == 1:
                if fulresult == 0:
                    print(f"Функция {vector} не лежит в объединении классов {classes}")
                else:
                    print(f"Из вектора значений {vector} можно получить {fulresult} функций, лежащих в объединении классов {classes}")
            elif check_type == 2:
                if len(fulresult) == 0:
                    print(f"Функция {vector} не лежит в объединении классов {classes}")
                else:
                    print(f"Из вектора значений {vector} можно получить следующие функции, лежащие в объединении классов {classes}:")
                    for vec in fulresult:
                        print(vec)   
                


def main():
    file_name = str(sys.argv[1])
    check_type = int(sys.argv[2])
    union_type = 0
    if len(sys.argv) == 4:
        union_type = int(sys.argv[3])
    test_for_classes(file_name, check_type, union_type)

if __name__ == '__main__':
    main()


