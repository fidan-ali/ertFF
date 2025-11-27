# Architecture Documentation

## Folder Structure

/erFF
/src
models.py
factory.py
repository.py
utils.py
/tests
test_models.py
/docs
(*.md files)
main.py
/data
students.json
courses.json
quizzes.json
progress.json

## Core Architectural Decisions

### 1. Use of JSON for Storage
- Simple and lightweight  
- Perfect for Sprint 1 prototyping  
- Requires no external database  
- Human-readable data format  

### 2. Repository Layer (Isolation and Persistence)
This design implements the **Repository Pattern** to decouple the application from the data layer.

 **JsonRepository:** This class handles all data persistence (reading/writing JSON files) and enforces 
 **Decoupling:** Storage logic is isolated; the Controller (`main.py`) only interacts with the          repository's high-level methods, not the JSON files directly.

### 3. Factory Pattern
Used to create entity objects dynamically.  
Improves scalability and reduces coupling.

### 4. High Cohesion, Low Coupling
- Each class has a clearly defined purpose.
- Storage logic is isolated from business classes.
- Object creation is isolated from logic (Factory).

## Interactions
- User → main.py (controller)
- main.py → Factory → Model Objects
- main.py → Repository → JSON Data
