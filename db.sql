create table if not exists logins
(
	id serial not null,
	email text,
	pass text,
	date timestamp
);


create unique index if not exists logins_email_uindex
	on logins (email);

create unique index if not exists logins_id_uindex
	on logins (id);

