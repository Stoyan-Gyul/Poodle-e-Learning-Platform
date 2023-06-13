
-- Insert data into the users table
INSERT INTO users (id, email, password, first_name, last_name, role, verification_token, is_verified, is_approved)
VALUES
    (1, 'alice@abv.bg', '$2b$12$Xag4rXZGOJrNkwRb32N6s.nscNQFlIfJSYhJXgHrFebVGgjj8Ve9K', 'Alice', 'Parker100', 'teacher', NULL, 0, 1),
    (2, 'steven@abv.bg', '$2b$12$ooercgclJ9NziweYJC8nSunM8LJ43PE0EvxTv8cul/7kdNTolGqMm', 'Steven', 'Parker100', 'student', NULL, 0, 1),
    (3, 'steven1@abv.bg', '$2b$12$yUT0WH0qklpI15Y7jXqyVe3.j6DCJVo4HsjrYBdIoLTB684/YLBTu', 'Steven1', 'Parker1', 'student', 'e399f595-5312-4ba1-bb74-64c46dc5bcd2', 1, 1),
    (4, 'steven2@abv.bg', '$2b$12$3cUVOilSyrfMNZ5LjPUKT.68P/OY7qVYL/VrVM6mpWUTx192xza8K', 'Steven2', 'Parker2', 'student', '77dc7699-4e3f-448a-9133-fb676d8b373b', 1, 0),
    (5, 'admin@abv.bg', '$2b$12$at3uULHSgb2zV6nrIJLP7uuSITMvZbMw68gA54Lfpy9OvV7saevaO', 'Admin', 'Adminov', 'admin', '77dc7699-4e3f-448a-9133-fb676d8b373b', 0, 1);

-- Insert data into the teachers table
INSERT INTO teachers (users_id, phone_number, linked_in_account)
VALUES
    (1, '888345600', 'www.linkedin.com/aliceparker100');

-- Insert data into the courses table
INSERT INTO courses (id, title, description, home_page_pic, owner_id, is_active, is_premium, course_rating)
VALUES
    (1, 'Core Python', 'This is core module', null, 1, 0, 0, 8.0),
    (2, 'OOP', 'This is OOP module', null, 1, 1, 1, 6.5),
    (4, 'General Python', 'This is general', null, 1, 0, 1, 7.0);

-- Insert data into the users_have_courses table
INSERT INTO users_have_courses (users_id, courses_id, status, rating, progress)
VALUES
    (2, 1, 1, 8, NULL),
    (2, 2, 1, 6, NULL),
    (3, 2, 1, 7, NULL),
    (3, 4, 1, 7, NULL);

-- Insert data into the objectives table
INSERT INTO objectives (id, description)
VALUES
    (1, 'Learn software'),
    (2, 'General view');

-- Insert data into the courses_have_objectives table
INSERT INTO courses_have_objectives (objectives_id, courses_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 4);

-- Insert data into the tags table
INSERT INTO tags (id, expertise_area)
VALUES
    (1, 'software development');

-- Insert data into the courses_have_tags table
INSERT INTO courses_have_tags (courses_id, tags_id)
VALUES
    (1, 1),
    (2, 1),
    (4, 1);

-- Insert data into the sections table
INSERT INTO sections (id, title, content, description, external_link, courses_id)
VALUES
    (1, 'Basics', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse lobortis velit id orci vestibulum mollis eget in lectus. Vestibulum massa lorem, volutpat a augue id, egestas tristique mi. Suspendisse potenti. Suspendisse iaculis tincidunt lacus. Ves...', 'Explain the basics', 'any', 1),
    (2, 'Tuples', 'Integer gravida, lectus non interdum rutrum, metus ex tempor orci, id venenatis lectus odio imperdiet nibh. Integer pellentesque neque in ultrices consectetur. Etiam luctus magna vitae nisl maximus sodales. Maecenas eget justo efficitur quam effi...', 'Explain tuples', 'any', 1),
    (3, 'Dicts', 'Vivamus lorem elit, luctus quis neque ut, congue venenatis purus. In rutrum ullamcorper nisl, at euismod urna aliquam sed. Curabitur ut velit magna. Donec quis sem vel felis pretium accumsan. Donec tempus ullamcorper risus, sed tristique orci. Class ap...', 'Explain dictionaries', 'any', 1),
    (4, 'Basic OOP', 'Aenean commodo bibendum mi id efficitur. Nam auctor, mauris eget blandit lacinia, turpis erat mattis felis, nec feugiat est justo eget leo. Suspendisse potenti. Cras sodales sapien lacus, vel pretium nunc tempus at. Maecenas sed ex quis sapien ornare g...', 'Explain basic OOP', 'any', 2),
    (5, 'Abstractions', 'Morbi ut arcu risus. Phasellus porta commodo lorem, vitae faucibus ipsum commodo in. Aliquam ornare, nunc vel luctus vulputate, ipsum dui gravida leo, dapibus euismod ligula nisi non dolor. Sed sodales ante est, ac scelerisque elit dignissim sed. Sed in...', 'Explain Abstraction', 'any', 2);
