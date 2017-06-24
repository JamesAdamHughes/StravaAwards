delete from tb_activity;

insert into tb_activity (
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