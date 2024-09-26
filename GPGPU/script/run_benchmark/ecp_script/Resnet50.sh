#!/bin/bash

start_docker_training() {
    # Docker image details
 
    # Define the training command with all arguments
    training_command="python3 /workspace/tensorflow2/resnet_ctl_imagenet_main.py \
                    --base_learning_rate=8.5 \
                    --batch_size=128 \
                    --clean \
                    --data_dir=/workspace/tf_records/train \
                    --datasets_num_private_threads=32 \
                    --dtype=fp32 \
                    --device_warmup_steps=1 \
                    --noenable_device_warmup \
                    --enable_eager \
                    --noenable_xla \
                    --epochs_between_evals=4 \
                    --noeval_dataset_cache \
                    --eval_offset_epochs=2 \
                    --eval_prefetch_batchs=192 \
                    --label_smoothing=0.1 \
                    --lars_epsilon=0 \
                    --log_steps=125 \
                    --lr_schedule=polynomial \
                    --model_dir=./model \
                    --momentum=0.9 \
                    --num_accumulation_steps=1 \
                    --num_classes=1000 \
                    --num_gpus=1 \
                    --optimizer=LARS \
                    --noreport_accuracy_metrics \
                    --single_l2_loss_op \
                    --noskip_eval \
                    --steps_per_loop=1252 \
                    --target_accuracy=0.759 \
                    --notf_data_experimental_slack \
                    --tf_gpu_thread_mode=gpu_private \
                    --notrace_warmup \
                    --train_epochs=1 \
                    --notraining_dataset_cache \
                    --training_prefetch_batchs=128 \
                    --nouse_synthetic_data \
                    --warmup_epochs=0 \
                    --weight_decay=0.0002 \
                    --train_steps=100"

    # Docker command to run the training without an interactive or bash session
    sudo docker run --gpus all --rm -v /home/cc/benchmark/ECP/Resnet50:/workspace tensorflow/tensorflow:2.4.0-gpu bash -c "$training_command"

    # Check if the Docker run was successful
    if [ $? -eq 0 ]; then
        echo "Training completed successfully!"
    else
        echo "Error in training."
    fi
}


start_docker_training

