# AIML Learning Platform

A comprehensive AI/ML learning platform designed for students, featuring interactive tutorials, code generation, visual learning aids, audio lessons, and personalized learning paths.

## Features

### 1. Concept Explanations
Get clear, detailed explanations of AI/ML concepts including:
- Neural Networks
- Machine Learning (Supervised & Unsupervised)
- Deep Learning
- Natural Language Processing
- Computer Vision
- And many more topics

### 2. Code Generation
Generate working code examples for various ML algorithms:
- Linear Regression
- Neural Networks
- Classification Models
- Data Preprocessing
- And more implementations

### 3. Visual Learning Aids
Interactive visualizations including:
- Neural Network Architecture
- Decision Tree Structures
- Model flow diagrams

### 4. Audio Lessons
Convert any learning material to audio format using text-to-speech technology for learning on-the-go.

### 5. Personalized Learning
- Track your progress with points and streaks
- Earn achievements
- Get personalized learning path recommendations
- Monitor completed lessons and activities

### 6. Resource Library
Browse comprehensive learning resources filtered by:
- Category (Neural Networks, ML, Deep Learning, etc.)
- Difficulty Level (Beginner, Intermediate, Advanced)
- Type (Tutorial, Project, Video, Article)

## Technology Stack

### Backend
- **Python Flask**: Web framework
- **Supabase**: Database and authentication
- **gTTS**: Text-to-speech for audio generation

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with gradient designs
- **JavaScript**: Interactive functionality
- **Supabase JS Client**: Real-time database and auth

### Database
- **PostgreSQL** (via Supabase)
- Row Level Security (RLS) enabled
- Tables: profiles, resources, user_progress, achievements, learning_paths

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. The Supabase credentials are already configured in the `.env` file

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
project/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── package.json          # Project metadata
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── index.html       # Home page
│   ├── resources.html   # Resources library
│   ├── learn.html       # Interactive learning tools
│   └── profile.html     # User profile dashboard
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       ├── auth.js      # Authentication logic
│       ├── main.js      # Main JavaScript
│       ├── resources.js # Resources page logic
│       ├── learn.js     # Learning tools logic
│       └── profile.js   # Profile page logic
└── README.md            # This file
```

## API Endpoints

### Concept Explanation
- `POST /api/concepts/explain`
- Body: `{ "concept": "neural networks" }`

### Code Generation
- `POST /api/code/generate`
- Body: `{ "task": "linear regression", "language": "python" }`

### Resources
- `GET /api/resources?category=&difficulty=`

### Visualizations
- `GET /api/visualizations/{type}`

### Audio Generation
- `POST /api/audio/generate`
- Body: `{ "text": "Your lesson content" }`

### User Progress
- `GET /api/progress`
- `POST /api/progress`

## Database Schema

### profiles
User profile information with learning statistics

### resources
Learning materials and tutorials

### user_progress
Tracks user progress through resources

### achievements
User achievements and badges

### learning_paths
Personalized learning paths for each user

## Authentication

The platform uses Supabase Authentication with email/password:
- User registration with profile creation
- Secure login
- Session management
- Row Level Security for data privacy

## Usage Guide

1. **Sign Up/Login**: Create an account or login to access all features

2. **Browse Resources**: Visit the Resources page to explore learning materials filtered by your preference

3. **Interactive Learning**: Use the Learn page to:
   - Get concept explanations
   - Generate code examples
   - View visualizations
   - Create audio lessons

4. **Track Progress**: Visit your Profile to:
   - See your learning statistics
   - View achievements
   - Monitor recent activity
   - Get personalized recommendations

## Features for Students

- Beginner-friendly explanations
- Step-by-step code examples
- Visual representations of complex concepts
- Audio lessons for different learning styles
- Gamification with points and achievements
- Personalized learning recommendations

## Security

- Row Level Security (RLS) enabled on all tables
- Users can only access their own data
- Secure authentication with Supabase
- Environment variables for sensitive data

## Future Enhancements

- Integration with AI models for dynamic content generation
- More interactive visualizations
- Video tutorials
- Discussion forums
- Code playgrounds
- Quizzes and assessments
- Mobile app version
