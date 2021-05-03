from app import create_app, db
from app.models import (UserLogin, QualificationDate, Address,
                        Patient, Provider, Appointment, 
                        TimeBlockOptions, AppointmentMatch)
import datetime


app = create_app()


def insert_time_block_options():
    options = [
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=0),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=0),
            TimeBlockOptions(
                time_block_start=datetime.time(16, 0, 1),
                time_block_end=datetime.time(20, 0, 0),
                day_of_week=0),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=1),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=1),
            TimeBlockOptions(
                time_block_start=datetime.time(16, 0, 1),
                time_block_end=datetime.time(20, 0, 0),
                day_of_week=1),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=2),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=2),
            TimeBlockOptions(
                time_block_start=datetime.time(16, 0, 1),
                time_block_end=datetime.time(20, 0, 0),
                day_of_week=2),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=3),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=3),
            TimeBlockOptions(
                time_block_start=datetime.time(16, 0, 1),
                time_block_end=datetime.time(20, 0, 0),
                day_of_week=3),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=4),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=4),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=5),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=5),
            TimeBlockOptions(
                time_block_start=datetime.time(8, 0, 0),
                time_block_end=datetime.time(12, 0, 0),
                day_of_week=6),
            TimeBlockOptions(
                time_block_start=datetime.time(12, 0, 1),
                time_block_end=datetime.time(16, 0, 0),
                day_of_week=6)
            ]
    # create app context and insert data
    with app.app_context():
        for o in options:
           db.session.add(o)
        db.session.commit()


if __name__ == '__main__':
    insert_time_block_options()
