drop table if exists posts;
drop table if exists topics;
create table posts (
  id integer primary key autoincrement,
  userId integer,
  title text not null,
  content text not null,
  topic integer not null,	
  createdAt timestamp default current_timestamp not null


);
create table topics (
  id integer primary key autoincrement,
  userId integer,
  title text not null,
  createdAt timestamp default current_timestamp not null
  


);

create table subs (
  id integer primary key autoincrement,
  userId integer not null,
  topicId integer not null,
  notified integer not null,
  createdAt timestamp default current_timestamp not null


);

