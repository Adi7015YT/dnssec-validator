from flask import Flask, request, jsonify, render_template
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the home page with a form to input resolver details.
    """
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_dnssec():
    data = request.json
    domain = data.get('domain')
    resolver = data.get('resolver', '34.27.111.125')  # Default resolver if not provided

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    try:
        # Execute the dig command to get DNSSEC trace data
        result = subprocess.run(['dig', f'@{resolver}', 'DS', domain, '+trace'], 
                                capture_output=True, text=True)
        
        # Log the full command output for debugging purposes
        app.logger.debug(f'dig stdout: {result.stdout}')
        app.logger.debug(f'dig stderr: {result.stderr}')
        
        if result.returncode != 0:
            return jsonify({'error': 'Failed to query DNSSEC data', 'details': result.stderr}), 500

        # Parse the dig command output
        trace_data = parse_dig_output(result.stdout)
        return jsonify(trace_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_dig_output(output):
    """
    Parse the dig command output and extract DNSSEC-related information.
    """
    trace_data = []
    lines = output.split('\n')
    for line in lines:
        if line.startswith(';'):
            continue
        
        parts = line.split()
        if len(parts) > 4 and parts[3] in ['DS', 'DNSKEY', 'RRSIG']:
            record = {
                'level': len(trace_data),
                'qname': parts[0],
                'type': parts[3],
                'data': ' '.join(parts[4:])
            }
            trace_data.append(record)
    return trace_data

if __name__ == '__main__':
<<<<<<< HEAD:dnssec/app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
    app.run(debug=True)
>>>>>>> fa3ce8052ab134038908a4849f9a74b55a9dcf70:app.py
