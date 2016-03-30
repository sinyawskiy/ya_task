#-*- coding: utf-8 -*-

#
# cat access.log| cut -d ' ' -f 1|sort|uniq -c|sort -n | tail -n 10|sort -rn
#

import re
import os

if __name__ == '__main__':
    file_name = 'access.log'
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    result_dict = {}
    IP_PATTERN = re.compile('(.*) - - ')

    with open(file_path) as f:
        for line in f.readlines():
            result = re.findall(IP_PATTERN, line)
            try:
                result_dict[result[0]]
            except KeyError:
                result_dict[result[0]] = 1
            else:
                result_dict[result[0]] += 1

        for key, value in sorted(result_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:10]:
            print "%s: %s" % (key, value)