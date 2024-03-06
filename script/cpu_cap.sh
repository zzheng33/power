#!/bin/bash

echo 50000000 | sudo tee /sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw
echo 50000000 | sudo tee /sys/class/powercap/intel-rapl:1/constraint_0_power_limit_uw

echo 50000000 | sudo tee /sys/class/powercap/intel-rapl:0/constraint_1_power_limit_uw
echo 50000000 | sudo tee /sys/class/powercap/intel-rapl:1/constraint_1_power_limit_uw