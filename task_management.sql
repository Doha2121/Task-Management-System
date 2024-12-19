create database task_management;
use task;
CREATE TABLE person (
    person_id INT NOT NULL, -- Define the primary key column
    username VARCHAR(15),
    password VARCHAR(15),
    gender VARCHAR(10),
    PRIMARY KEY (person_id) -- Declare the primary key constraint
);
select * from person;

CREATE TABLE task (
    task_id INT NOT NULL, -- Define the primary key column
    status VARCHAR(15),
    taskname VARCHAR(15),
    taskdescription VARCHAR(10),
    tasktime TIME,
    PRIMARY KEY (task_id) -- Declare the primary key constraint
);
select * from task;

CREATE TABLE do_task (
    task_id INT,
    person_id INT,
    PRIMARY KEY (task_id, person_id) 
);
ALTER TABLE do_task
ADD FOREIGN KEY (task_id)
REFERENCES task(task_id)
ON DELETE NO ACTION
ON UPDATE CASCADE;


ALTER TABLE do_task
ADD FOREIGN KEY (person_id)
REFERENCES person(person_id)
ON DELETE NO ACTION
ON UPDATE CASCADE;




