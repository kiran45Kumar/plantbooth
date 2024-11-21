# utils.py (create this file if you don't have it)
def extract_key_points(text):
    # Split text by sentences or bullet points
    points = text.split('.')  # Adjust the delimiter as needed
    return [point.strip() for point in points if point]  # Clean and filter
