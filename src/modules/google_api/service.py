import io
import os

from googleapiclient.http import MediaIoBaseDownload

from .client import DriveClient


class DriveService:
    def __init__(self, client: DriveClient):
        self.service = client.get_service()

    def _q(self, value: str) -> str:
        return value.replace("'", "\\'")

    def find_folder_id_by_path(self, path: str, parent_id="root") -> str:
        """Resolves a path (e.g., 'Folder/Subfolder') to a File ID."""
        parts = [p for p in path.strip("/").split("/") if p]
        current_parent = parent_id

        for i, folder_name in enumerate(parts):
            # Buscar en el padre actual
            q = (
                f"name = '{self._q(folder_name)}' "
                f"and mimeType = 'application/vnd.google-apps.folder' "
                f"and '{current_parent}' in parents and trashed = false"
            )
            response = self.service.files().list(q=q, pageSize=1, fields="files(id, name)").execute()
            files = response.get("files", [])

            # Si no se encuentra y estamos buscando el primer elemento en 'root', buscar en 'Shared with me' o global
            if not files and i == 0 and parent_id == 'root':
                print(f"Carpeta '{folder_name}' no encontrada en root. Buscando globalmente...")
                q_global = (
                     f"name = '{self._q(folder_name)}' "
                     f"and mimeType = 'application/vnd.google-apps.folder' "
                     f"and trashed = false"
                )
                response = self.service.files().list(q=q_global, pageSize=1, fields="files(id, name)").execute()
                files = response.get("files", [])

            if not files:
                raise FileNotFoundError(f"Folder '{folder_name}' not found under parent {current_parent}")
            
            current_parent = files[0]["id"]

        return current_parent

    def list_folders_in_folder(self, folder_id):
        """Lists subfolders within a given folder ID."""
        q = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        response = self.service.files().list(q=q, fields="files(id, name)").execute()
        return response.get("files", [])

    def download_folder(self, folder_id, local_destination):
        """Recursively downloads a folder from Drive to a local path."""
        # Create local folder
        if not os.path.exists(local_destination):
            os.makedirs(local_destination)

        # List contents
        q = f"'{folder_id}' in parents and trashed = false"
        response = self.service.files().list(q=q, fields="files(id, name, mimeType)").execute()

        files = response.get("files", [])
        for item in files:
            file_id = item["id"]
            name = item["name"]
            mime_type = item["mimeType"]
            local_path = os.path.join(local_destination, name)

            if mime_type == "application/vnd.google-apps.folder":
                self.download_folder(file_id, local_path)
            elif not mime_type.startswith("application/vnd.google-apps."):  # Skip Google Docs/Sheets
                self._download_file(file_id, local_path)

    def _download_file(self, file_id, local_path):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(local_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

    def move_file(self, file_id, new_parent_id):
        """Moves a file or folder to a new parent folder."""
        file = self.service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))

        self.service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=previous_parents,
            fields="id, parents",
        ).execute()
