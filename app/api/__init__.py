from flask_restx import Api

from app.api.v1.view import api as schedule_api



api = Api(version='1.0',
          title='Meeting Scheduler API service',
          doc='/api',
          description='Document for Elasticsearch API')


api.add_namespace(schedule_api, path='/api/v1/')

