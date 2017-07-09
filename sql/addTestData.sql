delete from tb_activity;
delete from tb_award;

insert OR IGNORE into tb_activity (
    fk_strava_activity_id,
    start_date,
    name,
    type
) values (
    1029,
    '2017-05-22T00:00:00+01:00',
    'Test Run1',
    2
),
(
    1030,
    '2017-05-22T00:00:00+01:00',
    'Test Run2',
    2
);

insert into tb_award (
    fk_user_id,
	datetime_start,
	datetime_end,
	type_id,
	datetime_created
) values (
    1,
    '2017-06-19T00:00:00+01:00',
    '2017-06-30T00:00:00+01:00',
    3,
    '2017-07-09T00:00:00+01:00',
);
