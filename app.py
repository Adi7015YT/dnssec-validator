from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_dnssec():
    data = request.json
    domain = data.get('domain')

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    try:
        # Execute the dig command to get DNSSEC trace data
        result = subprocess.run(['dig', '@localhost', 'DS', domain, '+trace'], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': 'Failed to query DNSSEC data'}), 500

        # Parse the dig command output
        trace_data = parse_dig_output(result.stdout)
        return jsonify(trace_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_dig_output(output):
    # Example function to parse dig output and convert it to a JSON structure
    # Implement the parsing logic according to the dig output format
    trace_data = []
    # Parse the output line by line
    lines = output.split('\n')
    for line in lines:
        if line.startswith(';'):
            continue
        # Extract relevant DNSSEC data from each line
        # For simplicity, assume the data is in a specific format (modify as needed)
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
    app.run(debug=True)
