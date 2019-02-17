#!/usr/bin/env python3.7
import psycopg2


# first question
def top_articals(num=99):
    """
    the most popular ? articles sorted by most viewed
    return list of articles and views for each
    """
    # create connection
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()

    # preparing reqierd table of
    #   articles.title   , views_count
    #   whith code 200 statue
    #   path contain /articales/<article slug>
    cur.execute('''
                select a.title , count(log.path)
                from log
                right join articles as a
                on (log.status like '%%200%%')
                and (log.path like concat('%%/article/%%',a.slug))
                group by a.title
                order by count desc
                limit %s;''', (num, ))

    res = cur.fetchall()

    # commit and closer connection
    db.commit()

    cur.close()
    db.close()
    return res


# second question
def top_author(num=99):
    """the most popular ? author sorted by page views"""
    # create connection
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()

    # creating list of author and  sum of view_count  for thier articles
    cur.execute('''SELECT authors.name, count(log.path)
                    from authors,articles,log
                    where (log.status like '%%200%%')
                    and (log.path like concat('%%/article/%%',articles.slug))
                    and authors.id = articles.author
                    group by authors.name
                    order by count desc
                    limit %s''', (num, ))

    res = cur.fetchall()

    # commit and close connection
    db.commit()

    cur.close()
    db.close()

    return res


# third question
def error_find(precentage=.01):
    """ error precentage higher than 1% default"""
    # create connection
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()

    # counting error by day
    # ignoring redirection statues 3xx
    # counting server and client error 4xx , 5xx

    # and date(time) = date(%s)
    cur.execute('''CREATE OR REPLACE view error_count as
                    select date(time) as date, count(*) as error
                    from log
                    where (status like '%%4%%' or status like '%%5%%')
                    group by date;''')

    # counting sucess by day
    # count suceess 2xx
    cur.execute('''CREATE OR REPLACE view success_count as
                    select date(time) as date , count(*) as success
                    from log
                    where (status like '%%2%%')
                    group by date;''')

    # fing date where error higher than precentage
    # multiplying first to convert ro float
    cur.execute('''SELECT er.date , (100.0*er.error)/sucs.success
                    from error_count as er ,success_count as sucs
                    where er.date = sucs.date
                    and cast(er.error as float)/sucs.success >= %s;''',
                (precentage, ))

    res = cur.fetchall()
    # commit and close connection
    db.commit()

    cur.close()
    db.close()

    return res


def view_data(res):
    '''
    print two coulomn data in formated way
    '''
    if len(res) == 0:
        print('no data')
        return
    width = max([len(str(i[0])) for i in res])+4
    for i in res:
        print('{:<{width}}{:>10}'.format(str(i[0]), i[1], width=width))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print('\ntop articles:')
        res = top_articals()
        view_data(res)

        print('\ntop authors:')
        res = top_author()
        view_data(res)

        print('\nerror report:')
        res = error_find()
        view_data(res)

    elif len(sys.argv) == 2:
        if (sys.argv[1] == 'articles'):
            res = top_articals()
        elif(sys.argv[1] == 'author'):
            res = top_author()
        elif(sys.argv[1] == 'error'):
            res = error_find()
        view_data(res)

    elif len(sys.argv) == 3:
        if (sys.argv[1] == 'articles'):
            res = top_articals(int(sys.argv[2]))
        elif(sys.argv[1] == 'author'):
            res = top_author(int(sys.argv[2]))
        elif(sys.argv[1] == 'error'):
            res = error_find(float(sys.argv[2])/100.0)
        view_data(res)
