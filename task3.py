# -*- coding: utf-8 -*-
#
# sqlite3 fs.sqlite < schema.sql
#
import re
from SQLiteHandler import SQLiteHandler
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = 'fs.sqlite'
SCHEMA_NAME = 'schema.sql'

class FileSystem(object):
    pwd = ''
    backslashes_regexp = re.compile(r"[/]{0,}$", re.IGNORECASE)

    def __init__(self):
        self.sql = SQLiteHandler(os.path.join(CURRENT_DIR, DATABASE_NAME))
        self.sql.connect()

    def __del__(self):
        self.sql.close()

    def cd(self, dir_name):
        dir_name = self.backslashes_regexp.sub(dir_name, '')
        if len(dir_name):
            abspath = u'%s%s' % (self.get_pwd(), dir_name)
        else:
            abspath = ''
        print abspath
        if self.is_dir(abspath if len(abspath) else '/'):
            self.pwd = abspath
            return True
        else:
            return False

    def get_pwd(self):
        if not self.pwd:
            self.cd('')
        return u'%s/' % self.pwd

    def ls(self, pwd=None):
        rows = self.sql.fetchAll(''' SELECT abspath FROM file WHERE abspath LIKE '%s%%' AND length>0; ''' % pwd or self.get_pwd())
        ls = []
        for row in rows:
            ls.append(row[0].rsplit('/', 1)[-1])
        return ls

    def get_file_attributes(self, abspath):
        return self.sql.fetchOne(''' SELECT attributes FROM file WHERE abspath='%s' AND length>0;''' % abspath)[0]

    def get_dir_attributes(self, abspath):
        return self.sql.fetchOne(''' SELECT attributes FROM file WHERE abspath='%s' AND length=0;''' % abspath)[0]

    def is_dir(self, abspath):
        result = self.sql.fetchOne('''SELECT COUNT(*) FROM file WHERE abspath='%s' AND length=0; ''' % abspath)
        return bool(result[0])

    def is_file(self, abspath):
        result = self.sql.fetchOne('''SELECT COUNT(*) FROM file WHERE abspath='%s' AND length>0; ''' % abspath)
        return bool(result[0])

    def exist(self, abspath, is_dir=True):
        if is_dir:
            return self.is_dir(abspath)
        else:
            return self.is_file(abspath)

    def touch(self, file_name):
        abspath = u'%s%s' % (self.get_pwd(), file_name)
        if not self.is_file(abspath):
            self.sql.execute(''' INSERT INTO file(abspath, length, attributes) VALUES ('%s', 1, '0777') ''' % abspath)
            self.sql.commit()
            return True
        return False

    def mkdir(self, dir_name, force=False):
        abspath = u'%s%s' % (self.get_pwd(), dir_name)
        if force or not self.is_dir(abspath):
            self.sql.execute(''' INSERT INTO file(abspath, length, attributes) VALUES ('%s', 0, '0644') ''' % abspath)
            self.sql.commit()
            return True
        return False

    def remove(self, abspath):
        self.sql.execute(''' DELETE FROM file WHERE abspath='%s' ''' % abspath)
        self.sql.commit()
        return True

if __name__ == '__main__':
    fs = FileSystem()
    if not fs.exist('/'):
        fs.mkdir('', force=True) # create root directory
    print fs.get_pwd()
    print fs.exist('/')
    print fs.cd('/')
    print fs.get_pwd()
    for item in xrange(10):
        fs.mkdir('dir_%d' % item)
    print fs.cd('dir_0')
    print fs.get_pwd()
    for item in xrange(10):
        fs.touch('file_%d.ext' % item)
    print fs.get_pwd()
    print fs.ls()
    print fs.get_dir_attributes('/dir_0')
    print fs.get_file_attributes('/dir_0/file_0.ext')