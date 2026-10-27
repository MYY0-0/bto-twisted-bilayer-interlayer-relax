#!/bin/bash
export CUDA_VISIBLE_DEVICES=3
nohup lmp -in in.txt 1>run.log 2>err&