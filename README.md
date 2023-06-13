# Poodle e-Learning Platform

## Getting started

The API of the project is in production on https://hydraulic-manifold.bg

The deployment of the frontend is in progress. Please, be patient! 

## Name
Poodle E-learning platform

## Description
This platform is used by students to search for online courses and enroll in maximum 5 premium ones AND teachers to publish their courses.

## Installation
All dependencies are listed in requirements.txt. 
The frontend part requires installation of Node.js

## Usage
The platform allows free access to a public part. The non-public one is accessable to registered users only.

The non-authenticated users are allowed to view the title, description and tags of available public courses but without opening them. They can search courses by tag and/or rating.

The access rights of registered users depend on their role.
The platform defines three types of users: students, teachers and admin.
1. The Student can:
    - view and edit their account information (except the username);
    - track their progress for every course based on the sections that they have visited;
    - view the courses that they are enrolled in (both public and premium);
    - view and search through by name and tag existing public and premium courses;
    - unsubscribe from premium courses;
    - rate a course (only one score for a course) only if they are enrolled in it;
    - subscribe to a maximum of 5 premium courses at a time and unlimited number of public courses.
2. The Teacher can:
    - view and edit their account information (except the username);
    - create courses, view and update their own courses;
    - be notified via email whenever an enrollment request is sent by a student for a specific course that they own;
    - approve enrollment requests sent by students;
    - deactivate / hide only courses to which they are owners when there are no students subscribed for that course;
    - run report for the past and current students that have subscribed for their courses.
3. The Admin can:
    - approve registrations for teachers;
    - view a list with all public and premium courses, the number of students in them and their rating;
    - deactivate/reactivate students;
    - delete / hide courses and the enrolled students receive a notification that the course is no longer active;
    - remove students from courses;
    - search through courses filtered by teacher and/or by student;
    - trace back ratings for courses to identify the students who scored the course.

The following information is stored for:
1. Users:
   - email, first name, last name, and a password. Note: The email serves as a username and cannot be amended;
   - teachers also have a phone number and linked-in account.
2. Courses:
   - title (unique), description, objectives, owner (teacher), tags with relevant expertise areas and sections;
   - optionally have a Home Page picture;
   - a rating which represents a proportionate value of the provided scores. As an example if 2 people rate a course with 7 out of 10 and 6 out of 10, then the calculated rating would be 7 plus 6 divided by 20 ( 7 + 6 = 13 / 20 = 0.65). The rating would be 6.5 out of 10.
3. Sections:
   - title, content type, description (optional), information / link to external resource(optional).

The above information is stored in a relational database MariaDB 10.11.2.

[Alt text](data_base/Schema_Model.png)

The SQL script E-learning_schema.sql is in data_base directory.

For testing purposes, fake data in DATA-E-learning_schema.sql is provided in the same directory.
## Support
Support is not provided.

## Roadmap
Future developements are not forseen.
## Authors and acknowledgment
TMS - Group 8 Alpha45 Telerik Academy. 
THANKS to our trainers and mentor for the provided support.

## License
Open Source License.

## Project status
The project is delivered.
