import base64

from Crypto.Cipher import AES
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
# from sqlalchemy import Enum

from app import db, app
from utils.common_utils import extend_to_16



class IndividualUser(db.Model):
    __tablename__ = "user_individual"
    Id = db.Column(db.Integer, primary_key=True)
    Nickname = db.Column(db.String(80), index=True, nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)

    Name = db.Column(db.String(20))
    Sex = db.Column(db.Enum('male', 'female'))
    Birth = db.Column(db.String(20))
    ResidenceAddress = db.Column(db.String(256))
    Education = db.Column(db.Enum('primary ','middle','high','bachelor','master','doctor'))
    School = db.Column(db.String(80))
    WorkAddress = db.Column(db.String(256))
    LiveAddress = db.Column(db.String(256))

    Marriage = db.Column(db.Enum('married','single'))
    Salary = db.Column(db.Integer)
    VehicleProperty = db.Column(db.Integer)
    HouseProperty = db.Column(db.Integer)
    VehicleLoan = db.Column(db.Integer)
    HouseLoan = db.Column(db.Integer)
    WorkYear = db.Column(db.Integer)

    Job = db.Column(db.Enum('student','whiteCollar','farmer','other'))

    IsAuthenticated = db.Column(db.Boolean)
    PhoneNumber = db.Column(db.String(11))
    IDCardNumber = db.Column(db.String(18))
    BankCardNumber = db.Column(db.String(19))


    ApplyPassTime = db.Column(db.Integer)
    PayTime = db.Column(db.Integer)
    OverdueTime = db.Column(db.Integer)
    SevereOverdueTime = db.Column(db.Integer)
    OverdueAmount = db.Column(db.Integer)
    OtherDebtAmount = db.Column(db.Integer)
    RepayCapitalAmount = db.Column(db.Integer)
    UnrepayCapitalAmount = db.Column(db.Integer)
    RepayIntersetAmount = db.Column(db.Integer)
    UnrepayInterestAmount = db.Column(db.Integer)
    CreditScore = db.Column(db.Integer)
    
    aes = AES.new(extend_to_16(app.config['SECRET_KEY']), AES.MODE_ECB)


    def __init__(self, nickname, password,
                    name, sex, birth, residence_address,
                    education, school, work_address, live_address,
                    marriage, salary, vehicle_property, house_property, vehicle_loan, house_loan, work_year,
                    job):
        self.Nickname = nickname
        self.hash_password(password)

        self.Name = name
        self.Sex = sex
        self.Birth = birth
        self.ResidenceAddress = residence_address

        self.School = school
        self.WorkAddress = work_address
        self.LiveAddress = live_address
        self.Marriage = marriage
        self.Salary = salary
        self.VehicleProperty = vehicle_property
        self.HouseProperty = house_property
        self.VehicleLoan = vehicle_loan
        self.HouseLoan = house_loan
        self.WorkYear = work_year

        self.Job = job

        # '-1' as 'not set'
        self.ApplyPassTime = -1
        self.PayTime = -1
        self.OverdueTime = -1
        self.SevereOverdueTime = -1
        self.OverdueAmount = -1
        self.OtherDebtAmount = -1
        self.RepayCapitalAmount = -1
        self.UnrepayCapitalAmount = -1
        self.RepayIntersetAmount = -1
        self.UnrepayInterestAmount = -1
        self.CreditScore = -1

        # Authentication info is not set when user is initialized,
        # fill these fields in Authentication process
        self.IsAuthenticated = False
        self.PhoneNumber = -1
        self.IDCardNumber = 'xxxxxxxxxxxxxxxxxx'
        self.BankCardNumber = 'xxxxxxxxxxxxxxxxxx'

    def to_dict(self):
        return {
            'name': self.Name,
            'sex':  self.Sex,
            'birth': self.Birth,
            'residence_address': self.ResidenceAddress,

            'school': self.School,
            'work_address': self.WorkAddress,
            'live_address': self.LiveAddress,
            'marriage': self.Marriage,
            'salary': self.Salary,
            'vehicle_property': self.VehicleProperty,
            'house_property': self.HouseProperty,
            'vehicle_loan': self.VehicleLoan,
            'house_loan': self.HouseLoan,
            'work_year': self.WorkYear,

            'job': self.Job,

            'apply_pass_time': self.ApplyPassTime,
            'pay_time': self.PayTime,
            'overdue_time': self.OverdueTime,
            'severe_overdue_time': self.SevereOverdueTime,
            'overdue_amount': self.OverdueAmount,
            'other_debt_amount': self.OtherDebtAmount,
            'repay_capital_amount': self.RepayCapitalAmount,
            'unrepay_capital_amount': self.UnrepayCapitalAmount,
            'repay_interset_amount': self.RepayIntersetAmount,
            'unrepay_interest_amount': self.UnrepayInterestAmount,
            'credit_score': self.CreditScore
        }

    def get_nickname(self):
        return self.Nickname

    def get_password_hash(self):
        return self.PasswordHash

    def hash_password(self, password):
        encrypt_aes = self.aes.encrypt(extend_to_16(password))
        self.PasswordHash = str(base64.encodebytes(encrypt_aes), encoding='utf-8').rstrip('\n')

    def get_decoded_password(self):
        encoded_str = base64.decodestring(self.PasswordHash.encode(encoding='utf-8'))
        decoded_password = self.aes.decrypt(encoded_str).decode().rstrip('\0')
        return decoded_password

    def verify_password(self, password):
        encrypt_aes = self.aes.encrypt(extend_to_16(password))
        password_hash = str(base64.encodebytes(encrypt_aes), encoding='utf-8').rstrip('\n')
        return password_hash == self.PasswordHash

    def gen_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=app.config['EXPIRES_IN'])
        return str(s.dumps({'UserId': self.Id}), encoding='utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        origin_token = bytes(token, encoding='utf-8')
        try:
            data = s.loads(origin_token)
        except SignatureExpired:
            return None # valid token, but expire
        except BadSignature:
            return None # invalid token
        user = IndividualUser.query.get(data['UserId'])
        return user

