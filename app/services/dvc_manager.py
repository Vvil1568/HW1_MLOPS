import os
import subprocess
from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)


class DVCManager:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)
        self._init_dvc()

    def _init_dvc(self):
        if not os.path.exists(os.path.join(self.data_dir, ".dvc")):
            logger.info("Initializing DVC...")
            subprocess.run(["git", "init"], cwd=self.data_dir)
            subprocess.run(["dvc", "init"], cwd=self.data_dir)
            cmd = ["dvc", "remote", "add", "-d", "minio", f"s3://{settings.S3_BUCKET_NAME}/dvc"]
            subprocess.run(cmd, cwd=self.data_dir)
            subprocess.run(["dvc", "remote", "modify", "minio", "endpointurl", settings.AWS_ENDPOINT_URL],
                           cwd=self.data_dir)
            subprocess.run(["dvc", "remote", "modify", "minio", "access_key_id", settings.AWS_ACCESS_KEY_ID],
                           cwd=self.data_dir)
            subprocess.run(["dvc", "remote", "modify", "minio", "secret_access_key", settings.AWS_SECRET_ACCESS_KEY],
                           cwd=self.data_dir)
            subprocess.run(["dvc", "remote", "modify", "minio", "ssl_verify", "false"], cwd=self.data_dir)
            subprocess.run(["git", "commit", "-m", "Initialize DVC"], cwd=self.data_dir)

    def add_and_push(self, filename: str, content: bytes = None):
        if content:
            file_path = os.path.join(self.data_dir, filename)
            with open(file_path, "wb") as f:
                f.write(content)

        logger.info(f"DVC adding {filename}")
        subprocess.run(["dvc", "add", filename], cwd=self.data_dir)
        subprocess.run(["dvc", "push"], cwd=self.data_dir)
        subprocess.run(["git", "add", f"{filename}.dvc"], cwd=self.data_dir)
        subprocess.run(["git", "commit", "-m", f"Add {filename}"], cwd=self.data_dir)

    def list_files(self):
        return [f.replace(".dvc", "") for f in os.listdir(self.data_dir) if f.endswith(".dvc")]