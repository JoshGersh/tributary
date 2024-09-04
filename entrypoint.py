# import the flask web framework
import json
import redis as redis
from flask import Flask, request
from loguru import logger

# Define two constants
HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

# create a Flask server, and allow us to interact with it using the app variable
app = Flask(__name__)


# define an endpoint which accepts POST requests, and is reachable from the /record endpoint
@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200


# practically identical to the above
@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    # Connect to the Redis database
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

    # Retrieve a list of engine temperature values from Redis
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"recived engine temperature successful from redis: {engine_temperature_values}")

    # Convert strings to floats (or int if you're sure the values are whole numbers)
    engine_temperature_sum = 0
    for temp in engine_temperature_values:
        engine_temperature_sum += float(temp)

    # Calculate the average of the engine temperature values
    average_engine_temperature = engine_temperature_sum / len(engine_temperature_values)

    logger.info(f"calculated average engine temperature: {average_engine_temperature}")
    logger.info(f"returning current engine temperature: {engine_temperature_values[0]}")

    # Prepare the result dictionary to be returned as a JSON response
    result = {
        "current_engine_temperature": engine_temperature_values[0],
        "average_engine_temperature": average_engine_temperature
    }
    logger.info(f"collect request successful")

    # Return the result with a 200 OK status code
    return result, 200