## Problem Statement

We need to build a Calendar system, which supports following functionalities:

### Prelim: (Single person)
- Schedule a meeting with input of Day and time and period(or to and from time)
- Should be able to detect any collisions if scheduling a new meeting.

### Advance: (Multiple person, room accommodation)
- include meeting rooms as parameter
- detect if there is collision when scheduling
include other persons in meeting as parameter
   - detect if other person is available



## Steps to perform
API is not yet deployed anywhere. It can be tested on local computer

### Perform below steps on cmd
```
git clone <repository_url>
cd meeting_scheduler
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

### API

- API End point: /api/v1/schedule
- API Type: POST
- Headers: 
`{
Authorization:  Basic dGVzdDpwYXNzd29yZA==,
Content-Type: application/json
}`
- Payload:
  - date(string): Date when meeting should be scheduled.  (Format: yyyy-mm-dd)
  - time(string): Time when meeting should be started. (Format - HH:MM:SS)
  - period(integer): Time period in minutes for which meeting should be scheduled
  - participant_names(list of strings): List of name of the paricipant of the meeting
  - room_name(string)(optional): Name of the room where meeting should be scheduled




## Example:
```
curl --location --request POST 'http://127.0.0.1:5000/api/v1/schedule' \
--header 'Authorization:  Basic dGVzdDpwYXNzd29yZA==' \
--header 'Content-Type: application/json' \
--data-raw '{
    "date": "2024-05-13",
    "time": "10:40:00",
    "period": 20,
    "participant_names":  ["John", "Joe"],
    "room_name": "2"
}'
```
