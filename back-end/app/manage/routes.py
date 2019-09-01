from flask import jsonify, request
from sqlalchemy import func

from flask import Response, jsonify
from app import app, db
from models.IndividualUser import IndividualUser
from models.EnterpriseUser import EnterpriseUser
from models.LoanProduct import LoanProduct
from models.LoanRecord import LoanRecord
from models.Contract import Contract
from models.LoanProductComment import LoanProductComment


@app.route("/infoMan/indUserInfo", methods=["GET"])
def query_individual_user():
    user_id = request.args.get('id', None)
    user_nickname = request.args.get('nickname', None)
    if user_id is None and user_nickname is None:
        return jsonify({'success': False, 'message': 'Missing param id and nickname.'})

    if user_id is not None:
        user = IndividualUser.query.filter(IndividualUser.Id == user_id).first()
    else:
        user = IndividualUser.query.filter(IndividualUser.Nickname == user_nickname).first()
    if user is None:
        return jsonify({'success': False, 'message': 'Failed to find a qualified user.'})
    
    return jsonify({'success': True, 'content': user.to_dict()})


@app.route("/infoMan/createIndUser", methods=["POST"])
def create_individual_user():
    try:
        params = request.form.to_dict()

        new_user = IndividualUser(**params)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'content': {
                'id': new_user.Id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route("/infoMan/indLogin", methods=["POST"])
def login_individual_user():
    nickname = request.form.get('nickname', None)
    password = request.form.get('password', None)
    if not nickname or not password:
        return jsonify({'success': False, 'message': 'Missing params nickname or password！'})
    user = IndividualUser.query.filter(IndividualUser.Nickname == nickname).first()
    if not user:
        return jsonify({'success': False, 'message': 'User does not exist！'})
    if user.verify_password(password):
        return jsonify({'success': True, 'token': user.gen_auth_token()})
    else:
        return jsonify({'success': False, 'message': 'Wrong password！'})


@app.route("/infoMan/entUserInfo", methods=["GET"])
def query_enterprise_user():
    user_id = request.args.get('id', None)
    user_name = request.args.get('name', None)
    if user_id is None and user_name is None:
        return jsonify({'success': False, 'message': 'Missing param id and name.'})

    if user_id is not None:
        user = EnterpriseUser.query.filter(EnterpriseUser.Id == user_id).first()
    else:
        user = EnterpriseUser.query.filter(EnterpriseUser.Name == user_name).first()
    if user is None:
        return jsonify({'success': False, 'message': 'Failed to find a qualified user.'})
    
    return jsonify({'success': True, 'content': user.to_dict()})


@app.route("/infoMan/createEntUser", methods=["POST"])
def create_enterprise_user():
    try:
        params = request.form.to_dict()

        new_user = EnterpriseUser(**params)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'content': {
                'id': new_user.Id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route("/infoMan/entLogin", methods=["POST"])
def login_enterprise_user():
    name = request.form.get('name', None)
    password = request.form.get('password', None)
    if not name or not password:
        return jsonify({'success': False, 'message': 'Missing params name or password！'})
    user = EnterpriseUser.query.filter(EnterpriseUser.Name == name).first()
    if not user:
        return jsonify({'success': False, 'message': 'User does not exist！'})
    if user.verify_password(password):
        return jsonify({'success': True, 'token': user.gen_auth_token()})
    else:
        return jsonify({'success': False, 'message': 'Wrong password！'})


@app.route("/infoMan/allLoanProductComment", methods=["GET"])
def all_loan_product_comment():
    comments = LoanProductComment.query.all()
    result = [c.to_dict() for c in comments]
    return jsonify({'success': True, 'content': result})


@app.route("/infoMan/entProductComment", methods=["GET"])
def ent_product_comment():
    name = request.args.get('company_name', None)
    if not name:
        return jsonify({'success': False, 'message': 'Missing params company_name'})
    sub = LoanProduct.query.filter(LoanProduct.EnterpriseName == name).subquery()
    commentList = db.session.query(sub, LoanProductComment).join(LoanProductComment, LoanProductComment.ProductId == sub.c.Id).all()
    result = [{
        'product_name': c.Name,
        'user_id': c.LoanProductComment.UserId,
        'comment': c.LoanProductComment.Comment,
        'score': c.LoanProductComment.Score,
    } for c in commentList]

    return jsonify({'success': True, 'content': result})


@app.route("/infoMan/entScore", methods=["GET"])
def ent_score():
    # entScore is the mean value of all the product scores from this enterprise
    name = request.args.get('company_name', None)
    if not name:
        return jsonify({'success': False, 'message': 'Missing params company_name'})
    sub = LoanProduct.query.filter(LoanProduct.EnterpriseName == name).subquery()
    commentList = db.session.query(sub, LoanProductComment).join(LoanProductComment, LoanProductComment.ProductId == sub.c.Id).subquery()
    score = db.session.query(func.avg(commentList.c.Score).label("mean_score")).first()
    result = {'score': float(str(score.mean_score))}
    return jsonify({'success': True, 'content': result})