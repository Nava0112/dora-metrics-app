from github import Github
import jwt
import time
import requests

class GitHubApp:
    def __init__(self, app_id, private_key_path, installation_id):
        self.app_id = app_id
        self.private_key = open(private_key_path, 'r').read()
        self.installation_id = installation_id
        self.access_token = self._get_access_token()
        self.github = Github(self.access_token)
    
    def _get_access_token(self):
        # Generate JWT
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,
            'iss': self.app_id
        }
        jwt_token = jwt.encode(payload, self.private_key, algorithm='RS256')
        
        # Get installation token
        headers = {'Authorization': f'Bearer {jwt_token}', 'Accept': 'application/vnd.github.v3+json'}
        url = f'https://api.github.com/app/installations/{self.installation_id}/access_tokens'
        response = requests.post(url, headers=headers)
        return response.json()['token']