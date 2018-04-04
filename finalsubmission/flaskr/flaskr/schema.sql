drop table if exists posts;
drop table if exists topics;
drop table if exists users;
drop table if exists subs;
drop table if exists userGroups;
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
  groupDisscution text,
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
create table Users (
  id integer primary key autoincrement,
  username text not null,
  pass text not null,
  question text,
  answer text,
  isLoggedIn integer
);


create table userGroups (
	groupName text primary key not null,
	usersInGroup text not null,
	CHECK(groupName <> '' and usersInGroup <> '')
);

insert into Users (id,username,pass,isLoggedIn,question,answer) values (1,'mark','password',0,'whats your name','mark');
insert into topics (id,userId,groupDisscution,title) values (1,1,'computerScience','welcome');
insert into subs (id,userId,topicId,notified) values (1,1,1,0);
insert into posts (id,userId,title,content,topic) values (1,1,'welcome','welcome to out application',1);
insert into userGroups (groupName,usersInGroup) values ('computerScience','mark');
