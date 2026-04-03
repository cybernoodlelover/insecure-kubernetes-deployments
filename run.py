from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_command():
    payload = request.get_json(silent=True, force=True)
    if not payload or 'cmd' not in payload:
        return jsonify({'error': 'Missing "cmd" in JSON body'}), 400

    cmd = payload['cmd']

    # WARNING: insecure behavior is intentional for this demo repo
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return jsonify({
            'cmd': cmd,
            'returncode': completed.returncode,
            'stdout': completed.stdout,
            'stderr': completed.stderr
        }), (200 if completed.returncode == 0 else 400)
    except subprocess.TimeoutExpired as e:
        return jsonify({'error': 'Command timed out', 'details': str(e)}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'POST to /execute with JSON {"cmd":"..."}'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
