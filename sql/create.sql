drop table tb_activity;
drop table tb_award;
drop table tb_user;

CREATE TABLE tb_activity (
	pk_activity_id integer PRIAMRY KEY,
	fk_strava_activity_id integer not null unique,
	fk_user_id integer not null,
	start_date datetimeoffset NOT NULL,
	name text not null,
	type integer not null,
	distance real not null,
	moving_time real not null
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

CREATE TABLE tb_user (
	pk_user_id integer PRIMARY KEY,
	fk_strava_user_id integer not null unique,
	email_address text not null,
	first_name text not null,
	last_name text not null,
	gender text,
	access_token text not null,
	profile_image_url text,
	datetime_created datetimeoffset NOT NULL
);
   	
