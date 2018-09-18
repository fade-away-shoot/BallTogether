# -*- coding: utf-8 -*-
__author__ = '51439'

from . import game
from flask import render_template, flash, redirect, url_for
from ..models import PlayInfo
from ..models import db
from .forms import CreateTeamForm
from flask_login import current_user, login_required


@game.route('/findteam', methods=['GET', 'POST'])
@login_required
def findteam():
    teams = PlayInfo.query.filter_by(PlayStatus='0').all()
    return render_template('game/findteam.html', teams=teams)


@game.route('/editteam/<teamid>', methods=['GET', 'POST'])
@login_required
def editteam(teamid):
    form = CreateTeamForm()
    game = PlayInfo.query.filter_by(id=teamid).first()
    if game:
        form.title.data = game.PlayTitle
        form.groundid.data = game.GroundId
        form.playtime.data = game.PlayTime
        form.playtype.data = game.PlayType
        form.needman.data = game.NeedManCount
        form.money.data = game.Money
        form.wantman.data = game.WantMan
        form.playinfo.data = game.PlayInfo
    if form.validate_on_submit():
        if game:
            game.PlayTitle = form.title.data
            game.GroundId = form.groundid.data
            game.PlayTime = form.playtime.data
            game.PlayType = form.playtype.data
            game.NeedManCount = form.needman.data
            game.Money = form.money.data
            game.WantMan = form.wantman.data
            game.PlayInfo = form.playinfo.data
        else:
            game = PlayInfo(PlayTitle=form.title.data, GroundId=form.groundid.data, PlayTime=form.playtime.data,
                            PlayType=form.playtype.data, NeedManCount=form.needman.data,
                            Money=form.money.data, WantMan=form.wantman.data, PlayInfo=form.playinfo.data,
                            LeaderMan=current_user.id)
            db.session.add(game)
            current_user.joinplay(game)
        db.session.commit()
        flash('成功发布约球信息')
        return redirect(url_for('game.gameinfo', teamid=game.id))
    return render_template('game/editteam.html', form=form)


@game.route('/jointeam/<teamid>')
@login_required
def jointeam(teamid):
    game = PlayInfo.query.filter_by(id=teamid, PlayStatus='0').first()
    if not game:
        flash('你感兴趣的约球不存在或不在招人状态！')
        return redirect(url_for('game.findteam'))
    current_user.joinplay(game)
    flash('干就完事了！')
    return redirect(url_for('game.gameinfo', teamid=teamid))


@game.route('/quitteam/<teamid>')
@login_required
def quitteam(teamid):
    game = PlayInfo.query.filter_by(id=teamid, PlayStatus='0').first()
    if not game:
        flash('无法退出！')
        return redirect(url_for('game.findteam'))
    if game.LeaderMan == current_user.id:
        flash('宝贝儿，别混了，你组织的你退出？')
        return redirect(url_for('game.findteam'))
    current_user.quitplay(game)
    flash('成功退出！')
    return redirect(url_for('game.findteam'))


@game.route('/gameinfo/<teamid>')
@login_required
def gameinfo(teamid):
    team = PlayInfo.query.filter_by(id=teamid).first_or_404()
    dicjoined = {}
    for joined_user in team.users.all():
        dicjoined[joined_user.users.UserName] = '/static/image/' + joined_user.users.UserName + '.jpg'
    return render_template('game/gameinfo.html', team=team, dicjoined=dicjoined)
