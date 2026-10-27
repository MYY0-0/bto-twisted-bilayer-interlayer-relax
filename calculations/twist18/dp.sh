#!/bin/bash
export CUDA_VISIBLE_DEVICES=2
nohup lmp -in in.txt 1>run.log 2>err&
