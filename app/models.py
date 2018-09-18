# -*- coding: utf-8 -*-
__author__ = '51439'

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import *

# 用户常用球场
user_ground = db.Table('user_ground',
                       db.Column('user_id', db.Integer, db.ForeignKey('userinfo.id'),
                                 primary_key=True),
                       db.Column('ground_id', db.Integer, db.ForeignKey('groundinfo.id'),
                                 primary_key=True),
                       )


# 用户约球关系
class UserPlay(db.Model):
    __tablename__ = 'userplay'

    UserId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), primary_key=True)
    PlayId = db.Column(db.Integer, db.ForeignKey('playinfo.id'), primary_key=True)
    UserSay = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# 用户约球评分历史记录表
class UserScoreHistory(db.Model):
    __tablename__ = 'userscorehistory'
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer)
    PlayId = db.Column(db.Integer)
    ScoreName = db.Column(db.String(20), nullable=False)
    ScoreValue = db.Column(db.String(10), nullable=False)
    ScoreTime = db.Column(db.DateTime, nullable=False)
    ScoreMan = db.Column(db.Integer)

    def __repr__(self):
        return '<UserScore %s>' % UserScore.UserId


# 留言板表
class MsgBoard(db.Model):
    __tablename__ = 'msgboard'

    id = db.Column(db.Integer, primary_key=True)
    MasterId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), nullable=False)
    MsgManId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), nullable=False)
    MsgContent = db.Column(db.String(500), nullable=False)
    MsgTime = db.Column(db.DateTime, nullable=False)


# 关注
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('userinfo.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('userinfo.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# 用户信息表
class UserInfo(UserMixin, db.Model):
    __tablename__ = 'userinfo'

    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(50), unique=True, index=True)
    RoleType = db.Column(db.String(10), default="1")
    UserName = db.Column(db.String(10), unique=True, index=True)
    PhoneNum = db.Column(db.String(13))
    ShowPhoneNum = db.Column(db.String(1), default='0')
    PlayFre = db.Column(db.String(10))
    OftenTime = db.Column(db.String(10))
    OftenWhere = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    Location = db.Column(db.String(64))
    #LocalPoint = db.Column(db.String(64))
    MemberDate = db.Column(db.DateTime, default=datetime.utcnow)
    Lastseen = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    # 评分
    scores = db.relationship('UserScore', backref='scoreduser')
    # 历史评分
    # scorehistories = db.relationship('UserScoreHistory', backref='scoreduser', lazy='dynamic')
    # 视频
    videos = db.relationship('UserVideo', backref='videouser')
    # 约球
    plays = db.relationship('UserPlay', backref='users', lazy='dynamic')
    # 常用球场
    grounds = db.relationship('GroundInfo', secondary=user_ground, backref='groundusers')
    # 身体素质
    body = db.relationship('UserBody', uselist=False, back_populates='userinfo')
    # 我关注的人
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'), lazy='dynamic',
                               cascade='all, delete-orphan')
    # 关注我的人
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'), lazy='dynamic',
                                cascade='all, delete-orphan')

    # 关注
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    # 取消关注
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    # 我是否关注？
    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    # 我是否被关注
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    # 给我的留言
    msgstome = db.relationship('MsgBoard',
                               foreign_keys=[MsgBoard.MasterId],
                               backref=db.backref('masteruser', lazy='joined'),
                               lazy='dynamic', cascade='all,delete-orphan')
    # 我留的言
    msgsfromme = db.relationship('MsgBoard',
                                 foreign_keys=[MsgBoard.MsgManId],
                                 backref=db.backref('msgmanuser', lazy='joined'),
                                 lazy='dynamic', cascade='all,delete-orphan')

    # 我是否留过言
    def is_msgfromme(self, user):
        return self.msgsfromme.filter_by(MasterId=user.id).first() is not None

    # 是否给我留过言
    def is_msgtome(self, user):
        return self.msgstome.filter_by(MsgManId=user.id).first() is not None

    # 加入队伍
    def joinplay(self, play):
        up = UserPlay(users=self, plays=play)
        db.session.add(up)

    # 退出队伍
    def quitplay(self, play):
        p = self.plays.filter_by(PlayId=play.id).first()
        if p:
            db.session.delete(p)

    def __repr__(self):
        return '<User_Login %s>' % self.UserName

    # 属性不可读
    @property
    def password(self):
        return AttributeError('密码不可读！')

    # 密码加密
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成确认令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # 生成修改密码令牌
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    # 重置密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = UserInfo.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # 邮件确认
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 生成API令牌
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 验证令牌,令牌可用返回用户
    # 因为只有解码令牌后才知道用户是谁，所以使用静态方法
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return UserInfo.query.get(data['id'])

    # 记录用户每次访问时间
    def ping(self):
        self.Lastseen = datetime.utcnow()
        db.session.add(self)


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


