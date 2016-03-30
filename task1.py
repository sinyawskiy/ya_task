#-*- coding: utf-8 -*-

def create_dict(keys, values):
    return dict(map(None, keys, values[:len(keys)]))

if __name__ == '__main__':
    keys_list = ['key1', 'key2', 'key3']
    for values in [
            [1,2],
            [1,2,3],
            [1,2,3,4]
        ]:
        print 'keys: ', keys_list, 'values: ', values, 'result: ', create_dict(keys_list, values)