CREATE TABLE tb_activity (
	pk_activity_id integer PRIAMRY KEY,
	fk_strava_activity_id integer not null unique,
	start_date datetimeoffset NOT NULL,
	name text not null,
	type integer not null
);

   	
