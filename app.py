import datetime
from flask import Flask, jsonify, request, Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from models import FootballPlayerModel

USER = "postgres"
PASS = "postgres"
HOST = "localhost"
PORT = 5432
DB = "football"

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/players", methods=["GET"])
def handle_players():
    if request.method == "GET":
        players = FootballPlayerModel.query.all()
        return jsonify([player.serialize for player in players])
    else:
        return {"message": "failure"}


@app.route("/players/<player_id>", methods=["GET", "PUT", "DELETE"])
def handle_player(player_id):
    if request.method == "GET":
        try:
            player = FootballPlayerModel.query.filter_by(id=player_id).first_or_404()
            return jsonify(player.serialize)
        except:
            return Response(f"ERROR: Football player {player_id} not found!", 404, mimetype='application/json')
    elif request.method == "PUT":
        request_data = request.get_json()
        try:
            player_to_update = db.session.query(FootballPlayerModel).filter_by(id=player_id).first()
            for data in request_data:
                setattr(player_to_update, data, request_data[data])
            player_to_update.last_modified = datetime.datetime.now()
            db.session.commit()
            return Response(f"Football player {player_to_update} updated.", 200, mimetype='application/json')
        except:
            return Response(f"ERROR: Football player {player_id} not found!", 404, mimetype='application/json')
    elif request.method == "DELETE":
        try:
            response = delete_player(player_id)
            return response
        except:
            return Response(f"ERROR: Football player {player_id} not found!", 404, mimetype='application/json')
    else:
        return {"message": "Request method not implemented"}


@app.route('/players', methods=["POST"])
def add_player():
    '''Function to add new player to our database'''
    request_data = request.get_json()  # getting data from client
    player = FootballPlayerModel(request_data["id"],
                                 request_data["first_name"],
                                 request_data["last_name"],
                                 request_data["club"],
                                 request_data["nationality"],
                                 request_data["dob"])
    response = add_player(player)
    return response


def delete_player(player_id):
    player_to_delete = db.session.query(FootballPlayerModel).filter_by(id=player_id).first()
    player_to_delete.delete()
    db.session.commit()
    return Response(f"Football player {player_id} deleted.", 200, mimetype='application/json')


def add_player(player: FootballPlayerModel):
    try:
        db.session.add(player)
        db.session.commit()
        return Response(f"Football player {player} added.", 200, mimetype='application/json')
    except exc.IntegrityError:
        db.session.rollback()
        return Response(f"Error while inserting a player. Player with same id already exists.", 405,
                        mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
