-- TODO: ADD all command we have to run on mysql

CREATE DATABASE doubi；
CREATE TABLE Demo(id BIGINT(64) NOT NULL PRIMARY KEY,text varchar(500) CHARACTER SET utf8mb4,followers_count int,favorite_count INT,retweet_count INT,created_at varchar(255));

CREATE TABLE TeslaTwitterAnalysisByOneDayFifteenMin(date VARCHAR(50) NOT NULL PRIMARY KEY,yyyymm CHAR(7), day INT,hour INT,quarters INT, median DOUBLE,mean DOUBLE,weighted_median DOUBLE,weighted_mean DOUBLE,count INT,zero_count INT);
CREATE TABLE TeslaTwitterAnalysisByOneDaySixtyMin(date VARCHAR(50) NOT NULL PRIMARY KEY,yyyymm CHAR(7), day INT,hour INT,quarters INT, median DOUBLE,mean DOUBLE,weighted_median DOUBLE,weighted_mean DOUBLE,count INT,zero_count INT);