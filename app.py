from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
from datetime import datetime
import io
from gtts import gTTS

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/api/concepts/explain', methods=['POST'])
def explain_concept():
    data = request.json
    concept = data.get('concept', '')

    explanations = {
        'neural networks': {
            'title': 'Neural Networks',
            'explanation': 'Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers that process information through weighted connections.',
            'key_points': [
                'Input Layer: Receives the initial data',
                'Hidden Layers: Process information through activation functions',
                'Output Layer: Produces the final result',
                'Backpropagation: Method for training the network'
            ],
            'example': 'A simple neural network for image classification takes pixel values as input, processes them through hidden layers, and outputs class probabilities.'
        },
        'machine learning': {
            'title': 'Machine Learning',
            'explanation': 'Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, learn patterns, and make decisions.',
            'key_points': [
                'Supervised Learning: Learning with labeled data',
                'Unsupervised Learning: Finding patterns in unlabeled data',
                'Reinforcement Learning: Learning through trial and error',
                'Feature Engineering: Selecting relevant data attributes'
            ],
            'example': 'Email spam filters use ML to classify emails as spam or legitimate based on patterns learned from training data.'
        },
        'deep learning': {
            'title': 'Deep Learning',
            'explanation': 'Deep Learning is a subset of machine learning using neural networks with multiple layers. It excels at learning hierarchical representations from data.',
            'key_points': [
                'Multiple hidden layers enable learning complex patterns',
                'Automatic feature extraction from raw data',
                'Requires large amounts of data and computational power',
                'Applications: Computer vision, NLP, speech recognition'
            ],
            'example': 'Deep learning powers facial recognition systems by learning features from thousands of face images.'
        },
        'supervised learning': {
            'title': 'Supervised Learning',
            'explanation': 'Supervised learning uses labeled training data to learn the mapping between inputs and outputs. The algorithm learns from examples with known correct answers.',
            'key_points': [
                'Classification: Predicting discrete categories',
                'Regression: Predicting continuous values',
                'Training set: Data with input-output pairs',
                'Test set: Data for evaluating model performance'
            ],
            'example': 'Predicting house prices based on features like size, location, and age using historical sales data.'
        },
        'unsupervised learning': {
            'title': 'Unsupervised Learning',
            'explanation': 'Unsupervised learning finds hidden patterns in data without labeled responses. The algorithm discovers structure in the input data on its own.',
            'key_points': [
                'Clustering: Grouping similar data points',
                'Dimensionality Reduction: Reducing feature space',
                'Anomaly Detection: Finding unusual patterns',
                'No predefined labels or outputs'
            ],
            'example': 'Customer segmentation groups shoppers based on purchasing behavior without predefined categories.'
        }
    }

    concept_lower = concept.lower().strip()
    explanation = explanations.get(concept_lower, {
        'title': concept,
        'explanation': f'This is an important concept in AI/ML. {concept} involves understanding how algorithms process and learn from data.',
        'key_points': [
            'Understanding fundamentals is crucial',
            'Practice with real-world examples',
            'Study related algorithms and techniques',
            'Build projects to reinforce learning'
        ],
        'example': f'Study {concept} through hands-on projects and code examples.'
    })

    return jsonify(explanation)

