import vk
import logging
import sqlite3
import logging

vk_api=object()
deep=6
    
def initparser(public):
    bad_list=get_bad_wallist(public,deep)
    good_list=bad_to_good(bad_list)
    good_list.sort(key=lambda item: item[1])
    final=good_to_final(good_list)
    
    final_no_dublicate=dublicate(final)
    return final_no_dublicate

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
    temp_list=[]
    spisok=['anekdodator']
    connect_to_vk('6015549', '+79117381261', 'pass')
    for i in spisok:
        temp_list=temp_list+initparser(i)
    uniq_temp_list=unique(temp_list)
    uniq_final_list=dublicate(uniq_temp_list)
    list_to_DB(uniq_final_list)
    insert_to_big_DB(uniq_final_list)
    
    
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

def if_empty():
    pass

def dublicate(final):
    big_DB = sqlite3.connect('big_aneks.db')
    DBspisok=big_DB.execute('SELECT * FROM aneks').fetchall()
    for i in DBspisok:
        for j in final:
            if i[0]==j:
                final.remove(j)
    return final
                
    
if __name__ == '__main__':
    main()

