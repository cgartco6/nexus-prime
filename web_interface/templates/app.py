from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nexus_core import NexusCore

app = Flask(__name__)
nexus = NexusCore()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'GET':
        projects = nexus.state_manager.list_projects()
        return jsonify(projects)
    else:
        data = request.json
        project_id = nexus.create_project(data['command'])
        return jsonify({"project_id": project_id})

@app.route('/api/projects/<project_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_project(project_id):
    if request.method == 'GET':
        if nexus.load_project(project_id):
            status = nexus.get_project_status()
            return jsonify(status)
        return jsonify({"error": "Project not found"}), 404
        
    elif request.method == 'PUT':
        result = nexus.execute_next_task()
        return jsonify(result)
        
    elif request.method == 'DELETE':
        success = nexus.state_manager.delete_project(project_id)
        return jsonify({"success": success})

@app.route('/api/projects/<project_id>/artifacts')
def get_project_artifacts(project_id):
    if nexus.load_project(project_id):
        return jsonify(nexus.workspace_state)
    return jsonify({"error": "Project not found"}), 404

@app.route('/workspace/<path:filename>')
def serve_workspace_file(filename):
    return send_from_directory('../workspace', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
