import os
import subprocess
from multiprocessing import Pool
import torch  # For detecting GPU resources

# Configuration
ALPHAFOLD_SCRIPT = "/path/to/run_alphafold.sh"  # AlphaFold execution script
INPUT_FASTA_DIR = "/path/to/fasta_inputs"  # Directory containing FASTA files
OUTPUT_DIR = "/path/to/alphafold_outputs"  # Directory for storing results
MODEL_PRESET = "multimer"  # Use AlphaFold-Multimer for protein-nucleic acid interactions
NUM_GPUS = torch.cuda.device_count()  # Detect available GPUs

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all FASTA files
fasta_files = [f for f in os.listdir(INPUT_FASTA_DIR) if f.endswith(".fasta")]

def run_alphafold(fasta_file, gpu_id):
    """ Runs AlphaFold on a single FASTA file using a specified GPU """
    fasta_path = os.path.join(INPUT_FASTA_DIR, fasta_file)
    output_path = os.path.join(OUTPUT_DIR, os.path.splitext(fasta_file)[0])

    # Check if prediction is already done
    if os.path.exists(os.path.join(output_path, "ranked_0.pdb")):
        print(f"Skipping {fasta_file}, already completed.")
        return

    print(f"Processing {fasta_file} on GPU {gpu_id}...")

    # Assign GPU dynamically
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # AlphaFold command
    cmd = f"{ALPHAFOLD_SCRIPT} --fasta_path={fasta_path} --output_dir={output_path} --model_preset={MODEL_PRESET}"
    subprocess.run(cmd, shell=True, env=env)

    print(f"Finished {fasta_file} on GPU {gpu_id}.")

# Parallel processing using GPUs
with Pool(NUM_GPUS) as p:
    p.starmap(run_alphafold, [(fasta_files[i], i % NUM_GPUS) for i in range(len(fasta_files))])

print("All predictions completed!")
