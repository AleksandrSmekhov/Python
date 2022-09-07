#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math
import itertools
import random
import os
import sys


# In[2]:


def generate_RM(r, m, return_type=True):
    C = np.zeros(0, dtype = np.int32)
    for i in range(r+1):
        C = np.append(C, int(math.factorial(m)/(math.factorial(i)*math.factorial(m-i))))
    k = np.sum(C)
    
    n = 2**m
    
    G = np.zeros((k, n), dtype = np.int32)
    G_x = np.zeros((m, n), dtype = np.int32)
    v_input = list(itertools.product(range(2), repeat = m))
    v_com_ind = m + 1
    
    for i in range(len(C)):
        if (i == 0):
            G[i] += 1
        elif (i == 1):
            for i1 in range(m):
                for j in range(n):
                    G[i1 + 1][j] = v_input[j][i1]
                    G_x[i1][j] = v_input[j][i1]
        else:
            v_combinations = list(itertools.combinations(range(m),i))
            for v_com in v_combinations:
                G[v_com_ind] += 1
                for i1 in range(len(v_com)):
                    G[v_com_ind] *= G[v_com[i1] + 1]
                v_com_ind += 1
    if return_type:
        return k, n, G
    else:
        return C, G_x, G


# In[3]:


def inv_M(M_def, return_type = True):
    M = np.copy(M_def)
    M_1 = np.eye(len(M), len(M[0]), dtype = np.int32)

    i = 0
    j = 0
    while i < len(M):
        if M[i][i] == 0:
            k = True
            j = i + 1
            while k and (j < len(M)):
                if M[j][i] == 1:
                    M[j] += M[i]
                    M[i] = M[j] - M[i]
                    M[j] -= M[i]
                    
                    M_1[j] += M_1[i]
                    M_1[i] = M_1[j] - M_1[i]
                    M_1[j] -= M_1[i]
                    
                    k = False
                else:
                    j += 1
        j = i + 1
        while j < len(M):
            if M[j][i] == 1:
                M[j] = (M[j] - M[i]) % 2
                M_1[j] = (M_1[j] - M_1[i]) % 2
                j += 1
            else:
                j += 1
        i += 1
    
    i = 1
    while i < len(M):
        j = 0
        while j < i:
            if M[j][i] == 1:
                M[j] = (M[j] - M[i]) % 2
                M_1[j] = (M_1[j] - M_1[i]) % 2
                j += 1
            else:
                j += 1
        i += 1
    
    if return_type:
        return M, M_1
    else:
        return M_1


# In[4]:


def generate_random_matrix(k):
    M = np.random.randint(0, 2, (k, k))
    if (np.linalg.det(M) == 0):
        M_1, M = generate_random_matrix(k)
    M_check, M_1 = inv_M(M)
    if np.allclose(M_check, np.eye(len(M), len(M[0]), dtype = np.int32)) == False:
        M_1, M = generate_random_matrix(k)
    return M_1, M


# In[5]:


def generate_random_P(n):
    a = np.array(range(n))
    b = np.random.permutation(n)
    a = np.append(a, b).reshape(2, n)
    P = np.zeros((n,n), dtype = np.int32)
    for i in range(n):
        P[a[1][i]][a[0][i]] = 1
    return P


# In[6]:


def generate_keys(r, m):
    k, n, Grm = generate_RM(r, m)
    
    M_1, M = generate_random_matrix(k)
    
    P = generate_random_P(n)

    Gpub = np.dot(np.dot(M, Grm), P) % 2
    
    P_1 = np.linalg.inv(P).astype(np.int32)
    
    sk = np.array([M_1, P_1], dtype = object)
    
    return sk, Gpub


# In[7]:


