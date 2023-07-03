/*главное меню, отображается на каждой странице*/
CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

/*Пользователи, состоят из администраторов и сотрудников*/
CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
email text NOT NULL,
password text NOT NULL,
time integer NOT NULL,
rank text NOT NULL
);

/*Клиенты, воспользовавшиеся услугами аренды автомобилей*/
CREATE TABLE IF NOT EXISTS clients (
client_id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
surname text NOT NULL,
phone_number text NOT NULL,
employee_id text NOT NULL,
FOREIGN KEY (employee_id) REFERENCES users(id)
);

/*Штрафы клиентов*/
CREATE TABLE IF NOT EXISTS fines (
fines_id integer PRIMARY KEY AUTOINCREMENT,
client_id integer NOT NULL,
time integer NOT NULL,
reason text NOT NULL,
sum integer NOT NULL,
user_id integer NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

/*Машины имеющиеся в наличии*/
CREATE TABLE IF NOT EXISTS cars (
    car_id integer PRIMARY KEY AUTOINCREMENT,
    model text NOT NULL,
    car_number text NOT NULL,
    price integer NOT NULL
);

/*Бронирование машины*/
CREATE TABLE IF NOT EXISTS reservation (
    reservation_id integer PRIMARY KEY AUTOINCREMENT,
    client_id integer NOT NULL,
    car_id integer NOT NULL,
    time integer NOT NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
);

/*Запись о аренде авто*/
CREATE TABLE IF NOT EXISTS record (
    record_id integer PRIMARY KEY AUTOINCREMENT,
    client_id integer NOT NULL,
    car_id integer NOT NULL,
    time integer NOT NULL,
    user_id integer NOT NULL,
    sum integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
);