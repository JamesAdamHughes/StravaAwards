select count(*) from (
    select strftime('%W', start_date) weekNo, count(*)
        from tb_activity
            where 1=1
                and start_date > '2017-05-29 00:00:00+01:00'
                and start_date < '2017-05-30 00:00:00+01:00'
                and type = 0
        group by weekNo
        having count(*) > 0
    )
;