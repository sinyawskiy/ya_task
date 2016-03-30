# -*- coding: utf-8 -*-

from SQLiteHandler import SQLiteHandler
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = 'fs.sqlite'
SCHEMA_NAME = 'schema.sql'

class FileSystem(object):
    pwd = ''

    def __init__(self):
        self.sql = SQLiteHandler(os.path.join(CURRENT_DIR, DATABASE_NAME))
        self.sql.connect()

    def __del__(self):
        self.sql.close()

    def cd(self, abspath):
        # TODO проверить на существование пути в базе
        self.pwd = abspath

    def get_pwd(self):
        if not self.pwd:
            self.cd('')
        return self.pwd+'/'

    def ls(self):
        rows = self.sql.execute(''' select * from file where abspath like '%s%%'; ''' % self.get_pwd())
        ls = []
        for row in rows:
            ls.append(row[1])
        return ls

    def get_attributes(self, abspath):
        return self.sql.execute(''' select attributes from file where abspath='%s' ''' % abspath)

    def touch(self, file_name):
        self.sql.execute(''' insert into file(abspath, length, attributes) values ('%s%s', 1, '777') ''' % (self.get_pwd(), file_name))
        self.sql.commit()
        return

    def mkdir(self, dir_name):
        self.sql.execute(''' insert into file(abspath, length, attributes) values ('%s%s', 0, '777') ''' % (self.get_pwd(), dir_name))
        self.sql.commit()
        return

    def remove(self, abspath):
        self.sql.execute(''' delete from file where abspath='%s' ''' % abspath)
        self.sql.commit()
        return

if __name__ == '__main__':
    fs = FileSystem()
    fs.mkdir('/')


    # for item in xrange(1,10):
    #     fs.touch('test_%d.txt' % item)
