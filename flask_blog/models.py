from datetime import datetime
from jwt import encode, decode
from datetime import datetime, timezone, timedelta
from flask import current_app
from flask_blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        payload = {'user_id': self.id,
                   'exp': datetime.now(timezone.utc) + timedelta(
                       seconds=expires_sec)}

        return encode(payload, current_app.config['SECRET_KEY'],
                      algorithm="HS256")

    @staticmethod
    def verify_reset_token(token):
        try:
            data = decode(token, current_app.config['SECRET_KEY'],
                          leeway=leeway, algorithms=['HS256'])
        except Exception:
            return None

        return User.query.get(data['user_id'])


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='select', cascade='all, delete-orphan')
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)


class Like(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'post_id',
                                              name='CompositePkForLike'),)

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'),
                        nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'),
                        nullable=False)