@app.route('/api/code/generate', methods=['POST'])
def generate_code():
    data = request.json
    task = data.get('task', '')
    language = data.get('language', 'python')

    code_templates = {
        'linear regression': {
            'python': '''# Linear Regression Implementation
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Model evaluation
score = model.score(X_test, y_test)
print(f"R² Score: {score}")
print(f"Predictions: {predictions}")
'''
        },
        'neural network': {
            'python': '''# Simple Neural Network with TensorFlow/Keras
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Create sample data
X_train = np.random.rand(1000, 20)
y_train = np.random.randint(0, 2, 1000)

# Build model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(20,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train model
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate
print(f"Final accuracy: {history.history['accuracy'][-1]}")
'''
        },
        'data preprocessing': {
            'python': '''# Data Preprocessing Pipeline
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Load data
df = pd.DataFrame({
    'feature1': [1, 2, np.nan, 4, 5],
    'feature2': [10, 20, 30, 40, 50],
    'category': ['A', 'B', 'A', 'C', 'B'],
    'target': [0, 1, 0, 1, 0]
})

# Handle missing values
imputer = SimpleImputer(strategy='mean')
df[['feature1']] = imputer.fit_transform(df[['feature1']])

# Encode categorical variables
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# Scale numerical features
scaler = StandardScaler()
df[['feature1', 'feature2']] = scaler.fit_transform(df[['feature1', 'feature2']])

print(df.head())
'''
        },
        'classification': {
            'python': '''# Classification with Random Forest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("\\nClassification Report:")
print(classification_report(y_test, y_pred))
'''
        }
    }

    task_lower = task.lower().strip()
    code = code_templates.get(task_lower, {
        'python': f'''# {task} Implementation
# This is a template for {task}

import numpy as np
import pandas as pd

def main():
    """
    Main function for {task}
    """
    print("Implement your {task} solution here")

    # Your code here
    pass

if __name__ == "__main__":
    main()
'''
    })

    return jsonify({
        'code': code.get(language, code.get('python')),
        'language': language,
        'task': task
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    resources = [
        {
            'id': 1,
            'category': 'Neural Networks',
            'title': 'Introduction to Neural Networks',
            'description': 'Learn the fundamentals of neural networks and their applications',
            'type': 'tutorial',
            'difficulty': 'beginner'
        },
        {
            'id': 2,
            'category': 'Machine Learning',
            'title': 'Supervised Learning Basics',
            'description': 'Understanding classification and regression algorithms',
            'type': 'tutorial',
            'difficulty': 'beginner'
        },
        {
            'id': 3,
            'category': 'Deep Learning',
            'title': 'Convolutional Neural Networks',
            'description': 'Deep dive into CNNs for image processing',
            'type': 'tutorial',
            'difficulty': 'intermediate'
        },
        {
            'id': 4,
            'category': 'Natural Language Processing',
            'title': 'Text Classification with LSTM',
            'description': 'Build text classifiers using recurrent networks',
            'type': 'project',
            'difficulty': 'advanced'
        },
        {
            'id': 5,
            'category': 'Computer Vision',
            'title': 'Object Detection with YOLO',
            'description': 'Real-time object detection implementation',
            'type': 'project',
            'difficulty': 'advanced'
        },
        {
            'id': 6,
            'category': 'Data Science',
            'title': 'Data Preprocessing Techniques',
            'description': 'Master data cleaning and feature engineering',
            'type': 'tutorial',
            'difficulty': 'beginner'
        }
    ]

    category = request.args.get('category')
    difficulty = request.args.get('difficulty')

    filtered_resources = resources
    if category:
        filtered_resources = [r for r in filtered_resources if r['category'].lower() == category.lower()]
    if difficulty:
        filtered_resources = [r for r in filtered_resources if r['difficulty'].lower() == difficulty.lower()]

    return jsonify(filtered_resources)

@app.route('/api/audio/generate', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        return send_file(
            audio_fp,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name='lesson.mp3'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress', methods=['GET', 'POST'])
def user_progress():
    if request.method == 'POST':
        data = request.json
        return jsonify({
            'status': 'success',
            'message': 'Progress saved',
            'data': data
        })
    else:
        progress_data = {
            'completed_lessons': 12,
            'total_lessons': 50,
            'current_streak': 7,
            'points': 450,
            'level': 'Intermediate',
            'achievements': [
                'First Lesson Complete',
                'Week Streak',
                'Code Master'
            ],
            'recent_activities': [
                {
                    'title': 'Neural Networks Basics',
                    'date': '2024-02-05',
                    'type': 'lesson'
                },
                {
                    'title': 'Linear Regression Project',
                    'date': '2024-02-04',
                    'type': 'project'
                }
            ]
        }
        return jsonify(progress_data)

@app.route('/api/visualizations/<viz_type>')
def get_visualization(viz_type):
    visualizations = {
        'neural-network': {
            'type': 'neural-network',
            'title': 'Neural Network Architecture',
            'description': 'Visual representation of a neural network with input, hidden, and output layers',
            'svg': '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:rgb(59,130,246);stop-opacity:1" />
                        <stop offset="100%" style="stop-color:rgb(147,51,234);stop-opacity:1" />
                    </linearGradient>
                </defs>
                <text x="50" y="30" font-size="14" fill="#333">Input Layer</text>
                <text x="175" y="30" font-size="14" fill="#333">Hidden Layer</text>
                <text x="310" y="30" font-size="14" fill="#333">Output</text>
                <circle cx="50" cy="80" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="50" cy="140" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="50" cy="200" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="200" cy="60" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="200" cy="120" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="200" cy="180" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="200" cy="240" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="350" cy="120" r="20" fill="url(#grad1)" opacity="0.8"/>
                <circle cx="350" cy="180" r="20" fill="url(#grad1)" opacity="0.8"/>
                <line x1="70" y1="80" x2="180" y2="60" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="70" y1="80" x2="180" y2="120" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="70" y1="140" x2="180" y2="120" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="70" y1="140" x2="180" y2="180" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="70" y1="200" x2="180" y2="180" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="70" y1="200" x2="180" y2="240" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="220" y1="60" x2="330" y2="120" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="220" y1="120" x2="330" y2="120" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="220" y1="180" x2="330" y2="180" stroke="#666" stroke-width="1" opacity="0.3"/>
                <line x1="220" y1="240" x2="330" y2="180" stroke="#666" stroke-width="1" opacity="0.3"/>
            </svg>'''
        },
        'decision-tree': {
            'type': 'decision-tree',
            'title': 'Decision Tree Structure',
            'description': 'Visual representation of a decision tree classification',
            'svg': '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                <rect x="150" y="20" width="100" height="40" rx="5" fill="#3b82f6" opacity="0.8"/>
                <text x="200" y="45" font-size="12" fill="white" text-anchor="middle">Root Node</text>
                <rect x="50" y="120" width="80" height="40" rx="5" fill="#10b981" opacity="0.8"/>
                <text x="90" y="145" font-size="12" fill="white" text-anchor="middle">Decision</text>
                <rect x="270" y="120" width="80" height="40" rx="5" fill="#10b981" opacity="0.8"/>
                <text x="310" y="145" font-size="12" fill="white" text-anchor="middle">Decision</text>
                <ellipse cx="50" cy="240" rx="40" ry="25" fill="#8b5cf6" opacity="0.8"/>
                <text x="50" y="245" font-size="11" fill="white" text-anchor="middle">Class A</text>
                <ellipse cx="150" cy="240" rx="40" ry="25" fill="#8b5cf6" opacity="0.8"/>
                <text x="150" y="245" font-size="11" fill="white" text-anchor="middle">Class B</text>
                <ellipse cx="310" cy="240" rx="40" ry="25" fill="#8b5cf6" opacity="0.8"/>
                <text x="310" y="245" font-size="11" fill="white" text-anchor="middle">Class C</text>
                <line x1="180" y1="60" x2="90" y2="120" stroke="#666" stroke-width="2"/>
                <line x1="220" y1="60" x2="310" y2="120" stroke="#666" stroke-width="2"/>
                <line x1="70" y1="160" x2="50" y2="215" stroke="#666" stroke-width="2"/>
                <line x1="100" y1="160" x2="150" y2="215" stroke="#666" stroke-width="2"/>
                <line x1="300" y1="160" x2="310" y2="215" stroke="#666" stroke-width="2"/>
            </svg>'''
        }
    }

    viz = visualizations.get(viz_type, {
        'type': viz_type,
        'title': f'{viz_type} Visualization',
        'description': 'Visual representation',
        'svg': '<svg viewBox="0 0 400 300"><text x="200" y="150" text-anchor="middle">Visualization</text></svg>'
    })

    return jsonify(viz)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
