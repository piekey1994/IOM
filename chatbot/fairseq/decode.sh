model='en.rl'
CUDA_VISIBLE_DEVICES=1 python generate.py data-bin/$model \
    --path checkpoints/$model/checkpoint_best.pt \
    --batch-size 128 --beam 1 --remove-bpe >> $model
grep ^H $model | cut -f3- > $model.output
grep ^T $model | cut -f2- > $model.value

# python generate.py data-bin/twitter.high \
#     --path checkpoints/twitter.high/checkpoint_best.pt \
#     --batch-size 128 --beam 1 --remove-bpe >> twitter.high.output
# grep ^H twitter.high.output | cut -f3- > twitter.high.out.sys
# grep ^T twitter.high.output | cut -f2- > twitter.high.out.ref