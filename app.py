from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import random
import time
from simulation_engine import SimulationEngine

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize the Simulation Engine
engine = SimulationEngine()

INDUSTRY_IDEAS = {
    "tech": [
        "An AI-powered resume screening tool for Indian startups that analyzes resumes for cultural fit and technical skills",
        "A subscription-based design platform for small businesses offering logo creation and social media templates",
        "A remote work productivity suite with virtual office spaces and task synchronization",
        "A cybersecurity compliance checker for Indian SMEs adapting to new data protection laws"
    ],
    "retail": [
        "A hyper-local grocery delivery aggregation app for tier-2 Indian cities",
        "A D2C sustainable fashion marketplace connecting rural artisans with urban buyers",
        "An AR-based virtual try-on plugin for small eyewear and jewellery retailers",
        "A smart inventory management system for Kirana stores using image recognition"
    ],
    "health": [
        "A vernacular telemedicine app connecting rural patients with city specialists",
        "A mental wellness platform for Indian students focusing on exam stress and career anxiety",
        "A diet planning app customized for Indian vegetarian and regional cuisines",
        "An affordable elderly care coordination service for families living abroad"
    ],
    "food": [
        "A ghost kitchen incubator platform for home chefs in metro cities",
        "A farm-to-table subscription box delivering organic vegetables to urban societies",
        "An AI-driven food waste management system for wedding halls and hotels",
        "A regional snack discovery box subscription featuring authentic local treats"
    ]
}

@app.route('/')
def home():
    return render_template('front.html')

@app.route('/api/industry-ideas/<industry_id>', methods=['GET'])
def get_industry_ideas(industry_id):
    # Simulate network delay for realism
    time.sleep(0.5) 
    
    ideas = INDUSTRY_IDEAS.get(industry_id, [])
    if not ideas:
        return jsonify({"error": "Industry not found"}), 404
        
    return jsonify({"ideas": ideas})

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    idea_text = data.get('idea')
    
    if not idea_text:
        return jsonify({"error": "No idea provided"}), 400

    # Run the simulation
    # Delays will be handled inside the engine or frontend polling, 
    # but here we simulate the processing time before returning
    # In a real async app we'd use a job queue, but for this demo we'll wait.
    # The requirement says "realistic processing delays (3-7 seconds total) with progress updates"
    # To support progress updates, we might need a streaming response or just FE simulation.
    # Given the constraint of a simple POST, the FE simulates the "Simulating..." steps
    # and we just sleep a bit here to account for "calculation".
    
    time.sleep(2) # Backend processing time
    
    result = engine.run_simulation(idea_text)
    return jsonify(result)

@app.route('/api/download-report', methods=['POST'])
def download_report():
    data = request.json
    report_id = data.get('report_id')
    
    # Get path from engine cache
    filepath = engine.get_report_path(report_id)
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Report not found"}), 404

    filename = os.path.basename(filepath)
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