def save_key(key, file_name, key_type = True):
    if key_type: # pk
        with open(file_name, 'w') as file:
            for i in range(len(key)):
                for j in range(len(key[0])):
                    file.write(str(key[i][j]))
                    if j != len(key[0]) - 1:
                        file.write(',')
                file.write('\n')
                
    else: # sk
        with open(file_name, 'w') as file:
            for i in range(len(key[0])):
                for j in range(len(key[0][0])):
                    file.write(str(key[0][i][j]))
                    if j != len(key[0][0]) - 1:
                        file.write(',')
                file.write('\n')
            file.write('\n')
            for i in range(len(key[1])):
                for j in range(len(key[1][0])):
                    file.write(str(key[1][i][j]))
                    if j != len(key[1][0]) - 1:
                        file.write(',')
                file.write('\n')


# In[8]:


def read_key(file_name, key_type = True):
    file_exist = os.path.exists(file_name)
    if file_exist:
        if key_type: # pk
            key = []
            k = 0
            n = 0
            with open(file_name, 'r') as file:
                for line in file:
                    n = 0
                    for var in line.split(','):
                        n += 1
                        key.append(int(var))
                    k += 1

            key = np.array(key, dtype = np.int32).reshape(k, n)
            return True, key

        else: # sk
            M_1 = []
            P_1 = []
            k = 0
            n = 0

            with open(file_name, 'r') as file:
                M = True
                for line in file:
                    if line == '\n':
                        M = False
                    elif M:
                        n = 0
                        for var in line.split(','):
                            n += 1
                            M_1.append(int(var))
                    else:
                        k = 0
                        for var in line.split(','):
                            k += 1
                            P_1.append(int(var))

            M_1 = np.array(M_1, dtype = np.int32).reshape(n, n)
            P_1 = np.array(P_1, dtype = np.int32).reshape(k, k)

            key = np.array([M_1, P_1], dtype = object)
            return True, key
        
    else:
        print(f'Файла {file_name} не существует')
        return False, np.zeros(0)
        


# In[9]:


def power_of_two(n):
    two_in_power = 2
    power = 0
    while two_in_power <= n:
        two_in_power *= 2
        power += 1
    return power

def r_finder(k, m):
    r = 0
    sumC = 0
    while sumC < k:
        C = np.zeros(0, dtype = np.int32)
        for i in range(r):
            C = np.append(C, int(math.factorial(m)/(math.factorial(i)*math.factorial(m-i))))
        sumC = np.sum(C)
        r += 1
    return r-2


# In[10]:


def random_message(k):
    m = np.random.randint(0, 2, k)
    return m


# In[11]:


def encryption(pk, a):
    a = np.dot(a, pk) % 2
    
    m = power_of_two(len(pk[0]))
    r = r_finder(len(pk), m)
    weigth = 2**(m - r - 1) - 1
    
    e = np.zeros(len(a), dtype = np.int32) 
    tmp = []
    while len(tmp) < weigth:
        x = random.randint(0, len(a) - 1)
        if x not in tmp:
            tmp.append(x)
    for val in tmp:
        e[val] += 1

    a = (a + e) % 2
    return a


# In[12]:


def save_message(message, name):
    with open(name, 'w') as file:
            for i in range(len(message)):
                file.write(str(message[i]))
                if i != len(message) - 1:
                    file.write(',')
    print(f"Cообщение: {message}\nСохранено в файл {name}")


# In[13]:


def get_message(k, message_name, message_type):
    message_exist = False
    m = []
    
    if message_type:
        m = random_message(k)
        save_message(m, message_name)
        message_exist = True
    else:
        file_exist = os.path.exists(message_name)
        if file_exist:
            with open(message_name, 'r') as file:
                for line in file:
                    for var in line.split(','):
                        m.append(int(var))

            m = np.array(m, dtype = np.int32)
            message_exist = True
        else:
            m = np.zeros(0)
            print(f"Файл {message_name} не найден")
    return m, message_exist


# In[14]:


