import sys
import re
import numpy as np
import itertools
import math

def transform_to_float(list):
    neg = 1
    vir = 0
    i = 0
    new_list = []
    for item in list:
        num = 0
        num2 = 0
        numfinal = 0
        mult = 1
        j = 1
        size = len(item)
        if item[0] == '-':
            neg = -1
            i = i + 1
        else :
            neg = 1
        if '.' in item :
            pos = item.index('.')
            while(size - j > pos):
                num = num + float(item[size-j]) * mult
                mult = mult * 10
                j = j + 1
            num = num / mult
            j = 1
            mult = 1
            while(j >= 1):
                num2 = num2 + float(item[pos-j]) * mult
                mult = mult * 10
                j = j - 1
            numfinal = (num2 + num) * neg
            new_list.append(float(numfinal))
        else:
            while(size - j >= 0):
                if item[size-j] != '-':
                    num = num + int(item[size-j]) * mult * neg
                    mult = mult * 10
                j = j + 1
            new_list.append(int(num))
    return new_list

def parser_expo(argv):
    #Fonction qui enregistre tous les exposants qui se trouve dans l'equation(argv) et retire les doublons
    list_index_expo = [i for i in range(len(argv)) if argv.startswith("*X^", i)]
    list_expo = []
    for item in list_index_expo:
        y = item + 3
        count = 0
        neg = 0
        list_tmp = []
        if(argv[y] == '-'):
            neg = -1
            list_tmp.append(argv[y])
            y = y + 1
        while y < len(argv) and (argv[y].isdigit() or argv[y] == '.'):
            list_tmp.append(argv[y])
            y = y + 1
        list_expo.append(list_tmp)
    list_expo = sorted(list(set(transform_to_float(list_expo))))
    return list_expo

def find_all(a_str, sub):
    #Fonction qui trouve les occurences et enregistre dans une liste les indexs de ces occurences
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def get_num_part(list_tmp,pos,x):
    num = 0
    mult = 1
    if x == 0:
        i = pos + 1
        while i < len(list_tmp)-1:
            num += float(list_tmp[i]) * mult
            mult *= 10
            i += 1
        return num
    elif x == 1:
        i = 0
        while i < pos:
            num += int(list_tmp[i]) * mult
            mult *= 10
            i += 1
        numfinal = float(num) / mult
        return numfinal
    elif x == 3:
        i = 0
        while i < len(list_tmp) - 1:
            num += int(list_tmp[i]) * mult
            mult *= 10
            i += 1
        return num
    
def transform_list_to_num(list_tmp):
    i = 0
    len_tmp = len(list_tmp)
    index_sign = len_tmp-1
    if list_tmp[index_sign] == '-':
        neg = -1
    else:
        neg = 1
    if '.' in list_tmp:
        pos_point = list_tmp.index('.')
        pre_part = len(list_tmp) - 2 - pos_point
        num_pre_part = get_num_part(list_tmp,pos_point, 0)
        num_post_part = get_num_part(list_tmp,pos_point, 1)
        num = (num_pre_part + num_post_part) * neg
    else:
        num = get_num_part(list_tmp,0,3) * neg
    return num

def get_num_from_argv(index,argv):
    i = index-1
    list_tmp = []
    pos_equal = argv.index('=')
    while (argv[i].isdigit() or argv[i] == '.') and i >= 0:
        list_tmp.append(argv[i])
        i = i - 1
        if argv[i] == '-' and i > pos_equal:
            list_tmp.append('+')
        elif argv[i] == '+' and i > pos_equal:
            list_tmp.append('-')
        elif argv[i] == '-' and i < pos_equal:
            list_tmp.append('-')
        elif argv[i] == '+' and i < pos_equal:
            list_tmp.append('+')
        elif i < 0:
            list_tmp.append('+')
        elif argv[i] == '=':
            list_tmp.append('-')
    num = transform_list_to_num(list_tmp)
    return num

