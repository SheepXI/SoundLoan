from app import db, app


class LoanProduct(db.Model):
    __tablename__ = "loan_product"

    Id = db.Column(db.Integer, primary_key=True)

    Name = db.Column(db.String(80))
    EnterpriseName = db.Column(db.String(80))
    AmountMin = db.Column(db.Integer)
    AmountMax = db.Column(db.Integer)
    RateMin = db.Column(db.Float)
    RateMax = db.Column(db.Float)
    DurationMin = db.Column(db.Integer)
    DurationMax = db.Column(db.Integer)


    def to_dict(self):
        return {
            'id': self.Id,
            'name': self.Name,
            'enterprise_name': self.EnterpriseName,
            'amount_min': self.AmountMin,
            'amount_max': self.AmountMax,
            'rate_min': self.RateMin,
            'rate_max': self.RateMax,
            'duratioin_min': self.DurationMin,
            'duratioin_max': self.DurationMax
        }