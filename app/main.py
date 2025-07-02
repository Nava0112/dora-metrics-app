from flask import Flask, request, jsonify
from github_api import GitHubApp
from metrics import calculate_dora_metrics
from grafana import push_to_grafana
import os

app = Flask(__name__)

# Initialize GitHub App
github_app = GitHubApp(
    app_id=os.getenv("GITHUB_APP_ID"),
    private_key_path=os.getenv("GITHUB_PRIVATE_KEY_PATH"),
    installation_id=os.getenv("GITHUB_INSTALLATION_ID")
)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if event == 'pull_request' and payload['action'] == 'closed':
        repo_name = payload['repository']['full_name']
        metrics = calculate_dora_metrics(github_app, repo_name)
        push_to_grafana(metrics)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)