def reed_decode(c, r, m, out_type = True):   
    C, G_x, Grm = generate_RM(r, m, return_type=False)
    k = np.sum(C)
    a = np.zeros(k, dtype = np.int32)
    
    cur_ind = len(Grm) - 1
    for i in range(len(C) - 1):
        u_combinations = list(itertools.combinations(range(m),len(C) - 1 - i))
        
        g_f = np.zeros(0, dtype = np.int32)
        for u in u_combinations:
            xu = np.zeros(shape=(2**(len(u)), m), dtype = np.int32)
            xu_comb = list(itertools.product(range(2), repeat=len(u)))
            
            for k in range(len(xu_comb)):
                j1 = 0 
                for j in u:
                    xu[k][j] += xu_comb[k][j1]
                    j1 += 1
            
            v_plus_ind = list(range(m))
            
            for j in u:
                v_plus_ind.remove(j)
                
            v_plus = np.zeros(shape=(2**len(v_plus_ind), m), dtype = np.int32)
            v_plus_comb = list(itertools.product(range(2), repeat=len(v_plus_ind)))
            
            for k in range(len(v_plus_comb)):
                j1 = 0 
                for j in v_plus_ind:
                    v_plus[k][j] += v_plus_comb[k][j1]
                    j1 += 1
            
            f_val = np.zeros(0, dtype = np.int32)
            for v in v_plus:
                xu_val = np.zeros(len(xu), dtype = np.int32)
                xu_val_ind = 0
                for x_u in xu:
                    temp = x_u + v
                    for j in range(len(G_x[0])):
                        temp1 = np.rot90(G_x, k=-1)[j]
                        if np.sum((temp1 + temp) % 2) == 0: 
                            xu_val[xu_val_ind] += c[j]
                    xu_val_ind += 1
                f_val = np.append(f_val, np.sum(xu_val) % 2)
            
            if (np.sum(f_val) > len(f_val)/2):
                g_f = np.append(g_f, cur_ind)
            else:
                g_f = np.append(g_f, 0)
            
            cur_ind -= 1
        
        for ind in g_f:
            if ind > 0:
                c = (c + Grm[ind]) % 2
                a[ind] += 1
                
    if(np.sum(c) > len(c)/2):
        c = (c + 1) % 2
        a[0] += 1
    if out_type == False:
        print(f"Ошибка: {c}")
    return a


# In[15]:


def decryption(sk, c):
    c = np.dot(c, sk[1])
    
    m = power_of_two(len(sk[1]))
    r = r_finder(len(sk[0]), m)
    
    c = reed_decode(c, r, m)
    
    c = np.dot(c, sk[0]) % 2

    return c


# In[16]:


def check_keys(pk, sk):
    m = power_of_two(len(pk[0]))
    r = r_finder(len(pk), m)
    
    k, n, Grm = generate_RM(r, m)
 
    M_1 = sk[0]
    P_1 = sk[1]
    
    if (k == len(M_1)) and (n == len(P_1)):
        M = inv_M(M_1, return_type=False)
        P = inv_M(P_1, return_type=False)

        k, n, Grm = generate_RM(r, m)
        potential_Gpub = np.dot(np.dot(M, Grm), P) % 2

        if np.allclose(potential_Gpub, pk):
            return True
        else:
            return False
    else:
        return False


# In[24]:


def ind_to_v(x, V_ind_set):
    x_ones = []
    x_zeros = []
    
    for i in range(len(x)):
        if x[i]:
            x_ones.append(i)
        else:
            x_zeros.append(i)
            
    V_set = []
    for ind_set in V_ind_set:
        v = np.zeros(len(x), dtype = np.int32)
        for i in ind_set:
            v[x_zeros[i]] = 1
        for i in x_ones:
            v[i] = 1
        V_set.append(v)
        
    V_set = np.array(V_set, dtype = np.int32)
    return V_set


# In[25]:


