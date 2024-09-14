import os
import subprocess
import requests
from tqdm.notebook import tqdm

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            progress_bar.update(size)

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

print("Starting ComfyUI setup...")

# Update or clone ComfyUI
comfyui_path = '/workspace/ComfyUI'

# Create necessary directories
directories = [
    '/workspace/ComfyUI/custom_nodes',
    '/workspace/ComfyUI/models/unet',
    '/workspace/ComfyUI/models/upscale_models',
    '/workspace/ComfyUI/models/clip',
    '/workspace/ComfyUI/models/vae',
    '/workspace/ComfyUI/models/loras'
]
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Clone repositories to custom_nodes
custom_nodes_repos = [
    "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git",
    "https://github.com/city96/ComfyUI-GGUF.git",
    "https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git",
    "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git",
    "https://github.com/rgthree/rgthree-comfy.git",
    "https://github.com/giriss/comfy-image-saver.git",
    "https://github.com/Acly/comfyui-tooling-nodes.git",
    "https://github.com/spacepxl/ComfyUI-Florence-2.git",
    "https://github.com/kijai/ComfyUI-KJNodes.git",
    "https://github.com/kijai/ComfyUI-Florence2.git",
    "https://github.com/kijai/ComfyUI-segment-anything-2.git",
    "https://github.com/yolain/ComfyUI-Easy-Use.git",
    "https://github.com/KoreTeknology/ComfyUI-Universal-Styler.git",
    "https://github.com/un-seen/comfyui-tensorops.git",
    "https://github.com/Xclbr7/ComfyUI-Merlin.git",
    "https://github.com/digitaljohn/comfyui-propost.git",
    "https://github.com/BlenderNeko/ComfyUI_Noise.git",
    "https://github.com/WASasquatch/was-node-suite-comfyui.git",
    "https://github.com/Clybius/ComfyUI-Latent-Modifiers.git",
    "https://github.com/chrisgoringe/cg-use-everywhere.git",
    "https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git",
    "https://github.com/city96/ComfyUI-GGUF.git",
]

print("\nCloning custom node repositories...")
for repo in custom_nodes_repos:
    repo_name = repo.split('/')[-1].replace('.git', '')
    command = f'git clone {repo} /workspace/ComfyUI/custom_nodes/{repo_name}'
    run_command(command)

# Download files only if they don't exist
files_to_download = {
    '/workspace/ComfyUI/models/unet/flux1-dev-Q6_K.gguf': 'https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q6_K.gguf',
    '/workspace/ComfyUI/models/upscale_models/4x-UltraSharp.pth': 'https://civitai.com/api/download/models/125843?type=Model&format=PickleTensor',
    '/workspace/ComfyUI/models/clip/t5-v1_1-xxl-encoder-Q6_K.gguf': 'https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q6_K.gguf',
    '/workspace/ComfyUI/models/clip/clip_l.safetensors': 'https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors',
    '/workspace/ComfyUI/models/vae/ae.safetensors': 'https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors',
    '/workspace/ComfyUI/models/loras/Boreal_Lora.safetensors': 'https://civitai.com/api/download/models/715729?type=Model&format=SafeTensor',
    '/workspace/ComfyUI/models/loras/flux-RealismLora.safetensors': 'https://huggingface.co/XLabs-AI/flux-RealismLora/resolve/main/lora.safetensors'
}

print("\nChecking and downloading model files...")
for filename, url in files_to_download.items():
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        download_file(url, filename)
    else:
        print(f"{filename} already exists. Skipping download.")

print("\nSetup completed successfully!")
