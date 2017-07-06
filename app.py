import vk
import logging
import sqlite3
import logging
import unittest

vk_api=object()
def poptime(l,eps):
    k=0
    for i in l:
        k=k+1
    poptimes=k//eps
    return poptimes

    
def initparser(public,deep):
    eps=5
    bad_list=get_bad_wallist(public,deep)
    good_list=bad_to_good(bad_list)
    good_list.sort(key=lambda item: item[1])
    final=good_to_final(good_list)
    final_no_dublicate=dublicate(final)
    final_no_dublicate_shorted=[]
    x=poptime( final_no_dublicate, eps)
    for i in range(x):
        final_no_dublicate_shorted.append(final_no_dublicate.pop())
        
    return final_no_dublicate_shorted

def insert_to_big_DB(l):
    big_DB = sqlite3.connect('big_aneks.db')
    c=big_DB.cursor()
    c.executemany('INSERT INTO aneks VALUES(?)',[[a] for a in l])
    big_DB.commit()    

def connect_to_vk(appid,number,password):
     session = vk.AuthSession(appid, number, password, scope='wall, messages')
     global vk_api
     vk_api=vk.API(session)
     
def unique(lst):
    seen = set()
    result = []
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
        result.append(x)
    return result

def main():
    deep=5
    connect_to_vk('6015549', '+79117381261', 'pass')
    if isempty:
        temp_list=[]
        spisok=['anekdodator']
        for i in spisok:
            temp_list=temp_list+initparser(i,deep)
        uniq_temp_list=unique(temp_list)
        uniq_final_list=dublicate(uniq_temp_list)
        list_to_DB(uniq_final_list)
        insert_to_big_DB(uniq_final_list)
    poster()
    
    
def get_bad_wallist(name,num):
     s = vk_api.wall.get(domain=name, count=num)
     s.pop(0)
     return s
    
def bad_to_good(badone):
    goodone=[]
    for i in badone:
        if (i.get('attachment','Never')) != 'Never':
            badone.remove(i)
    for i in badone:
        goodone.append([i['text'],i['likes']['count']])
    return goodone

def good_to_final(s):
    bestone=[]
    for i in s:
        bestone.append(i.pop(0))
    return bestone

def list_to_DB(l):
    conn = sqlite3.connect('temp_aneks.db')
    c = conn.cursor()
    c.executemany('INSERT INTO aneks VALUES(?)',[[a] for a in l])
    conn.commit()

def poster():
    pass

def isempty():
    conn = sqlite3.connect('temp_aneks.db')
    if conn.execute('SELECT * FROM aneks').fetchall()==[]:
        return True
    else:
        return False
def dublicate(final):
    big_DB = sqlite3.connect('big_aneks.db')
    DBspisok=big_DB.execute('SELECT * FROM aneks').fetchall()
    for i in DBspisok:
        for j in final:
            if i[0]==j:
                final.remove(j)
    return final
class Tests(unittest.TestCase):
    def test_lists_1(self):
        self.assertEqual(initparser('testgroupnum2',6), ['Quatre'] )
    def test_lists_2(self):
        self.assertEqual(initparser('testgroupnum1',6),['Трииис'])
        

    
if __name__ == '__main__':
    main()
    unittest.main()

