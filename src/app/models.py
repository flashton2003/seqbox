"""
SQLAlchemy : Using ORM(Oject Relational Mapper)
"""
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import backref # relationship
#from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """This is a Class for User inherits from db.Model,a base class for all models from Flask-SQLAlchemy.
    
    Arguments:
        UserMixin {class} --[ This provides default implementations for the methods that Flask-Login expects user objects to have.]
        db {object} -- [Object that represents the database.]
    
    """
    # These class variables define the column properties
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # establishes a relationship between User and Post
    # backref adds a new property to the Post class, Post.author will point to a User
    # lazy defines when sqlalchemy will load data from the database
    # dynamic returns a query object which you can apply further selects to
    # dynamic is an unusual choice according to here
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """[The __repr__ method tells Python how to print objects of this class.]
        
        Returns:
            [string] -- [return User model representation. ]
        """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """[The set_password method to hash ad store a password in the User model.]
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """[The check_password method to verify the password.  ]
        
        Returns:
            [str] -- [Returns True if the password matched, False otherwise.]
        """
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """[The @login.user_loader decorated function is used by Flask-Login to convert a stored user ID to an actual user instance.
    The user loader callack function receives a user identifier as a Unicode string the return value of the function 
    must be the user object if available or None otherwise. ]  
    
    """
    return User.query.get(int(id))


class Post(db.Model):
    """[summary]
    
    Arguments:
        db {[type]} -- [description]ll
    
    Returns:
        [type] -- [description]
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user.id here refers to user table, id column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return '<Post {}>'.format(self.body)

class IlluminaReadSet(db.Model):

    """[Define model 'Sample' mapped to table 'sample']
    
    Arguments:
        db {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    # are they using the actual read set id as the primary key?
    id_illumina_read_set = db.Column(db.Integer, primary_key=True)

    num_reads = db.Column(db.VARCHAR(60), comment="the number of sequencing reads")
    added_at = db.Column(db.DATETIME)
    # organism = db.Column(db.VARCHAR(30))
    batch = db.Column(db.VARCHAR(50), db.ForeignKey("batch.id_batch",onupdate="cascade",ondelete="set null"),nullable=True)
    batches = db.relationship("Batch", backref=backref("illumina_read_set",passive_updates=True,passive_deletes=True))

    path_r1 = db.Column(db.VARCHAR(60))
    path_r2 = db.Column(db.VARCHAR(60))
    result1 = db.Column(db.Integer, db.ForeignKey("result1.id_result1",onupdate="cascade",ondelete="set null"),nullable=True) 
    results1 = db.relationship("Result1", backref=backref("illumina_read_set",passive_updates=True,passive_deletes=True))
    mykrobe = db.Column(db.Integer, db.ForeignKey("mykrobe.id_mykrobe",onupdate="cascade",ondelete="set null"),nullable=True)
    mykrobes = db.relationship("Mykrobe", backref=backref("illumina_read_set",passive_updates=True,passive_deletes=True))

    def __repr__(self):
        return "<Sample(id_sample='%s', num_reads='%s', organism='%s', batch='%s', date_time='%s', location='%s', path_r1='%s', path_r2='%s', result1='%s', mykrobe='%s')>" % (self.id_sample, self.num_reads, self.organism, self.batch, self.added_at, self.location, self.path_r1, self.path_r2, self.result1, self.mykrobe)


class Isolate(db.Model):
    id_isolate = db.Column(db.Integer, primary_key=True)
    isolate_identifier = db.Column(db.VARCHAR(30))
    species = db.Column(db.VARCHAR(120))
    sample_type = db.Column(db.VARCHAR(60))
    patient_identifier = db.Column(db.VARCHAR(30))
    date_collected = db.Column(db.DATETIME)
    date_added = db.Column(db.DATETIME)
    location = db.Column(db.VARCHAR(50), db.ForeignKey("location.id_location", onupdate="cascade", ondelete="set null"),
                         nullable=True)
    locations = db.relationship("Location", backref=backref("sample", passive_updates=True, passive_deletes=True))

    def __repr__(self):
        return f"Sample({self.isolate_identifier}, {self.species})"

class Batch(db.Model):
    """[Define model 'Batch' mapped to table 'batch']
    
    Arguments:
        db {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    id_batch = db.Column(db.VARCHAR(30),primary_key=True)
    name_batch = db.Column(db.VARCHAR(50))
    date_batch = db.Column(db.DATE)
    instrument = db.Column(db.VARCHAR(250))
    primer = db.Column(db.VARCHAR(100))
    
    def __repr__(self):
        return '<Batch {}>'.format(self.name_batch)

class Location(db.Model):
    """[Define model 'Location' mapped to table 'location']
    
    Arguments:
        db {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    id_location = db.Column(db.VARCHAR(25),primary_key=True)
    continent = db.Column(db.VARCHAR(80))
    country  = db.Column(db.VARCHAR(60))
    province = db.Column(db.VARCHAR(40))
    city = db.Column(db.VARCHAR(50))
   

    def __repr__(self):
        return '<Location {}>'.format(self.continent)

class Result1(db.Model):
    """[Define model 'Result1' mapped to table 'result1']
    
    Arguments:
        db {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    id_result1 = db.Column(db.Integer,primary_key=True)
    qc = db.Column(db.VARCHAR(60))
    ql = db.Column(db.VARCHAR(60))
    description = db.Column(db.VARCHAR(250))
    snapper_variants = db.Column(db.Integer)
    snapper_ignored = db.Column(db.Integer)
    num_heterozygous = db.Column(db.Integer)
    mean_depth = db.Column(db.CHAR)
    coverage = db.Column(db.CHAR)
   
    def __repr__(self):
        return '<Result1 {}>'.format(self.qc)

class Mykrobe(db.Model):

    """[Define model 'Mykrobe' mapped to table 'mykrobe']
    
    Returns:
        [type] -- [description]
    """
    
    id_mykrobe = db.Column(db.Integer, primary_key=True)
    mykrobe_version = db.Column(db.VARCHAR(50))
    phylo_grp = db.Column(db.VARCHAR(60))
    phylo_grp_covg = db.Column(db.CHAR)
    phylo_grp_depth = db.Column(db.CHAR)
    species = db.Column(db.VARCHAR(50))
    species_covg = db.Column(db.CHAR)
    species_depth = db.Column(db.CHAR)
    lineage = db.Column(db.VARCHAR(50))
    lineage_covg = db.Column(db.CHAR)
    lineage_depth = db.Column(db.CHAR)
    susceptibility = db.Column(db.VARCHAR(50))
    variants = db.Column(db.VARCHAR(80))
    genes = db.Column(db.VARCHAR(100))
    drug = db.Column(db.VARCHAR(90))
  
    def __repr__(self):
        return '<Mykrobe {}>'.format(self.mykrobe_version)
    
class Study(db.Model):

    """[Define model 'Study' mapped to table 'study']
    
    Returns:
        [type] -- [description]
    """
    id_study = db.Column(db.VARCHAR(50),primary_key=True)
    date_study = db.Column(db.DATE)
    result_study = db.Column(db.VARCHAR(80))
    
    def __repr__(self):
        return '<Study {}>'.format(self.result_study)

class Sample_study(db.Model):

    """[Define model 'Sample_study' mapped to table 'sample_study']
    
    Returns:
        [type] -- [description]
    """
    id_sample = db.Column(db.VARCHAR(40),primary_key = True)
    id_study = db.Column(db.VARCHAR(50),primary_key = True)
    
    def __repr__(self):
        return '<Sample_study {}>'.format(self.id_sample)

