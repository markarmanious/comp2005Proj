drop table if exists userGroups;
create table userGroups (
	groupName text primary key not null,
	usersInGroup text not null,
	CHECK(groupName <> '' and usersInGroup <> '')
);
