"""
Flask RBAC Application with Admin Panel and REST API
Author: Senior Python Full Stack Developer
Description: Complete Role-Based Access Control system with CRUD operations
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Change this in production

# Database configuration
DATABASE = 'database.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

# ==================== CUSTOM DECORATORS ====================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        try:
            db = get_db()
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      (username, hashed_password, 'user'))
            db.commit()
            db.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('login'))
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {username}!', 'success')
            
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

# ==================== STUDENT CRUD OPERATIONS ====================

@app.route('/students')
@login_required
def view_students():
    """View all students"""
    db = get_db()
    students = db.execute('SELECT * FROM students ORDER BY id').fetchall()
    db.close()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add new student"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        
        # Validation
        if not name or not email or not course:
            flash('All fields are required', 'error')
            return redirect(url_for('add_student'))
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Invalid email format', 'error')
            return redirect(url_for('add_student'))
        
        db = get_db()
        db.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
                  (name, email, course))
        db.commit()
        db.close()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('view_students'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    """Edit student details"""
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('view_students'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        
        if not name or not email or not course:
            flash('All fields are required', 'error')
            return redirect(url_for('edit_student', id=id))
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Invalid email format', 'error')
            return redirect(url_for('edit_student', id=id))
        
        db.execute('UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?',
                  (name, email, course, id))
        db.commit()
        db.close()
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('view_students'))
    
    db.close()
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:id>')
@admin_required
def delete_student(id):
    """Delete student (Admin only)"""
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    
    if student:
        db.execute('DELETE FROM students WHERE id = ?', (id,))
        db.commit()
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found', 'error')
    
    db.close()
    return redirect(url_for('view_students'))

# ==================== ADMIN PANEL ====================

@app.route('/admin')
@admin_required
def admin():
    """Admin dashboard"""
    db = get_db()
    
    # Get all users
    users = db.execute('SELECT id, username, role FROM users ORDER BY id').fetchall()
    
    # Get all students
    students = db.execute('SELECT * FROM students ORDER BY id').fetchall()
    
    db.close()
    
    return render_template('admin.html', users=users, students=students)

# ==================== REST API ENDPOINTS ====================

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """GET all students"""
    db = get_db()
    students = db.execute('SELECT id, name, email, course FROM students').fetchall()
    db.close()
    
    students_list = []
    for student in students:
        students_list.append({
            'id': student['id'],
            'name': student['name'],
            'email': student['email'],
            'course': student['course']
        })
    
    return jsonify(students_list)

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """POST new student"""
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'email', 'course']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Field "{field}" is required and cannot be empty'}), 400
        
        # Email validation
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        db = get_db()
        cursor = db.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
                           (data['name'], data['email'], data['course']))
        db.commit()
        student_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'message': 'Student added successfully',
            'id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:id>', methods=['PUT'])
def api_update_student(id):
    """PUT update student"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        db = get_db()
        student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
        
        if not student:
            db.close()
            return jsonify({'error': 'Student not found'}), 404
        
        # Validation
        if 'name' in data and data['name']:
            name = data['name']
        else:
            name = student['name']
            
        if 'email' in data and data['email']:
            email = data['email']
            # Email validation
            email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
            if not re.match(email_pattern, email):
                db.close()
                return jsonify({'error': 'Invalid email format'}), 400
        else:
            email = student['email']
            
        if 'course' in data and data['course']:
            course = data['course']
        else:
            course = student['course']
        
        db.execute('UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?',
                  (name, email, course, id))
        db.commit()
        db.close()
        
        return jsonify({'message': 'Student updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:id>', methods=['DELETE'])
def api_delete_student(id):
    """DELETE student"""
    try:
        db = get_db()
        student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
        
        if not student:
            db.close()
            return jsonify({'error': 'Student not found'}), 404
        
        db.execute('DELETE FROM students WHERE id = ?', (id,))
        db.commit()
        db.close()
        
        return jsonify({'message': 'Student deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
