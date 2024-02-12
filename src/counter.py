from src import status

from flask import Flask
app = Flask(__name__)


COUNTERS = {}


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


# Route as put method
@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Update a counter"""
    # Create a route for method PUT on endpoint /counters/<name>
    app.logger.info(f"Request to update counter: {name}")
    global COUNTERS
    # Make sure the counter exists
    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist"}, status.HTTP_404_NOT_FOUND
    # Create a function to implement that route
    # Increment the counter by 1
    COUNTERS[name] += 1
    # Return the new counter and a 200_OK return code.
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Should get a counter"""
    # Very similar to update without the increment I think
    app.logger.info(f"Request to get counter: {name}")
    global COUNTERS
    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist"}, status.HTTP_404_NOT_FOUND
    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Should delete a counter"""
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS
    # Doesn't have to return the code 404_NOT_FOUND as not in specifications of REST API, but will anyways I guess
    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist"}, status.HTTP_404_NOT_FOUND
    del COUNTERS[name]
    return {"Message": f"Counter {name} successfully deleted!"}, status.HTTP_204_NO_CONTENT