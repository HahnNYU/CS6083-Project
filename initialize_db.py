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


def insert_priority_groups():
    groups = [
            QualificationDate(
                priority_group=1,
                qualify_date=datetime.date(2021, 1, 1)
                ),
            QualificationDate(
                priority_group=2,
                qualify_date=datetime.date(2021, 2, 1)
                ),
            QualificationDate(
                priority_group=3,
                qualify_date=datetime.date(2021, 3, 1)
                ),
            QualificationDate(
                priority_group=4,
                qualify_date=datetime.date(2021, 4, 1)
                ),
            ]
    # create app context and insert data
    with app.app_context():
        for g in groups:
           db.session.add(g)
        db.session.commit()


def insert_patients():
    # create UserLogin and Address entry for each patient
    # also create time_preference for each patient
    pass


def insert_providers():
    # create UserLogin and Address entry for each provider
    pass


def insert_appointments():
    pass


def insert_appointment_matches():
    pass


if __name__ == '__main__':
    #insert_time_block_options()
    #insert_priority_groups()
    #insert_pateints()
    #insert_providers()
    #insert_appointments()
    #insert_appointment_matches()
