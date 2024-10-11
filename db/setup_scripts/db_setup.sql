-- create tables
create table users (
  email varchar(63) primary key,
  password varchar(63),
  lang varchar(63)
);

create table sources (
  email varchar(63),
  url varchar(255),
  primary key (email, url),
  foreign key (email) references users(email)
);
