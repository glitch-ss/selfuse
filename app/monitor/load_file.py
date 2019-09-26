#-*- coding:utf-8


def get_sus_list(file):
    a = []
    with open(file, 'r') as f:
        for l in f.readlines():
            a.append(l.strip())
        return a
