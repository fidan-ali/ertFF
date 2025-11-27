import json
import os
import logging

# Setup simple logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('Repo')

class JsonRepository:
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.file_path = f'data/{entity_name.lower()}s.json'
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    # --- Check Methods ---
    
    def get_by_id(self, entity_id):
        """Checks for existing ID (Primary Key)."""
        data = self._load_data()
        return next((item for item in data if item.get('id') == entity_id), None)
    
    def get_by_id_key(self, key, value):
        """Checks for a key/value pair (e.g., name or email)."""
        data = self._load_data()
        return next((item for item in data if item.get(key) == value), None)

    # Note: name_exists is no longer used for Student, but kept for general utility.
    def email_exists(self, email):
        """Helper to check if an email already exists (for Student)."""
        return self.get_by_id_key('email', email) is not None

    def create(self, entity):
        entity_dict = entity.to_dict()
        entity_type = self.entity_name
        
        # --- ENFORCE UNIQUENESS CONSTRAINTS (Strictly as requested) ---
        
        # 1. PRIMARY KEY CHECK (ID / Course ID / Quiz ID / Progress ID MUST be unique)
        if self.get_by_id(entity_dict.get('id')):
             raise ValueError(f"❌ Cannot create {entity_type}: ID {entity_dict.get('id')} already exists!")
             
        # 2. Specific Checks
        if entity_type == 'Student':
            # ONLY Email check is applied for Student. Name check is removed.
            if self.email_exists(entity_dict.get('email')): 
                raise ValueError(f"❌ Cannot create Student: Email '{entity_dict.get('email')}' already registered.")
                
        if entity_type == 'Course':
            # ONLY Title check is applied for Course.
            if self.get_by_id_key('title', entity_dict.get('title')): 
                raise ValueError(f"❌ Cannot create Course: Title '{entity_dict.get('title')}' already exists.")


        # If all checks pass, save the data
        data = self._load_data()
        data.append(entity_dict)
        self._save_data(data)
        logger.info(f"✔️ Saved {self.entity_name} successfully.")