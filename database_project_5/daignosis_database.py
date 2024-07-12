from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///patientdata.db')

class Patient_data(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(100), nullable=True)
    weight = Column(Integer, nullable=True)
    allergy = Column(String(100), nullable=True)

    @property
    def visualize(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'weight': self.weight,
            'allergy': self.allergy
        }

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# new_patient = Patient_data(name="John Doe", age=30, gender="Male", weight=70, allergy="None")
# session.add(new_patient)
# session.commit()
