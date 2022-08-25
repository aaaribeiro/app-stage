from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
# from sqlalchemy_utils import EmailType, PasswordType
from database.database import Base


class Tickets(Base):
    
    __tablename__ = 'mov_tickets'
    id = Column(Integer, primary_key=True)
    org_id = Column(String, ForeignKey('mov_organizations.id'))
    agent_id = Column(String, ForeignKey('mov_agents.id'))
    created_date = Column(DateTime)
    status = Column(String)
    category = Column(String)
    urgency = Column(String)
    subject =  Column(String)    
    sla_solution_date = Column(DateTime)
    sla_first_response = Column(DateTime)
    # relationships
    time_appointments = relationship('TimeAppointments', back_populates='ticket')
    organization =  relationship('Organizations', back_populates='tickets')
    agent = relationship('Agents', back_populates='tickets')


class Organizations(Base):

    __tablename__ = 'mov_organizations'
    id = Column(String, primary_key=True)
    # cc = Column(String)
    name = Column(String, nullable=False)
    # relationships
    tickets = relationship('Tickets', back_populates='organization')


class Agents(Base):

    __tablename__ = 'mov_agents'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    team = Column(String)
    # relationships
    tickets = relationship('Tickets', back_populates='agent')
    time_appointments = relationship('TimeAppointments', back_populates='agent')


class TimeAppointments(Base):

    __tablename__ = 'mov_time_appointments'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('mov_tickets.id'), nullable=False)
    agent_id = Column(String, ForeignKey('mov_agents.id'), nullable=False)
    created_date = Column(DateTime)
    time_appointment = Column(Time)
    # relationships
    agent = relationship('Agents', back_populates='time_appointments')
    ticket = relationship('Tickets', back_populates='time_appointments')


# class WebhookLogs(Base):

#     __tablename__ = 'webhook_log'
#     hook_id = Column(Integer, primary_key=True, autoincrement=True)
#     ticket_id = Column(Integer, nullable=False)
#     change = Column(String, nullable=False)
#     trigger_date = Column(DateTime, nullable=False)
#     was_read = Column(Boolean, nullable=False, default=False)


# class Users(Base):

#     __tablename__ = 'auth_users'
#     # TYPES = [u'admin', u'edit', u'read']
#     user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     name = Column(String, nullable=False)
#     email = Column(EmailType, nullable=False, unique=True)
#     isadmin = Column(Boolean, nullable=False, default=False)
#     password = Column(PasswordType(schemes=['pbkdf2_sha512']))
#     # relationships
#     token = relationship('AccessToken', backref=backref('auth_access_token', uselist=False))


# class AccessToken(Base):

#     __tablename__ = 'auth_access_token'
#     token_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('auth_users.user_id'), nullable=False)
#     access_token = Column(String, nullable=False)