def find_all_args(list_index_args,argv):
    #Fonction pour enregistrer dans une liste les arguments sous formes de nombres afin de pouvoir efectuer des operations
    i = 0
    j = 0
    list_num = []
    while i < len(list_index_args):
        j = 0
        if isinstance(list_index_args[i], list):
            num = 0
            while j < len(list_index_args[i]):
                num += get_num_from_argv(list_index_args[i][j],argv)
                j += 1
            list_num.append(num)
        i += 1
    list_index_args = reconstruct_list2(list_index_args, list_num)
    return list_index_args

def recontruct_list(list_tmp, list_index_args):
    i = 0
    j = 0
    list_index_args = list_index_args[::-1]
    list_tmp = list_tmp[::-1]
    while i < len(list_index_args):
        if i % 2 != 0 and j < len(list_tmp):
            list_index_args[i] = list_tmp[j]
            j += 1
        i += 1
    return list_index_args

def reconstruct_list2(list_index_args, list_num):
    i = 0
    j = 0
    while i < len(list_index_args):
        if isinstance(list_index_args[i], list):
            list_index_args[i] = list_num[j]
            j += 1
        i += 1
    i = 0
    return list_index_args

def remove_duplicate(list_index_args):
    list_index_args = list_index_args[::-1]
    list_tmp = []
    i = 0
    while i < len(list_index_args):
        #on regarde si element de la list est une list
        if isinstance(list_index_args[i], list):
            list_tmp.append(list_index_args[i])
        i += 1
    #on a list_tmp qui contient tous les array 
    i = 0
    while i < len(list_tmp):
        j = 0
        while j < len(list_tmp[i]):
            check_if_its_in(list_tmp,i,j)
            j += 1
        i += 1
    return recontruct_list(list_tmp, list_index_args)

def check_if_its_in(list_tmp,i,j):
    tmp = list_tmp[i][j]
    i = i + 1
    while i < len(list_tmp):
        j = 0
        while j < len(list_tmp[i]): 
            if tmp == list_tmp[i][j]:
                list_tmp[i].pop(j)
            j += 1
        i += 1

def parser_args(argv, list_expo):
    list_index_args = []
    list_final = []
    for expo in list_expo:
        list_index_args.append(expo)
        string = "*X^"+str(expo)
        list_args_by_expo = list(find_all(argv,string))
        list_index_args.append(list_args_by_expo)
    #On retire les doublons ex: *X^1 *X^1.1 *X^11
    list_index_args = remove_duplicate(list_index_args)
    #On utilise list_index_args pour trouver les args afin de pouvoir les additionner et de pouvoir presenter la forme reduite de l'equation"
    list_final = find_all_args(list_index_args,argv)
    return list_final

def swap_list(list_args):
    i = 0
    while i < len(list_args):
        tmp = list_args[i]
        list_args[i] = list_args[i+1]
        list_args[i+1] = tmp
        i += 2
    return list_args

def get_short_writing(list_args):
    i = 0
    new_str = ""
    list_args = swap_list(list_args)
    while i < len(list_args):
        if i % 2 == 0:
            if list_args[i] < 0:
                new_str += '- '
                neg = -1
            elif list_args[i] >= 0 and i > 0:
                new_str += '+ '
                neg = 1
            else:
                neg = 1
            new_str += str(list_args[i]*neg)+" "
        else:
            new_str += "* X^"+str(list_args[i])+" "
        i += 1
    new_str += "= 0"
    return new_str

def find_max_pow(list_args):
    i = 0
    expo_max = -100
    while i < len(list_args):
        if i % 2 == 0:
            if list_args[i] > expo_max:
                expo_max = list_args[i]
        i += 1
    return expo_max

def find_min_pow(list_args):
    i = 0
    expo_min = 1000000000000000
    while i < len(list_args):
        if i % 2 == 0:
            if list_args[i] < expo_min:
                expo_min = list_args[i]
        i += 1
    return expo_min

def find_dot(list_args):
    i = 0
    ret = 0
    while i < len(list_args):
        if i % 2 == 0:
            if isinstance(list_args[i], float):
                ret = 1
        i += 1
    return ret

