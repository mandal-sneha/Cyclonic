from your_model_file import predict_cyclone_attributes

def analyze_cyclone_file(image_path):
    analysis_results = predict_cyclone_attributes(image_path)
    return analysis_results