from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests, os, json, math
import redis
import ijson
from concurrent.futures import ThreadPoolExecutor, as_completed

apiKey = os.environ.get('API_KEY')

def load_cities_data():
    with open('static/city.list.json', 'r', encoding="utf-8") as file:
        pipeline = cache.pipeline()
        for city in ijson.items(file, "item"):
            coord = float(city['coord']['lon']), float(city['coord']['lat']), city['name']
            pipeline.geoadd("cities", coord)
        print("Execute pipeline")
        pipeline.execute()
        print("Write complete")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/selected_area', methods=['POST'])
def selected_area():
    try:
        data = json.loads(request.data)
        print(f"Received selected area: {data}")
        minLon = data['minLon']
        maxLon = data['maxLon']
        minLat = data['minLat']
        maxLat = data['maxLat']
        centerLon = (minLon + maxLon) / 2
        centerLat = (minLat + maxLat) / 2
        radius = math.sqrt((maxLon - centerLon) ** 2 + (maxLat - centerLat) ** 2) * 111.32 # convert from cordinate value to km value
        print(f"radius {radius} centerLon {centerLon} centerLat {centerLat}")
        nearby_cities = cache.georadius("cities", centerLon, centerLat, radius, unit="km")

        filtered_city_ids = []
        for city_id in nearby_cities:
            city_pos = cache.geopos("cities", city_id)
            if city_pos:
                lon, lat = city_pos[0]
                if minLon <= lon <= maxLon and minLat <= lat <= maxLat:
                    filtered_city_ids.append(city_id.decode("utf-8"))

        print(filtered_city_ids)
        filtered_cities = []
        filtered_cities_failed = []
        if (len(filtered_city_ids) > 100):
            return jsonify({"status": "fail", "message": "Bad request", "data": "Your bounding box too large, shrink it"}), 400
        with ThreadPoolExecutor() as executor:
            future_to_city = {executor.submit(requests.get, f'https://api.openweathermap.org/data/2.5/weather?q={city_id}&appid={apiKey}'): city_id for city_id in filtered_city_ids}
            for future in as_completed(future_to_city):
                res = future.result()
                if res.status_code == 200:
                    filtered_cities.append(res.json())
                else:
                    filtered_cities_failed.append(city_id.decode("utf-8"))
                    
            executor.shutdown(wait=True)
        print(f"filtered_cities_failed {filtered_cities_failed}")
        # Add retry here and append to filtered_cities
        print(f"Response selected area: {filtered_cities}")
        return jsonify({"status": "success", "message": "Area received", "data": filtered_cities})
    except Exception as e:
        return jsonify({"status": "fail", "message": "Internal Server Error", "data": f"{e}"}), 500

if __name__ == '__main__':
    load_dotenv()   
    cache = redis.Redis(
                        host=os.environ.get('REDIS_HOST'),
                        port=int(os.environ.get('REDIS_PORT')),
                        #password=os.environ.get('REDIS_PASSWORD')
                        )
    load_cities_data()
    app.run(debug=True)
