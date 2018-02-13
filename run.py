from json import dumps
from flask import Flask, render_template
import functions
from datetime import datetime
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/live', methods=['GET', 'POST'])
def live():
    data = functions.get_live_matches()
    return render_template('live.html', data=data)


@app.route('/live/<team>/<opp>', methods=['GET', 'POST'])
def live_calc(team, opp):
    team_final_prob, opp_final_prob, draw_final_prob = functions.calc_live(team, opp)
    draw_final = float(draw_final_prob) * int(100)
    team_final = float(team_final_prob) * int(100)
    opp_final = float(opp_final_prob) * int(100)
    return render_template('live-game.html', team=team, opp=opp, team_final=int(team_final), opp_final=int(opp_final), draw_final=int(draw_final))


@app.route('/future', methods=['GET', 'POST'])
def future():
    return render_template('future.html')


@app.route('/future/<team>', methods=['GET', 'POST'])
def future_team(team):
    id, opps, myteam = functions.get_future_matches(team)
    return render_template('future-team.html', team=myteam, id=id, opps=dumps(opps))


@app.route('/future/<date>/<team>/<opp>', methods=['GET', 'POST'])
def future_games(date, team, opp):
    team_final_prob, opp_final_prob, draw_final_prob = functions.calc_future(date, team, opp)
    team_final = float(team_final_prob) * int(100)
    opp_final = float(opp_final_prob) * int(100)
    draw_final = float(draw_final_prob) * int(100)
    date_dt = datetime.strptime(date, '%Y-%m-%d')
    date = datetime.strftime(date_dt, '%a %d %b %Y')
    return render_template('future-game.html', team=team, opp=opp, date=date, team_final=int(team_final), opp_final=int(opp_final), draw_final=int(draw_final))


if __name__ == '__main__':
    app.run()