def gauss_exception(A):
    A = np.array(A, dtype = np.int32)
    cur_j = 0
    for i in range(len(A[0])):
        j = cur_j
        while j < len(A) and A[j][i] == 0:
            j += 1
        if j != len(A): 

            temp = np.copy(A[j])
            A[j] = A[cur_j]
            A[cur_j] = temp

            for j in range(cur_j + 1, len(A)):
                if A[j][i] == 1:
                    A[j] = (A[j] + A[cur_j]) % 2

            cur_j += 1
    
    A = A.tolist()
    for i in range(len(A) - cur_j):
        A.pop()
        
    return A


# In[26]:


def add_new_vectors(basis, V_set):
    for V in V_set:
        basis.append(V)
    
    basis = gauss_exception(basis)
    
    return basis


# In[22]:


def build_C0(x, G):
    x_ind = []
    for i in range(len(x)):
        if x[i] == 1: 
            x_ind.append(i)
            
    C0 = np.copy(G)
    
    cur_j = 0
    for i in x_ind:
        j = cur_j
        while j < len(C0) and C0[j][i] == 0:
            j += 1
        if j != len(C0): 

            temp = np.copy(C0[j])
            C0[j] = C0[cur_j]
            C0[cur_j] = temp

            for j in range(cur_j + 1, len(C0)):
                if C0[j][i] == 1:
                    C0[j] = (C0[j] + C0[cur_j]) % 2

            cur_j += 1
     
    C0 = C0[cur_j:]
    
    for j in x_ind:
        for i in range(len(C0)):
            assert C0[i][j] == 0
    
    C = np.zeros((len(C0), len(C0[0]) - np.sum(x)), dtype = np.int32)
    
    cur_i = 0
    for i in range(len(C0[0])):
        if not (i in x_ind):
            for j in range(len(C0)):
                C[j][cur_i] = C0[j][i]
            cur_i += 1
    return C


# In[23]:


def divide_C0(r, m, C0):
    M = 1
    V_set = np.zeros(0, dtype = np.int32)
    
    is_finded = False 
    while not is_finded:
        temp1 = 2 ** (m - 2 * r + 1)
        temp2 = 2 ** (m - r)
        c = math.ceil(M * (temp1 * (temp1 - 1) / float(temp2 * (temp2 - 1))))

        minw = temp2
        eps = math.sqrt(1 - 1.0 / temp1)
        maxw = temp1 * ((2 ** r) - 1) * eps

        xi = []

        while len(xi) < M:
            temp = np.random.randint(0, 2, len(C0))
            test_x = np.dot(temp, C0) % 2
            if minw <= np.sum(test_x) < maxw:
                xi.append(test_x)

        cij_counter = dict()
        temp = 2 ** m - 2 ** (m - r)

        for i in range(temp):
            for j in range(i + 1, temp):
                cij_counter[(i, j)] = 0

        for x in xi:
            for i in range(temp):
                for j in range(i + 1, temp):
                    if x[i] == 1 and x[j] == 1:
                        cij_counter[(i,j)] += 1

        G = {}
        for i in range(temp):
            G[i] = set()

        c /= 2
        for i in range(temp):
            for j in range(i + 1, temp):
                if cij_counter[(i, j)] >= c:
                    G[i].add(j)
                    G[j].add(i)

        marked_v = set()
        
        V_set = np.zeros(0, dtype = np.int32)
        
        is_finish = True
        
        for i in G.keys():
            if i not in marked_v: 
                v_queue = np.array([i])
                V = set()
                while len(v_queue) > 0:
                    v_last, v_queue = v_queue[-1], v_queue[:-1]
                    marked_v.add(v_last)
                    V.add(v_last)
                    if len(G[v_last]) != temp2 - 1:
                        is_finish = False
                    for v in G[v_last]:
                        if v not in marked_v:
                            v_queue = np.append(v_queue, v)                    
                V_set = np.append(V_set, V)

        if is_finish:
            is_finded = True
            
        M += 200
    return V_set


# In[28]:


def adamar_mul(A, B):
    C = []
    for i in range(len(A)):
        for j in range(len(B)):
            C.append(A[i] * B[j])
    
    C = gauss_exception(C)
        
    C = np.array(C, dtype = np.int32)
    
    return C


