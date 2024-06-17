from flask import abort, request
from flask_restx import Namespace, Resource
from app.api.v1.controller import Schedule


api = Namespace("Meeting Scheduler", description="Meeting Scheduler API")

@api.route("/schedule")
class ScheduleMeeting(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description="Schedule Meeting API")
    def post(self):
        request_json = request.json
        if 'date' not in request_json:
            return ({"message": "date is not provived"}, 500)
        if 'time' not in request_json:
            return ({"message": "time is not provived"}, 500)
        if 'period' not in request_json:
            return ({"message": "period is not provived"}, 500)
        if 'participant_names' not in request_json:
            return ({"message": "participant_names is not provived"}, 500)
        
        try:
            meeting_Scheduler = Schedule()
            message = meeting_Scheduler.schedule_meeting(request_json['date'], request_json['time'],
                                       request_json['period'], request_json['participant_names'], request_json.get('room_name'))
            return ({"message": message}, 200)
        except Exception as e:
            print(e)
            abort(400, e)

