import pandas as pd
import os
from datetime import datetime
import streamlit as st
import hashlib
import json

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_user_file_path(self, username, file_type="study"):
        """Get file path for user data"""
        if file_type == "study":
            return os.path.join(self.data_dir, f"{username}_study_data.csv")
        elif file_type == "quiz":
            return os.path.join(self.data_dir, f"{username}_quiz_data.csv")
        elif file_type == "auth":
            return os.path.join(self.data_dir, "user_auth.json")
        else:
            return os.path.join(self.data_dir, f"{username}_{file_type}_data.csv")
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_auth_data(self):
        """Load authentication data from file"""
        auth_file = self.get_user_file_path("", "auth")
        if os.path.exists(auth_file):
            try:
                with open(auth_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_auth_data(self, auth_data):
        """Save authentication data to file"""
        auth_file = self.get_user_file_path("", "auth")
        try:
            with open(auth_file, 'w') as f:
                json.dump(auth_data, f)
            return True
        except:
            return False
    
    def create_user(self, username, password):
        """Create a new user profile with password"""
        # Check if user already exists
        auth_data = self._load_auth_data()
        if username in auth_data:
            return False, "Username already exists!"
        
        file_path = self.get_user_file_path(username)
        if os.path.exists(file_path):
            return False, "User data already exists!"
        
        # Create empty DataFrame with proper columns
        columns = ['date', 'subject', 'chapter', 'duration_minutes', 'confidence_rating', 'notes', 'timestamp']
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_csv(file_path, index=False)
        
        # Save user authentication data
        auth_data[username] = {
            'password_hash': self._hash_password(password),
            'created_date': datetime.now().isoformat()
        }
        
        if self._save_auth_data(auth_data):
            return True, "User created successfully!"
        else:
            return False, "Failed to save authentication data!"
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        auth_data = self._load_auth_data()
        
        if username not in auth_data:
            return False, "Username not found!"
        
        stored_hash = auth_data[username]['password_hash']
        input_hash = self._hash_password(password)
        
        if stored_hash == input_hash:
            return True, "Authentication successful!"
        else:
            return False, "Incorrect password!"
    
    def get_all_users(self):
        """Get list of all existing users from auth file"""
        auth_data = self._load_auth_data()
        return sorted(list(auth_data.keys()))
    
    def get_user_data(self, username):
        """Load user's study data"""
        file_path = self.get_user_file_path(username)
        
        if not os.path.exists(file_path):
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            # Ensure date column is properly formatted
            if not df.empty and 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.date
            return df
        except Exception as e:
            st.error(f"Error loading user data: {str(e)}")
            return pd.DataFrame()

    
    def log_study_session(self, username, subject, chapter, duration, confidence, date, notes=""):
        """Log a new study session"""
        try:
            file_path = self.get_user_file_path(username)
            
            # Create new session data
            new_session = {
                'date': date,
                'subject': subject,
                'chapter': chapter,
                'duration_minutes': duration,
                'confidence_rating': confidence,
                'notes': notes,
                'timestamp': datetime.now().isoformat()
            }
            
            # Load existing data or create new DataFrame
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
            else:
                df = pd.DataFrame()
            
            # Append new session
            new_df = pd.DataFrame([new_session])
            df = pd.concat([df, new_df], ignore_index=True)
            
            # Save back to CSV
            df.to_csv(file_path, index=False)
            return True
            
        except Exception as e:
            st.error(f"Error logging study session: {str(e)}")
            return False
    

    def delete_user_data(self, username):
        """Delete all data for a user including authentication"""
        try:
            study_file = self.get_user_file_path(username, "study")
            
            if os.path.exists(study_file):
                os.remove(study_file)
            
            # Remove from auth data
            auth_data = self._load_auth_data()
            if username in auth_data:
                del auth_data[username]
                self._save_auth_data(auth_data)
            
            return True
        except Exception as e:
            st.error(f"Error deleting user data: {str(e)}")
            return False
    
    def backup_user_data(self, username):
        """Create a backup of user data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.data_dir, "backups")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Backup study data
            study_file = self.get_user_file_path(username, "study")
            if os.path.exists(study_file):
                backup_study_file = os.path.join(backup_dir, f"{username}_study_backup_{timestamp}.csv")
                pd.read_csv(study_file).to_csv(backup_study_file, index=False)
            
            return True
        except Exception as e:
            st.error(f"Error creating backup: {str(e)}")
            return False