# In[29]:


def orthogonal_comp(G):
    is_solved = False
    zero_v = np.zeros(len(G), dtype = np.int32)
    orthogonal_vectors = []
    
    while not is_solved:
        test_x = np.random.randint(0, 2, len(G[0]))
        res = np.dot(G, test_x) % 2
        if np.allclose(res, zero_v):
            orthogonal_vectors.append(test_x)
            if (len(orthogonal_vectors) != 1):
                orthogonal_vectors = gauss_exception(orthogonal_vectors)
        
        if len(orthogonal_vectors) == (len(G[0]) - len(G)):
            is_solved = True
            
    orthogonal_vectors = np.array(orthogonal_vectors, dtype = np.int32)
    
    return orthogonal_vectors 


# In[27]:


def dm_reduce(Gdm):
    m = power_of_two(len(Gdm[0]))
    d = r_finder(len(Gdm), m)
    C = np.zeros(0, dtype = np.int32)
    for i in range(d):
        C = np.append(C, int(math.factorial(m)/(math.factorial(i)*math.factorial(m-i))))
    
    basis = []
    
    while len(basis) < np.sum(C):
        x = np.zeros(len(Gdm[0]), dtype = np.int32)
        while np.sum(x) != 2**(m-d):
            temp = np.random.randint(0, 2, len(Gdm))
            x = np.dot(temp, Gdm) % 2
        
        C0 = build_C0(x, Gdm)
        
        V_ind_set = divide_C0(d, m, C0)
        
        V_set = ind_to_v(x, V_ind_set)
        
        basis = add_new_vectors(basis, V_set)
        
    basis = np.array(basis, dtype = np.int32)
    return basis


# In[35]:


def adamar_attack(pk):
    m = power_of_two(len(pk[0]))
    r = r_finder(len(pk), m)
    
    d, b = r, m - 1
    while b:
        d, b = b, d % b
    
    Gdm = pk
    cur_r = r
    while cur_r != d:
        if (cur_r + r) < m:
            Gdm = adamar_mul(Gdm, pk)
            cur_r += r
        else:
            Gdm = orthogonal_comp(Gdm)
            cur_r = m - r - 1
            
    Gd1m = dm_reduce(Gdm)
    
    A = orthogonal_comp(Gdm)
    B = adamar_mul(A, Gd1m)
    G1m = orthogonal_comp(B)
    
    #Поиск подставки sigma` // finding permutation sigma`
    #return P_1


# In[17]:


def mode_one(r, m, pk_name = 'pk.txt', sk_name = 'sk.txt'):
    if r > m:
        r += m
        m = r - m
        r -= m
    sk, pk = generate_keys(r, m)
    save_key(pk, pk_name)
    save_key(sk, sk_name, False)


# In[ ]:


def mode_two(pk_name = 'pk.txt'):
    pk_exist, pk = read_key(pk_name)
    if pk_exist:
        P_1 = adamar_attack(pk)
        m = power_of_two(len(pk[0]))
        r = r_finder(len(pk), m)
        _, _, Grm = generate_RM(r, m)
        Grm_1 = inv_M(Grm)
        M_1 = np.dot(np.dot(pk, P_1), Grm_1) % 2
        sk = np.array([M_1, P_1], dtype = object)
        save_key(sk, 'recovered_sk_key.txt', False)


# In[18]:


def mode_three(pk_name = 'pk.txt', sk_name = 'sk.txt'):
    pk_exist, pk = read_key(pk_name)
    sk_exist, sk = read_key(sk_name, key_type=False)
    
    if pk_exist and sk_exist:
        if check_keys(pk, sk):
            print("true")
        else:
            print("false")


# In[19]:


