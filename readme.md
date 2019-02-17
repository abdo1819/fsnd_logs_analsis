# introduction

this python module for reporting data in news database

avilabe options are to :
* view top articles
* view top authors
* view days with high error rate


# using program
> python3 reporter.py [option [number] ]

### option:
* atricles
* author
* error
### number:
* any positive number for atricles,author
* precent from 0 to 100 for error report

sample usage
## run three queries

## (1) to view top three atricles 
> python3.7 reporter.py articles 3
```
Candidate is jerk, alleges rival        338647
Bears love berries, alleges bear        253801
Bad things gone, say good people        170098
```

## (2) to view top authors 
> python3.7 reporter.py author
```
Ursula La Multa               507594
Rudolf von Treppenwitz        423457
Anonymous Contributor         170098
Markoff Chaney                 84557
```

## (3) to view error precentage pathes 1%
> python3.7 reporter.py error 1
```
2016-07-17    2.3175416133162612
```

## view all qeuries
> python3.7 reporter.py

```

top articles:
Candidate is jerk, alleges rival          338647
Bears love berries, alleges bear          253801
Bad things gone, say good people          170098
Goats eat Google's lawn                    84906
Trouble for troubled troublemakers         84810
Balloon goons doomed                       84557
There are a lot of bears                   84504
Media obsessed with bears                  84383


top authors:
Ursula La Multa               507594
Rudolf von Treppenwitz        423457
Anonymous Contributor         170098
Markoff Chaney                 84557

error report:
2016-07-17    2.3175416133162612
```

## view error higher than .75%
> python3.7 reporter.py error .75
```
2016-07-05    0.78463952737007292532
2016-07-06    0.76126730779839288013
2016-07-08    0.76009501187648456057
2016-07-17    2.3175416133162612
2016-07-19    0.76763560956088332666
2016-07-21    0.76519896999470387348
2016-07-24    0.78554163920017578554
```
## to view top two authors 
> python3.7 reporter.py author 2
```
Ursula La Multa               507594
Rudolf von Treppenwitz        423457
```

# reqierd views
 you don't need to create those views they are already included in python source code as create or replace


## error count for every day
```sql
CREATE OR REPLACE view error_count as
select date(time) as date, count(*) as error
from log
where (status like '%%4%%' or status like '%%5%%')
group by date;
```
## success count for every day
```sql
CREATE OR REPLACE view success_count as
select date(time) as date , count(*) as success
from log
where (status like '%%2%%')
group by date;
```


# farther testing to check recived data data 
## verifay numbers of visits compare to top articles number
```sql
select count(*) from log 
where (log.status like '%%200%%') 
and (log.path like '%%/article/%%');
```
`1185706`

>python3.7 reporter.py articles
```
Candidate is jerk, alleges rival          338647
Bears love berries, alleges bear          253801
Bad things gone, say good people          170098
Goats eat Google's lawn                    84906
Trouble for troubled troublemakers         84810
Balloon goons doomed                       84557
There are a lot of bears                   84504
Media obsessed with bears                  84383
```
`338647+253801+170098+84906+84810+84557+84504+84383=1185706`

## finding spam urls
```sql
select path from log 
where not (path like '%/article/%' or path like '/') limit 20;
```
```
         path          
------------------------
 /+++ATH0
 /+++ATH0
 /+++ATH0
 /spam-spam-spam-humbug
 /+++ATH0
 /+++ATH0
 /%20%20%20
 /+++ATH0
 /%20%20%20
 /+++ATH0
 /%20%20%20
 /%20%20%20
```



# style checking
> pycodestyle reporter.py 
