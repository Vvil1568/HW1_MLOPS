import os
import subprocess
import sys

def generate():
    """Generates gRPC code from proto file."""
    subprocess.check_call([
        sys.executable, "-m", "grpc_tools.protoc",
        "-I.",
        "--python_out=.",
        "--grpc_python_out=.",
        "proto/service.proto"
    ])
    print("Proto files generated.")

if __name__ == "__main__":
    generate()