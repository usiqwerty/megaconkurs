from flask import Flask, request
from flask_cors import CORS, cross_origin

from main import find_all_vuzes, get_vuz_info, get_rating, get_vuz_programs

app = Flask(__name__)
CORS(app)
HOST = "0.0.0.0"
PORT = 5000


@app.route('/')
def hello_world():  # put application's code here
	return 'Hello World!'


@app.route('/api/get_vuz_programs', methods=["GET"])
@cross_origin()
def api_get_vuz_programs():
	args = request.args
	if "vuz" not in args:
		return {'error': "Bad Request"}, 400
	return get_vuz_programs(args["vuz"])


@app.route('/api/get_vuz_info', methods=["GET"])
@cross_origin()
def api_get_vuz_info():
	args = request.args
	if "vuz" not in args:
		return {'error': "Bad Request"}, 400
	vuz = get_vuz_info(args["vuz"])
	return {"code": vuz.code, "name": vuz.full_name}


@app.route('/api/get_all_vuzes', methods=["GET"])
@cross_origin()
def api_get_all_vuzes():
	return [{"name": vuz.name, "code": vuz.code} for vuz in find_all_vuzes()]


@app.route('/api/get_rating', methods=["GET"])
@cross_origin()
def api_get_rating():
	args = request.args
	if "vuz" not in args or "rating_id" not in args:
		return {'error': "Bad Request"}, 400
	vuz = args["vuz"]
	rating_id = args["rating_id"]

	rating = [{
		"pos":rt.position_number,
		"snils":rt.snils,
		"score": rt.score,
		"confirmed": rt.confirmed,
		"bvi": rt.bvi,
		"other": [{"code":x.code, "confirmed":x.confirmed, "vuz":x.vuz, "position":x.position_number} for x in rt.other_programs]
	} for rt in get_rating(vuz, rating_id)]

	return {"vuz": vuz, "code": rating_id, "rating": rating}


if __name__ == '__main__':
	app.run(host=HOST, port=PORT)