def start_calcul(list_args):
    max_pow = find_max_pow(list_args)
    min_pow = find_min_pow(list_args)
    is_expo_float = find_dot(list_args)
    short_writing = get_short_writing(list_args) 
    print short_writing
    if max_pow > 2:
        print "The polynomial degree is stricly greater than 2, I can't solve."
    elif min_pow < 0 or max_pow < 0:
        print "Cannot solve equation with negatif power"
    elif is_expo_float == 1:
        print "Cannot solve equation with float power"
    elif max_pow <= 2 and is_expo_float == 0 and min_pow >= 0:
        resolve_equation(list_args)
    
def calcul_solution_pow1(list_args):
    x0 = 0
    x1 = 0
    i = 0
    while i < len(list_args):
        if i % 2 == 0 and list_args[i] == 0:
            x0 = list_args[i+1]
        elif i % 2 == 0 and list_args[i] == 1:
            x1 = list_args[i+1]
        i += 1
    result = float(x0) / float(x1)
    print result   

def calcul_solution_pow2(a,b,c,d,list_args):
    if d > 0:
        print "Discriminant is strictly positive, the two solutions are:"
        x1 = (-b - math.sqrt(d)) / float(2*a)
        x2 = (-b + math.sqrt(d)) / float(2*a)
        print "%0.6f" % x1
        print "%0.6f" % x2
    elif d == 0:
        print "Discriminant is null, the solution is:"
        x1 = (-b) / float(2*a)
        print "%0.6f" % x1
    elif d < 0:
        d = -d
        x1_0 = -b / (2*a)
        x1_1 = -(math.sqrt(d))/float(2*a)
        x2_1 = (math.sqrt(d))/float(2*a)
        if x1_1 < 0:
            x1_1 = - x1_1
            tmp_x1_1 = " - "+str(x1_1)+"i"
        else:
            tmp_x1_1 = " + "+str(x1_1)+"i"
        if x2_1 < 0:
            x2_1 = - x2_1
            tmp_x2_1 = " - "+str(x2_1)+"i"
        else:
            tmp_x2_1 = " + "+str(x2_1)+"i"
        tmp_x1 = str(x1_0)+tmp_x1_1
        tmp_x2 = str(x1_0)+tmp_x2_1
        print "Discriminant is negativ, no real solutions but the two complex solutions"
        print tmp_x1
        print tmp_x2

def special_case(list_args):
    if len(list_args) == 0:
        print "Tous les solutions dans R"
        return 1
    elif len(list_args) == 2:
        if list_args[1] == 0:
            print "Impossible"
            return 1
        elif list_args[1] == 1:
            print "Tous les solutions dans R"
            return 1
        elif list_args[1] == 2:
            print "Solution est 0"
            return 1
    else :
        return 0

def calcul_solution(a,b,c,d,list_args):
    test = special_case(list_args)
    max_pow = find_max_pow(swap_list(list_args))
    if max_pow < 2 and test == 0:
        calcul_solution_pow1(list_args)
    elif max_pow == 2 and test == 0:
        calcul_solution_pow2(a,b,c,d,list_args)

def calcul_discriminant(list_args):
    i = 0
    a = 0
    b = 0
    c = 0
    d = 0
    while i < len(list_args):
        if i % 2 != 0:
            if list_args[i] == 2:
                a = list_args[i-1]
            elif list_args[i] == 1:
                b = list_args[i-1]
            elif list_args[i] == 0:
                c = list_args[i-1]
        i += 1
    d = b*b - 4*a*c
    calcul_solution(a,b,c,d,list_args)

def check_equation(list_args):
    i = 0
    while i < len(list_args):
        if i % 2 == 0 and list_args[i] == 0:
            del list_args[i]
            del list_args[i]
        i += 1
    return list_args

def resolve_equation(list_args):
    test = check_equation(list_args)
    calcul_discriminant(test)

def parse_argv(argv):
    list_expo = parser_expo(argv)
    list_args = parser_args(argv, list_expo)
    start_calcul(list_args)

def main():
    if len(sys.argv) < 2:
        print("Enter an equation")
    elif len(sys.argv) > 2:
        print("Enter only one equation")
    else :
        parse_argv(sys.argv[1].replace(" ",""))

main ()