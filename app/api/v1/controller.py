import sqlite3
from datetime import datetime, timedelta


class Schedule():
    def __init__(self):
        self.conn = sqlite3.connect('calendar.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date Date NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            room_id INTEGER,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (meeting_id) REFERENCES meetings(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        self.conn.commit()

    
    def add_user(self, name):
        self.cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.conn.commit()
        return self.cursor.lastrowid


    def add_room(self, room_name):
        self.cursor.execute('INSERT INTO rooms (name) VALUES (?)', (room_name,))
        self.conn.commit()
        return self.cursor.lastrowid


    def add_meeting(self, title, start_time, end_time, room_id, participant_ids):
        self.cursor.execute('''
            INSERT INTO meetings (date, start_time, end_time, room_id)
            VALUES (?, ?, ?, ?)
        ''', (title, start_time, end_time, room_id))
        meeting_id = self.cursor.lastrowid

        for user_id in participant_ids:
            self.cursor.execute('''
                INSERT INTO participants (meeting_id, user_id)
                VALUES (?, ?)
            ''', (meeting_id, user_id))

        self.conn.commit()

    def check_room_collision(self, room_id, start_time, end_time):
        self.cursor.execute('''
            SELECT * FROM meetings
            WHERE room_id = ? AND NOT (? <= start_time OR ? >= end_time)
        ''', (room_id, end_time, start_time))
        if self.cursor.fetchone():
            return True
        return False


    def check_collision(self, start_time, end_time, participant_ids, room_id):
        for user_id in participant_ids:
            self.cursor.execute('''
                SELECT * FROM meetings
                JOIN participants ON meetings.id = participants.meeting_id
                WHERE participants.user_id = ? AND NOT (? <= meetings.start_time OR ? >= meetings.end_time)
            ''', (user_id, end_time, start_time))
            if self.cursor.fetchone():
                return True
        if room_id:
            return self.check_room_collision(room_id, start_time, end_time)
        return False


    def get_room_id(self, room_name):
        if not room_name:
            return None
        self.cursor.execute('SELECT id FROM rooms WHERE name = ?',(room_name,))
        room_id = self.cursor.fetchone()
        if not room_id:
            room_id = self.add_room(room_name)
        else:
            room_id=room_id[0]
        return room_id


    def get_participant_ids(self, participant_names):
        participant_ids = []
        for name in participant_names:
            self.cursor.execute('SELECT id FROM users WHERE name = ?', (name,))
            participant_id = self.cursor.fetchone()
            if not participant_id:
                participant_id = self.add_user(name)
            else:
                participant_id = participant_id[0]
            participant_ids.append(participant_id)
        return participant_ids

    def is_valid_date_format(self, date_string, date_format):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def schedule_meeting(self, date, time, period, participant_names, room_name=None):
        if not self.is_valid_date_format(date, '%Y-%m-%d'):
            return "Date is not in correct format. Correct format: yyyy-mm-dd"
        
        if not self.is_valid_date_format(time, '%H:%M:%S'):
            return "Time is not in correct format. Correct format: HH:MM:SS"
        
        room_id = self.get_room_id(room_name)

        start_time = date + ' ' + time
        end_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=period)

        if self.check_collision(start_time, end_time, participant_names, room_id):
            return "Collision detected! Cannot schedule the meeting."

        self.add_meeting(date, start_time, end_time, room_id, participant_names)
        return "Meeting scheduled successfully."
