create table if not exists contacts(
studentid varchar(32) not null primary key,
name varchar(32) not null,
gender varchar(32) not null,
grade varchar(32),
mobile varchar(32),
email varchar(32),
living_area varchar(32),
employer varchar(32),
sns varchar(32),
field_1 varchar(32),
field_2 varchar(32)
) default character set utf8;

create table if not exists fields(
id int(32) not null auto_increment primary key,
field varchar(32) not null,
field_name varchar(32) not null
) default character set utf8;

create table if not exists users(
id int(32) not null auto_increment primary key,
username varchar(32) not null,
password   varchar(32) not null,
salt varchar(32) not null,
available boolean not null
) default character set utf8;

insert into fields(field, field_name) values
('studentid', '学号'),
('name', '姓名'),
('gender', '性别'),
('grade', '年级专业班级'),
('mobile', '手机号'),
('email', '邮箱'),
('living_area', '所在地区'),
('employer', '工作单位'),
('sns', '社交网络'),
('field_1', '备注1'),
('field_2' , '备注2');

-- for test only:
insert into users(username, password, salt, available) values
	('admin', 'f38a02ea409ec7ca45fabe75163fe3f5', '77B6-C278-4F32-958D-4B16', true);