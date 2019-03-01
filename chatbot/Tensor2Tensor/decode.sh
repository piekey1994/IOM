t2t-decoder --t2t_usr_dir=problem \
--problem=chatbot_problem \
--data_dir=./self_data \
--model=transformer \
--hparams_set=transformer_base \
--output_dir=./train \
--decode_hparams="beam_size=1,alpha=0.6" \
--decode_from_file=rawdata/Twitter.100w.test.key \
--decode_to_file=decoder/Twitter.100w.test.output