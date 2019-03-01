model='en.rh'
TEXT=examples/translation/$model.key-value
python preprocess.py --source-lang key --target-lang value \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test \
    --destdir data-bin/$model