from app import create_app, db
from app.models import (UserLogin, QualificationDate, Address,
                        Patient, Provider, Appointment, 
                        TimeBlockOptions, AppointmentMatch)


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
            'AppointmentMatch': AppointmentMatch}
