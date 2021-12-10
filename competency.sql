CREATE TABLE "Users" (
	"user_id"	INTEGER,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT,
	"phone"	TEXT,
	"email"	TEXT UNIQUE,
	"password"	TEXT,
	"hire_date"	TEXT,
	"date_created"	TEXT,
	"active"	INTEGER DEFAULT 1,
	"user_type"	INTEGER DEFAULT 0,
	FOREIGN KEY("user_id") REFERENCES "Competencies"("competency_id"),
	PRIMARY KEY("user_id" AUTOINCREMENT)
);

CREATE TABLE "Competencies" (
	"competency_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	"date_created"	TEXT,
	PRIMARY KEY("competency_id" AUTOINCREMENT)
);

CREATE TABLE "Assessments" (
	"assessment_id"	INTEGER UNIQUE,
	"competency_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"description"	,
	PRIMARY KEY("assessment_id" AUTOINCREMENT)
);

CREATE TABLE "Competency_Assessment_Results" (
	"result_id"	INTEGER,
	"user_id"	INTEGER,
	"competency_id"	INTEGER,
	"assessment_id"	INTEGER,
	"score"	INTEGER NOT NULL,
	"date_taken"	TEXT,
	"active"	INTEGER DEFAULT 1,
	FOREIGN KEY("assessment_id") REFERENCES "Assessments"("assessment_id"),
	FOREIGN KEY("competency_id") REFERENCES "Competencies",
	FOREIGN KEY("user_id") REFERENCES "Users"("user_id"),
	PRIMARY KEY("result_id" AUTOINCREMENT)
);