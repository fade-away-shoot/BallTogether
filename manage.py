# -*- coding: utf-8 -*-
__author__ = '51439'

# !/usr/bin/env python
import os
from app import create_app, db
from app.models import user_ground,UserPlay,MsgBoard,Follow,UserInfo,UserScore,\
    UserScoreHistory,UserVideo,UserBody,PlayInfo,PlayApllyRecord,GroundInfo,SysParameter
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db,user_ground = user_ground,UserPlay = UserPlay,MsgBoard = MsgBoard,Follow=Follow,
                UserInfo=UserInfo,UserScore=UserScore,UserScoreHistory=UserScoreHistory,UserVideo=UserVideo,
                UserBody=UserBody,PlayInfo=PlayInfo,PlayApllyRecord=PlayApllyRecord,GroundInfo=GroundInfo,SysParameter=SysParameter)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
