import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class DriveClient:
    def __init__(self, credentials_path, token_path, scopes):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
            except Exception as e:
                logging.error(f"Error loading token: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    logging.info("Token expired and refresh failed, re-authenticating")
                    creds = self._new_auth()
            else:
                creds = self._new_auth()

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def _new_auth(self):
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")

        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.scopes)
        return flow.run_local_server(port=0)

    def get_service(self):
        return self.service
