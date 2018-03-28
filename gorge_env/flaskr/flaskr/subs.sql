drop table if exists subscriptions;
create table subscriptions (
	id integer primary key autoincrement,
	userid integer not null,
	postid integer not null,
	viewed boolean not null,
);