# 用户约球评分表(历史评分计算结果)
class UserScore(db.Model):
    __tablename__ = 'userscore'
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('userinfo.id'))
    ComputeTime = db.Column(db.DateTime, nullable=False)
    ScoreName = db.Column(db.String(20), nullable=False)
    ScoreValue = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<UserScore %s>' % UserScore.UserId


# 用户视频表
class UserVideo(db.Model):
    __tablename__ = 'uservideo'

    VideoId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), nullable=False)
    VideoUrl = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<UserVideo %s>' % UserVideo.VideoId


# 用户身体素质表
class UserBody(db.Model):
    __tablename__ = 'userbody'

    UserId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), primary_key=True)
    Sex = db.Column(db.String(2), default='保密')
    Age = db.Column(db.String(3), default='保密')
    Position = db.Column(db.String(1), )
    BallAge = db.Column(db.Integer, default=0)
    Height = db.Column(db.Integer)
    Weight = db.Column(db.Integer)
    BodyFat = db.Column(db.Integer)
    ArmSpan = db.Column(db.INTEGER)
    TimeFor100m = db.Column(db.TIME)
    ReachJump = db.Column(db.FLOAT)

    userinfo = db.relationship('UserInfo', back_populates='body')

    def __repr__(self):
        return '<UserBody %s>' % UserBody.UserId


# 约球信息表
class PlayInfo(db.Model):
    __tablename__ = 'playinfo'

    id = db.Column(db.Integer, primary_key=True)
    GroundId = db.Column(db.String(50), nullable=False)
    PlayType = db.Column(db.String(1), nullable=False)
    PlayStatus = db.Column(db.String(1), default='0')
    LeaderMan = db.Column(db.Integer, nullable=False)
    PlayTime = db.Column(db.DateTime, nullable=False)
    PlayTitle = db.Column(db.String(50), default='一起来打球吧！')
    PlayInfo = db.Column(db.String(50), nullable=False)
    NeedManCount = db.Column(db.Integer, nullable=False)
    Money = db.Column(db.Float, default=0)
    WantMan = db.Column(db.String(50))
    Time = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('UserPlay', backref='plays', lazy='dynamic')

    def isjoined(self, user):
        return self.users.filter_by(UserId=user.id).first() is not None

    # UserScoreHistories = db.relationship('histories',backref = 'userplays')
    def __repr__(self):
        return '<PlayInfo %s>' % PlayInfo.PlayId


# 约球申请记录表
class PlayApllyRecord(db.Model):
    __tablename__ = 'playapplyrecord'

    id = db.Column(db.Integer, primary_key=True)
    ApplyManId = db.Column(db.Integer, db.ForeignKey('userinfo.id'), nullable=False)
    PlayId = db.Column(db.Integer, db.ForeignKey('playinfo.id'), nullable=False)
    ApllyTime = db.Column(db.DateTime, nullable=False)
    ApllyResult = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return '<PlayApllyRecord %s>' % PlayApllyRecord.ApplyManId


# 球场信息表
class GroundInfo(db.Model):
    __tablename__ = 'groundinfo'

    id = db.Column(db.Integer, primary_key=True)
    GroundName = db.Column(db.String(20), nullable=False)
    InOrOutDoor = db.Column(db.String(1), nullable=False)
    HaveLight = db.Column(db.String(1), nullable=False)
    IsFree = db.Column(db.String(1), nullable=False)
    Money = db.Column(db.String(10))
    GroundType = db.Column(db.String(10), nullable=False)
    GroundOpenTime = db.Column(db.Time, nullable=False)
    GroundCloseTime = db.Column(db.Time, nullable=False)
    GroudWhere = db.Column(db.Enum, nullable=False)
    HaveShopNearBy = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<GroundInfo %s>' % GroundInfo.GroundId


# 基础参数表
class SysParameter(db.Model):
    __tablename__ = 'sysparameter'

    id = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(10), nullable=False)
    Value = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<SysParameter %s>' % SysParameter.Id