def mode_four(pk_name = 'pk.txt', message_name = 'message.txt', en_message = 'en_message.txt', is_random_message = True):
    pk_exist, pk = read_key(pk_name)
    if pk_exist:
        k = len(pk)
        m, message_exist = get_message(k, message_name, is_random_message)
        if message_exist and k == len(m):
            c = encryption(pk, m)
            save_message(c, en_message)
        else:
            print(f"Размер сообщения не соответствует размеру ключа {pk_name}")


# In[20]:


def mode_five(sk_name = 'sk.txt', en_message = 'en_message.txt', de_message = 'de_message.txt'):
    sk_exist, sk = read_key(sk_name, key_type=False)
    if sk_exist:
        m, message_exist = get_message(0, en_message, False)
        if message_exist and len(sk[1]) == len(m):
            a = decryption(sk, m)
            save_message(a, de_message)
        else:
            print(f"Размер сообщения не соответствует размеру ключа {sk_name}")


# In[21]:


def mode_six(r, m, message = 'en_message.txt'):
    C = np.zeros(0, dtype = np.int32)
    for i in range(r+1):
        C = np.append(C, int(math.factorial(m)/(math.factorial(i)*math.factorial(m-i))))
    k = np.sum(C)
    c, message_exist = get_message(0, message, False)
    
    if 2**m == len(c) and message_exist:
        a = reed_decode(c, r, m, out_type = False)
        print(f"Сообщение: {a}")
    elif k != len(c):
        print("Неподходящая длина сообщения")


# In[37]:


def main():
    mode = int(sys.argv[1])
    args = sys.argv[2:]
    if mode == 1:
        i = 0
        is_correct = True
        r = 0
        m = 0
        pk_name = 'pk.txt'
        sk_name = 'sk.txt'
        while i < len(args):
            if i == 0:
                r = int(args[i])
            elif i == 1:
                m = int(args[i])
            elif i == 2:
                pk_name = str(args[i])
            elif i == 3:
                sk_name = str(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct and len(args) > 1:
            mode_one(r, m, pk_name, sk_name)
    elif mode == 2:
        i = 0
        is_correct = True
        pk_name = 'pk.txt'
        while i < len(args):
            if i == 0:
                pk_name = str(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct and len(args) < 2:
            mode_two(pk_name)
    elif mode == 3:
        i = 0
        is_correct = True
        pk_name = 'pk.txt'
        sk_name = 'sk.txt'
        while i < len(args):
            if i == 0:
                pk_name = str(args[i])
            elif i == 1:
                sk_name = str(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct and len(args) < 3:
            mode_three(pk_name, sk_name)
    elif mode == 4:
        i = 0
        is_correct = True
        pk_name = 'pk.txt'
        message_name = 'message.txt'
        en_message = 'en_message.txt'
        is_random_message = True
        while i < len(args):
            if i == 0:
                pk_name = str(args[i])
            elif i == 1:
                message_name = str(args[i])
            elif i == 2:
                en_message = str(args[i])
            elif i == 3:
                is_random_message = bool(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct:
            mode_four(pk_name, message_name, en_message, is_random_message)
    elif mode == 5:
        i = 0
        is_correct = True
        sk_name = 'sk.txt'
        en_message = 'en_message.txt'
        de_message = 'de_message.txt'
        while i < len(args):
            if i == 0:
                sk_name = str(args[i])
            elif i == 1:
                en_message = str(args[i])
            elif i == 2:
                de_message = str(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct:
            mode_five(sk_name, en_message, de_message)
    elif mode == 6:
        i = 0
        is_correct = True
        r = 0
        m = 0
        message = 'en_message.txt'
        while i < len(args):
            if i == 0:
                r = int(args[i])
            elif i == 1:
                m = int(args[i])
            elif i == 2:
                message = str(args[i])
            else:
                print('Слишком много аргументов')
                is_correct = False
            i += 1
        if is_correct and len(args) > 1:
            mode_six(r, m, message)
    else:
        print('Такого режима нет')


# In[ ]:

if __name__ == '__main__':
    main()


