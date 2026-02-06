/*
  # AIML Learning Platform Database Schema

  ## Overview
  This migration creates the core database structure for an AI/ML learning platform
  that provides personalized learning experiences for students.

  ## 1. New Tables
  
  ### `profiles`
  User profile information extending Supabase Auth
  - `id` (uuid, primary key) - Links to auth.users
  - `email` (text) - User email
  - `full_name` (text) - User's full name
  - `level` (text) - Current learning level (beginner/intermediate/advanced)
  - `points` (integer) - Gamification points
  - `streak_days` (integer) - Consecutive days of learning
  - `created_at` (timestamptz) - Account creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `resources`
  Learning resources and materials
  - `id` (uuid, primary key) - Unique resource identifier
  - `title` (text) - Resource title
  - `description` (text) - Resource description
  - `category` (text) - Resource category (Neural Networks, ML, Deep Learning, etc.)
  - `difficulty` (text) - Difficulty level (beginner/intermediate/advanced)
  - `type` (text) - Resource type (tutorial/project/video/article)
  - `content` (text) - Resource content or URL
  - `estimated_time` (integer) - Estimated completion time in minutes
  - `created_at` (timestamptz) - Creation timestamp

  ### `user_progress`
  Track user learning progress
  - `id` (uuid, primary key) - Unique progress record
  - `user_id` (uuid, foreign key) - Links to profiles
  - `resource_id` (uuid, foreign key) - Links to resources
  - `status` (text) - Progress status (not_started/in_progress/completed)
  - `completion_percentage` (integer) - Progress percentage (0-100)
  - `started_at` (timestamptz) - When user started
  - `completed_at` (timestamptz) - When user completed
  - `last_accessed` (timestamptz) - Last access time

  ### `achievements`
  User achievements and milestones
  - `id` (uuid, primary key) - Achievement identifier
  - `user_id` (uuid, foreign key) - Links to profiles
  - `title` (text) - Achievement title
  - `description` (text) - Achievement description
  - `earned_at` (timestamptz) - When achievement was earned
  - `badge_icon` (text) - Icon identifier for the badge

  ### `learning_paths`
  Personalized learning paths
  - `id` (uuid, primary key) - Path identifier
  - `user_id` (uuid, foreign key) - Links to profiles
  - `path_name` (text) - Name of the learning path
  - `resources` (jsonb) - Ordered list of resource IDs
  - `created_at` (timestamptz) - Creation timestamp

  ## 2. Security
  - Enable Row Level Security (RLS) on all tables
  - Users can only read/update their own profile data
  - Resources are publicly readable
  - Progress and achievements are private to each user
  - Learning paths are private to each user

  ## 3. Important Notes
  - All timestamps use timestamptz for timezone awareness
  - Foreign keys ensure referential integrity
  - Default values set for common fields
  - RLS policies ensure data privacy and security
*/

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text UNIQUE NOT NULL,
  full_name text,
  level text DEFAULT 'beginner' CHECK (level IN ('beginner', 'intermediate', 'advanced')),
  points integer DEFAULT 0,
  streak_days integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create resources table
CREATE TABLE IF NOT EXISTS resources (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text,
  category text NOT NULL,
  difficulty text DEFAULT 'beginner' CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
  type text DEFAULT 'tutorial' CHECK (type IN ('tutorial', 'project', 'video', 'article')),
  content text,
  estimated_time integer DEFAULT 30,
  created_at timestamptz DEFAULT now()
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  resource_id uuid REFERENCES resources(id) ON DELETE CASCADE NOT NULL,
  status text DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
  completion_percentage integer DEFAULT 0 CHECK (completion_percentage >= 0 AND completion_percentage <= 100),
  started_at timestamptz,
  completed_at timestamptz,
  last_accessed timestamptz DEFAULT now(),
  UNIQUE(user_id, resource_id)
);

-- Create achievements table
CREATE TABLE IF NOT EXISTS achievements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  title text NOT NULL,
  description text,
  earned_at timestamptz DEFAULT now(),
  badge_icon text DEFAULT 'trophy'
);

-- Create learning_paths table
CREATE TABLE IF NOT EXISTS learning_paths (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  path_name text NOT NULL,
  resources jsonb DEFAULT '[]'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

-- Resources policies (publicly readable)
CREATE POLICY "Anyone can view resources"
  ON resources FOR SELECT
  TO authenticated
  USING (true);

-- User progress policies
CREATE POLICY "Users can view own progress"
  ON user_progress FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
  ON user_progress FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
  ON user_progress FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own progress"
  ON user_progress FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Achievements policies
CREATE POLICY "Users can view own achievements"
  ON achievements FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own achievements"
  ON achievements FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Learning paths policies
CREATE POLICY "Users can view own learning paths"
  ON learning_paths FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own learning paths"
  ON learning_paths FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own learning paths"
  ON learning_paths FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own learning paths"
  ON learning_paths FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Insert sample resources
INSERT INTO resources (title, description, category, difficulty, type, content, estimated_time) VALUES
  ('Introduction to Neural Networks', 'Learn the fundamentals of neural networks and how they work', 'Neural Networks', 'beginner', 'tutorial', 'neural-networks-intro', 45),
  ('Building Your First ML Model', 'Step-by-step guide to creating a machine learning model', 'Machine Learning', 'beginner', 'tutorial', 'first-ml-model', 60),
  ('Deep Learning with CNNs', 'Master convolutional neural networks for image processing', 'Deep Learning', 'intermediate', 'tutorial', 'cnn-deep-dive', 90),
  ('Natural Language Processing Basics', 'Introduction to NLP and text processing', 'NLP', 'beginner', 'tutorial', 'nlp-basics', 50),
  ('Advanced Reinforcement Learning', 'Deep dive into RL algorithms and applications', 'Reinforcement Learning', 'advanced', 'tutorial', 'advanced-rl', 120),
  ('Computer Vision Project', 'Build a real-world object detection system', 'Computer Vision', 'intermediate', 'project', 'cv-project', 180)
ON CONFLICT DO NOTHING;
