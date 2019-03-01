model='en.rm'
CUDA_VISIBLE_DEVICES=4 python train.py data-bin/$model \
    --lr 0.25 --clip-norm 0.1 --dropout 0.2 --max-tokens 3500 \
    --arch fconv --fp16 --save-dir checkpoints/$model