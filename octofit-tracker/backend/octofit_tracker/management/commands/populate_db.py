from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            {'_id': ObjectId(), 'email': 'thundergod@mhigh.edu', 'name': 'Thor Odinson', 'password': 'thundergodpassword'},
            {'_id': ObjectId(), 'email': 'metalgeek@mhigh.edu', 'name': 'Tony Stark', 'password': 'metalgeekpassword'},
            {'_id': ObjectId(), 'email': 'zerocool@mhigh.edu', 'name': 'Dade Murphy', 'password': 'zerocoolpassword'},
            {'_id': ObjectId(), 'email': 'crashoverride@mhigh.edu', 'name': 'Kate Libby', 'password': 'crashoverridepassword'},
        ]
        db.users.insert_many(users)

        # Create teams
        teams = [
            {'_id': ObjectId(), 'name': 'Avengers', 'members': [users[0]['_id'], users[1]['_id']]},
            {'_id': ObjectId(), 'name': 'Hackers', 'members': [users[2]['_id'], users[3]['_id']]},
        ]
        db.teams.insert_many(teams)

        # Create activities
        activities = [
            {'_id': ObjectId(), 'user': users[0]['_id'], 'activity_type': 'Running', 'duration': 30, 'date': datetime(2025, 5, 25)},
            {'_id': ObjectId(), 'user': users[1]['_id'], 'activity_type': 'Cycling', 'duration': 45, 'date': datetime(2025, 5, 26)},
            {'_id': ObjectId(), 'user': users[2]['_id'], 'activity_type': 'Swimming', 'duration': 60, 'date': datetime(2025, 5, 24)},
            {'_id': ObjectId(), 'user': users[3]['_id'], 'activity_type': 'Yoga', 'duration': 40, 'date': datetime(2025, 5, 23)},
        ]
        db.activity.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {'_id': ObjectId(), 'team': teams[0]['_id'], 'points': 150},
            {'_id': ObjectId(), 'team': teams[1]['_id'], 'points': 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {'_id': ObjectId(), 'name': 'Pushups', 'description': 'Do 20 pushups', 'difficulty': 'Easy'},
            {'_id': ObjectId(), 'name': '5K Run', 'description': 'Run 5 kilometers', 'difficulty': 'Medium'},
            {'_id': ObjectId(), 'name': 'Plank', 'description': 'Hold a plank for 2 minutes', 'difficulty': 'Hard'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
