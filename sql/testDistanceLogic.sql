select count(distance) 
from tb_activity
where 1=1
    and start_date > '2017-07-15 15:44:16'
    and start_date < '2017-07-23 23:44:16'
    and type = 0 
