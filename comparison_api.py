import json
import random

from flask import Blueprint, jsonify, request

comparison_api = Blueprint("comparison_api", __name__)


def generate_context_text(record, input_value):
    """
    Generate a context text by comparing the input_value (e.g., recipe recipy)
    to the stored value for the given activity. The stored record contains:
        - name: a short title of the activity (e.g., "Flight from Paris to Berlin")
        - value: the CO₂ emission value for that activity.

    The function calculates the ratio between input_value and stored_value
    and selects an appropriate narrative.
    """
    stored_value = record.get("value", 0)
    if stored_value == 0:
        return "Comparison data is insufficient for a meaningful comparison."

    # Calculate ratio and percentage.
    ratio = input_value / stored_value
    percent = round(ratio * 100)

    if ratio < 0.5:
        # Input is less than half the stored value.
        return f"Your recipe are about {percent}% of those from {record['name']}."
    elif ratio < 0.9:
        # Input is somewhat lower than the stored value.
        return f"Your recipe are {record['name']} (around {percent}%)."
    elif ratio <= 1.1:
        # Input is roughly equivalent.
        return f"Your recipe are roughly equivalent to {record['name']}."
    elif ratio <= 2:
        # Input is higher but within a moderate range.
        excess = round((ratio - 1) * 100)
        return f"Your recipe are approximately {percent}% of those from {record['name']}, which is about {excess}% more."
    else:
        # Input is much higher.
        return f"Your recipe are significantly higher than those from {record['name']} (over {round(ratio, 1)} times as much)."


@comparison_api.route("/api/comparison", methods=["GET"])
def get_comparison():
    # Get input parameters from the query string: e.g., /api/comparison?value=100&unit=kg
    try:
        input_value = float(request.args.get("value", 0))
    except (ValueError, TypeError):
        input_value = 0

    # Load the stored comparison data
    try:
        with open("data/comparison_activities.json", "r") as f:
            comparisons = json.load(f)
    except Exception:
        return jsonify({"error": "Comparison data not available"}), 500

    if not comparisons:
        return jsonify({"error": "No comparison data found"}), 404

    # Randomly select one record from the stored comparisons.
    record = random.choice(comparisons)
    stored_value = record.get("value", 0)
    if stored_value == 0:
        factor = 0
    else:
        factor = (input_value / stored_value) * 100

    # Calculate a context factor as a percentage.
    contextFactor = f"{round(factor)}%"

    # Generate a dynamic context text based on the input recipy.
    contextText = generate_context_text(record, input_value)

    # Add the calculated fields to the record.
    record["contextFactor"] = contextFactor
    record["contextText"] = contextText

    return jsonify(record)
