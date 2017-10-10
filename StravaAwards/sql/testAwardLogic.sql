-- select count(*) from (
--             select strftime('%W', start_date) weekNo, count(*)
--             from tb_activity
--                 where 1=1
--                     and start_date > '2017-07-03 00:00:00+01:00'
--                     and start_date < '2017-07-09 00:00:00+01:00'
--                     and type = 0
--             group by weekNo
--             having count(*) > 0
--         );

    
-- select count(*) from (
--             select strftime('%W', start_date) weekNo, count(*)
--             from tb_activity
--                 where 1=1
--                     and start_date > '2017-07-03 15:44:16'
--                     and start_date < '2017-07-09 15:44:16'
--                     and type = 0
--             group by weekNo
--             having count(*) > 2
--         );

        select strftime('%W', start_date) weekNo, count(*)
            from tb_activity
                where 1=1
                    and start_date > '2017-07-03 15:44:16'
                    and start_date < '2017-07-09 15:44:16'
                    and type = 0
            group by weekNo
            having count(*) = 2;