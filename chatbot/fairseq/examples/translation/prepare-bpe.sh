#!/usr/bin/env bash
#
# Adapted from https://github.com/facebookresearch/MIXER/blob/master/prepareData.sh

# echo 'Cloning Moses github repository (for tokenization scripts)...'
# git clone https://github.com/moses-smt/mosesdecoder.git

# echo 'Cloning Subword NMT repository (for BPE pre-processing)...'
# git clone https://github.com/rsennrich/subword-nmt.git

SCRIPTS=mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
BPEROOT=subword-nmt
BPE_TOKENS=10000

# URL="https://wit3.fbk.eu/archive/2014-01/texts/de/en/de-en.tgz"
# GZ=de-en.tgz

# if [ ! -d "$SCRIPTS" ]; then
#     echo "Please set SCRIPTS variable correctly to point to Moses scripts."
#     exit
# fi

src=key
tgt=value
lang=key-value
prep=en.rh.key-value #???????
tmp=$prep/tmp
orig=en.rh #???????

mkdir -p $tmp $prep

# echo "Downloading data from ${URL}..."
# cd $orig
# wget "$URL"

# if [ -f $GZ ]; then
#     echo "Data successfully downloaded."
# else
#     echo "Data not successfully downloaded."
#     exit
# fi

# tar zxvf $GZ
# cd ..

echo "pre-processing train data..."
for l in $src $tgt; do
    f=train.tags.$lang.$l
    tok=train.tags.$lang.tok.$l

    cat $orig/$lang/$f | \
    grep -v '<url>' | \
    grep -v '<talkid>' | \
    grep -v '<keywords>' | \
    sed -e 's/<title>//g' | \
    sed -e 's/<\/title>//g' | \
    sed -e 's/<description>//g' | \
    sed -e 's/<\/description>//g' | \
    perl $TOKENIZER -threads 8 -l $l > $tmp/$tok
    echo ""
done
perl $CLEAN -ratio 1.5 $tmp/train.tags.$lang.tok $src $tgt $tmp/train.tags.$lang.clean 1 175
for l in $src $tgt; do
    perl $LC < $tmp/train.tags.$lang.clean.$l > $tmp/train.tags.$lang.$l
done

echo "pre-processing dev data..."
for l in $src $tgt; do
    f=dev.tags.$lang.$l
    tok=dev.tags.$lang.tok.$l

    cat $orig/$lang/$f | \
    grep -v '<url>' | \
    grep -v '<talkid>' | \
    grep -v '<keywords>' | \
    sed -e 's/<title>//g' | \
    sed -e 's/<\/title>//g' | \
    sed -e 's/<description>//g' | \
    sed -e 's/<\/description>//g' | \
    perl $TOKENIZER -threads 8 -l $l > $tmp/$tok
    echo ""
done
perl $CLEAN -ratio 1.5 $tmp/dev.tags.$lang.tok $src $tgt $tmp/dev.tags.$lang.clean 1 175
for l in $src $tgt; do
    perl $LC < $tmp/dev.tags.$lang.clean.$l > $tmp/dev.tags.$lang.$l
done

echo "pre-processing test data..."
for l in $src $tgt; do
    f=test.tags.$lang.$l
    tok=test.tags.$lang.tok.$l

    cat $orig/$lang/$f | \
    grep -v '<url>' | \
    grep -v '<talkid>' | \
    grep -v '<keywords>' | \
    sed -e 's/<title>//g' | \
    sed -e 's/<\/title>//g' | \
    sed -e 's/<description>//g' | \
    sed -e 's/<\/description>//g' | \
    perl $TOKENIZER -threads 8 -l $l > $tmp/$tok
    echo ""
done
perl $CLEAN -ratio 1.5 $tmp/test.tags.$lang.tok $src $tgt $tmp/test.tags.$lang.clean 1 175
for l in $src $tgt; do
    perl $LC < $tmp/test.tags.$lang.clean.$l > $tmp/test.tags.$lang.$l
done

# echo "pre-processing valid/test data..."
# for l in $src $tgt; do
#     for o in `ls $orig/$lang/IWSLT14.TED*.$l.xml`; do
#     fname=${o##*/}
#     f=$tmp/${fname%.*}
#     echo $o $f
#     grep '<seg id' $o | \
#         sed -e 's/<seg id="[0-9]*">\s*//g' | \
#         sed -e 's/\s*<\/seg>\s*//g' | \
#         sed -e "s/\’/\'/g" | \
#     perl $TOKENIZER -threads 8 -l $l | \
#     perl $LC > $f
#     echo ""
#     done
# done


echo "creating train, valid, test..."
for l in $src $tgt; do
    mv  $tmp/dev.tags.$lang.$l  $tmp/valid.$l
    mv  $tmp/train.tags.$lang.$l  $tmp/train.$l
    mv  $tmp/test.tags.$lang.$l  $tmp/test.$l
    # cat $tmp/IWSLT14.TED.dev2010.de-en.$l \
    #     $tmp/IWSLT14.TEDX.dev2012.de-en.$l \
    #     $tmp/IWSLT14.TED.tst2010.de-en.$l \
    #     $tmp/IWSLT14.TED.tst2011.de-en.$l \
    #     $tmp/IWSLT14.TED.tst2012.de-en.$l \
    #     > $tmp/test.$l
done

TRAIN=$tmp/train.value-key
BPE_CODE=$prep/code
rm -f $TRAIN
for l in $src $tgt; do
    cat $tmp/train.$l >> $TRAIN
done

echo "learn_bpe.py on ${TRAIN}..."
python $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

for L in $src $tgt; do
    for f in train.$L valid.$L test.$L; do
        echo "apply_bpe.py to ${f}..."
        python $BPEROOT/apply_bpe.py -c $BPE_CODE < $tmp/$f > $prep/$f
    done
done
