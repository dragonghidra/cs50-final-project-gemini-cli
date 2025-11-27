from flask import Blueprint, jsonify, request
from .models import db, Task, Note

api = Blueprint('api', __name__)

@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@api.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(content=data.get('content'), priority=data.get('priority', 'Medium'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@api.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    if 'completed' in data:
        task.completed = data['completed']
    if 'content' in data:
        task.content = data['content']
    if 'priority' in data:
        task.priority = data['priority']
    db.session.commit()
    return jsonify(task.to_dict())

@api.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Notes Routes
@api.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@api.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    new_note = Note(title=data.get('title', 'Untitled'), content=data.get('content', ''))
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201

@api.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.json
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    db.session.commit()
    return jsonify(note.to_dict())

@api.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return '', 204
