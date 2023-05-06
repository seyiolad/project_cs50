

CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    student_name TEXT
);

CREATE TABLE houses (
    id INTEGER PRIMARY KEY,
    house TEXT
);


CREATE TABLE house_assignment (
    id INTEGER PRIMARY KEY,
    head TEXT,
    id_house INTEGER,
    id_student INTEGER,
    FOREIGN KEY(id_house) REFERENCES houses(id),
    FOREIGN KEY(id_student) REFERENCES student(id)
);