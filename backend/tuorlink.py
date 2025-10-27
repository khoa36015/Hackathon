from flask import Flask,jsonyfy,request,abort
import mysql.connector

app=Flask(__name__)

def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

#connect mysql
def get_db_connection():
        return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="Authen"
        )
 #api get info all_provinces
@app.route("/api/provinces",methods=['GET'])
def get_all_provinces():
    result=[{'id':'key','ten':data['ten'],'mota':data['mota']} for key,data in provinces.items()]
    return jsonify(result)

#api get info provinces
@app.route("/api/provinces/<id_provinces",methods=['GET'])
def get_provinces(provinces_id):
    provinces=get.provinces(provinces_id.lower())
    if not provinces:
      abort(400,description="khong tim thay tinh")
    return jsonyfy(provinces)
#api search
@app.route("/api/search",methods=['GET'])
def get_search():
    name = request.args.get('name', '').lower()
    for key, info in provinces.items():
        if name in info["ten"].lower():
            return jsonify(info)
    abort(404, description="Không tìm thấy tỉnh này.")
#all_tour
@app.route("/api/tours",methods=['GET'])
def get_tours():
    return jsonify(tours)
#all_tour_hot
@app.route('/api/hot_tours',methods=['GET'])
def get_hot_tours():
    hot_tours=[tour for tour in tours if tour.get("hot", True)]
    return jsonyfy(hot_tours)

if __name__=="__main__":
    app.run(debug=True,port=18)


