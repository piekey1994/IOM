# coding=utf-8
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry

@registry.register_problem
class ChatbotProblem(text_problems.Text2TextProblem):
  """Predict next line of poetry from the last line. From Gutenberg texts."""

  @property
  def approx_vocab_size(self):
    return 2**15  # ~64k

  @property
  def is_generate_per_split(self):
    # generate_data will shard the data into TRAIN and EVAL for us.
    return False

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 9,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    del data_dir
    del tmp_dir
    del dataset_split


    q_r = open("./rawdata/Twitter.100w.train.key", "r")
    a_r = open("./rawdata/Twitter.100w.train.value", "r")

    comment_list = q_r.readlines()
    tag_list = a_r.readlines()
    q_r.close()
    a_r.close()
    for comment, tag in zip(comment_list, tag_list):
        comment = comment.strip()
        tag = tag.strip()
        yield {
            "inputs": comment,
            "targets": tag
        }