import json
import logging
import random

from flask import Blueprint, jsonify, request

comparison_api = Blueprint("comparison_api", __name__)

# Set up a logger for this module (if not already set by your Flask app)
logger = logging.getLogger("foodprint")
logger.setLevel(logging.DEBUG)  # Ensure debug level logging


def generate_context_text(record, input_value):
    """
    Generate a context text by comparing the input_value (e.g., recipe emission)
    to the stored value for the given activity.
    """

    stored_value = record.get("value", 0)
    if stored_value == 0:
        text = "Sammenligningsdata er utilstrækkelige til en meningsfuld sammenligning."
        logger.debug("Stored value is 0; returning: %s", text)
        return text

    # Calculate ratio and percentage.
    ratio = input_value / stored_value
    percent = round(ratio * 100)
    logger.debug("Calculated ratio: %s, percent: %s", ratio, percent)

    if ratio < 0.5:
        text = f"Din opskrift er omkring {percent}% af {record['description']}."
    elif ratio < 0.9:
        text = f"Din opskrift er {record['description']} (omkring {percent}%)."
    elif ratio <= 1.1:
        text = f"Din opskrift svarer nogenlunde til {record['description']}."
    elif ratio <= 2:
        excess = round((ratio - 1) * 100)
        text = f"Din opskrift er cirka {percent}% af {record['description']}, hvilket er omkring {excess}% mere."
    else:
        text = f"Din opskrift er væsentligt højere end {record['description']} (over {round(ratio, 1)} gange så meget)."

    logger.debug("Generated context text")
    return text


@comparison_api.route("/api/comparison", methods=["GET"])
def get_comparison():
    logger.debug("Received request for /api/comparison")

    # Get input parameters from the query string.
    try:
        input_value = float(request.args.get("value", 0))
    except (ValueError, TypeError) as e:
        logger.error("Error converting input value: %s", e)
        input_value = 0
    input_unit = request.args.get("unit", "").lower()
    logger.debug("Input parameters - value: %s, unit: %s", input_value, input_unit)

    # Load the stored comparison data.
    try:
        with open("food_co2_estimator/data/comparison_activities.json", "r") as f:
            comparisons = json.load(f)
        logger.debug("Loaded comparisons")
    except Exception as e:
        logger.error("Error loading comparisons: %s", e)
        return jsonify({"error": "Sammenligningsdata ikke tilgængelige"}), 500

    if not comparisons:
        logger.warning("No comparisons found in data file.")
        return jsonify({"error": "Ingen sammenligningsdata fundet"}), 404

    # Randomly select one record from the stored comparisons.
    record = random.choice(comparisons)
    logger.debug("Selected record")
    stored_value = record.get("value", 0)
    if stored_value == 0:
        factor = 0
    else:
        factor = (input_value / stored_value) * 100

    # Calculate a context factor as a percentage.
    contextFactor = f"{round(factor)}%"
    logger.debug("Computed context factor: %s", contextFactor)

    # Generate a dynamic context text based on the input value.
    contextText = generate_context_text(record, input_value)

    # Add the calculated fields to the record.
    record["contextFactor"] = contextFactor
    record["contextText"] = contextText

    logger.debug("Final record to return.")
    return jsonify(record)
