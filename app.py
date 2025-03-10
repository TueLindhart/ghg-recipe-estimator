import asyncio
import threading
from enum import StrEnum
from typing import Callable, TypedDict

from flask import Flask, jsonify, render_template, request

from comparison_api import comparison_api
from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.estimator import RunParams, env_use_cache

app = Flask(__name__)

app.register_blueprint(comparison_api)


class StatusTypes(StrEnum):
    Processing = "Processing"
    Completed = "Completed"
    Error = "Error"


class Result(TypedDict):
    status: str
    result: str | None


results = {}


def run_in_thread(func: Callable, runparams: RunParams):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        success, result = loop.run_until_complete(func(runparams=runparams))
        if not success:
            results[runparams.uid] = Result(
                status=StatusTypes.Error.value, result=result
            )
        else:
            results[runparams.uid] = Result(
                status=StatusTypes.Completed.value, result=result
            )
    except Exception as exc_info:
        results[runparams.uid] = Result(
            status=StatusTypes.Error.value, result=str(exc_info)
        )
    finally:
        loop.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate")
def calculate():
    url = request.args.get("input_data")
    if not url:
        return jsonify(status="No input provided"), 400

    use_cache = request.args.get("use_cache")
    use_cache = env_use_cache() if use_cache is None else use_cache.lower() == "true"
    runparams = RunParams(url=url, use_cache=use_cache)
    results[runparams.uid] = Result(status=StatusTypes.Processing.value, result=None)
    threading.Thread(
        target=run_in_thread, kwargs={"func": async_estimator, "runparams": runparams}
    ).start()

    return jsonify(
        status="Processing", input_data=url, uid=runparams.uid
    ), 202  # Return 202 Accepted status


@app.route("/status/<uid>")
def status(uid):
    result = results.get(uid)
    if not result:
        return jsonify(status="Not Found"), 404

    return jsonify(result), 200


@app.route("/clear-result/<uid>")
def clear_result(uid):
    results.pop(uid, None)
    return jsonify(status="Cleared")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
