import subprocess

def start_docker_training():
    # Docker image details
    docker_image = "bert"
    
    # Define local and container directories
    local_dir = "/home/cc/benchmark/ECP/bert-large"
    container_dir = "/workspace"
    
    # Define the training command with all arguments
    training_command = (
        "TF_XLA_FLAGS='--tf_xla_auto_jit=2' python3 /workspace/run_pretraining.py "
        "--bert_config_file=/workspace/input_files/bert_config.json "
        "--output_dir=/tmp/output/ "
        "--input_file=/workspace/6000_samples "
        "--do_train=True "
        "--iterations_per_loop=1000 "
        "--learning_rate=0.0001 "
        "--max_eval_steps=1250 "
        "--max_predictions_per_seq=76 "
        "--max_seq_length=512 "
        "--num_gpus=1 "
        "--num_train_steps=750 "
        "--num_warmup_steps=1562 "
        "--optimizer=lamb "
        "--save_checkpoints_steps=156200000 "
        "--start_warmup_step=0 "
        "--train_batch_size=8 "
        "--nouse_tpu"
    )
    
    # Docker command to run the training without an interactive or bash session
    command = [
        "sudo", "docker", "run", "--gpus", "all", "--rm",
        "-v", f"{local_dir}:{container_dir}",
        docker_image,
        "bash", "-c", training_command
    ]
    
    # Run the Docker container and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Training completed successfully!")
        print(result.stdout)
    else:
        print("Error in training:")
        print(result.stderr)

if __name__ == "__main__":
    start_docker_training()
