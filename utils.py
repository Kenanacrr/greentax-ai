# util.py

import logging  # Removed unused imports


def generate_mock_recommendations(data):
    try:
        # Validate input
        if not isinstance(data, list) or not data:
            raise ValueError('Input data must be a non-empty list.')
        recommendations = []
        for item in data:
            # Generate recommendations based on input
            recommendations.append(f'Recommendation for {item}')
        return recommendations
    except Exception as e:
        logging.error(f'Error generating recommendations: {e}')
        return []  # Return empty list on error


def another_function():
    pass  # This is just an example function

# Add more functions as needed
