CREATE TABLE tb_activity (
	pk_activity_id integer PRIAMRY KEY,
	fk_strava_activity_id integer not null unique,
	start_date datetimeoffset NOT NULL,
	name text not null,
	type integer not null,
	distance real not null1
);

CREATE TABLE tb_award (
	pk_award_id integer PRIAMRY KEY,
	fk_user_id integer not null,
	name text not null,
	datetime_start datetimeoffset NOT NULL,
	datetime_end datetimeoffset NOT NULL,
	type_id integer not null,
	datetime_created datetimeoffset NOT NULL
);
   	
