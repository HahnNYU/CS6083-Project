from app import create_app, db
from app.models import (UserLogin, QualificationDate, Address,
                        Patient, Provider, Appointment, 
                        TimeBlockOptions, AppointmentMatch)
from app.main.utils import appointment_matcher, unmatch_expired_offers


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'UserLogin': UserLogin, 
            'QualificationDate': QualificationDate, 
            'Address': Address,
            'Patient': Patient, 
            'Provider': Provider, 
            'Appointment': Appointment, 
            'TimeBlockOptions': TimeBlockOptions,
            'AppointmentMatch': AppointmentMatch
           }


@app.cli.command()
def offer_appointments():
    """Run appointment matcher"""
    # crontab to run at every 5 minutes:
    # */5 * * * * cd <project directory> && venv/bin/flask offer-appointments > /dev/null 2>&1
    appointment_matcher()


@app.cli.command()
def remove_expired():
    """Unmatch pending appointments that are expired"""
    # crontab to run once every day:
    # 0 20 * * * cd <project directory> && venv/bin/flask remove-expired > /dev/null 2>&1
    unmatch_expired_offers()
