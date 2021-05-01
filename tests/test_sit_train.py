import json
import os
import tempfile
from unittest import TestCase

import numpy as np

from inference.main_batch_predict import BatchPredict
from main_train_pipeline import TrainPipeline


class TestSitTrain(TestCase):

    def test_train_with_no_exception_aimed(self):
        # Arrange
        train_data_file = os.path.join(os.path.dirname(__file__), "sample_data", "train_data", "aimed.json")
        batch = 3

        # Bert Config
        vocab_size = 20000
        sequence_len = 20
        num_classes = 2

        bert_config = {"vocab_size": vocab_size, "hidden_size": 10, "num_hidden_layers": 1,
                       "tokenisor_max_seq_len": sequence_len, "num_labels": num_classes,
                       "num_attention_heads": 1}

        # Additional args
        dataset_factory = "datasets.aimed_dataset_factory.AimedDatasetFactory"
        model_factory = "models.bert_model_factory.BertModelFactory"
        tokenisor_data_dir = os.path.join(os.path.dirname(__file__), "sample_data", "tokensior_data")
        additional_args = {"model_config": json.dumps(bert_config),
                           "tokenisor_data_dir": tokenisor_data_dir,
                           "datasetfactory": dataset_factory,
                           "modelfactory": model_factory,
                           "batch": batch,
                           "numworkers": 1,
                           "epochs": 2,
                           "earlystoppingpatience": 1
                           }

        # Act
        self._run_train(train_data_file, additional_args)

    def test_train_with_no_exception_ppi_multiclass(self):
        # Arrange
        train_data_file = os.path.join(os.path.dirname(__file__), "sample_data", "train_data_ppi_multiclass")
        dataset_factory = "datasets.ppi_multiclass_dataset_factory.PpiMulticlassDatasetFactory"
        model_factory = "models.bert_model_factory.BertModelFactory"

        batch = 3

        # Bert Config
        vocab_size = 20000
        sequence_len = 20
        num_classes = 7

        bert_config = {"vocab_size": vocab_size, "hidden_size": 10, "num_hidden_layers": 1,
                       "tokenisor_max_seq_len": sequence_len, "num_labels": num_classes,
                       "num_attention_heads": 1}

        # Additional args
        tokenisor_data_dir = os.path.join(os.path.dirname(__file__), "sample_data", "tokensior_data")
        additional_args = {"model_config": json.dumps(bert_config),
                           "tokenisor_data_dir": tokenisor_data_dir,
                           "datasetfactory": dataset_factory,
                           "modelfactory": model_factory,
                           "batch": batch,
                           "numworkers": 1,
                           "epochs": 2,
                           "earlystoppingpatience": 1
                           }

        self._run_train(train_data_file, additional_args)

    def test_predict_with_no_exception_ppi_multiclass(self):
        # Arrange
        train_data_file = os.path.join(os.path.dirname(__file__), "sample_data", "train_data_ppi_multiclass")
        dataset_factory = "datasets.ppi_multiclass_dataset_factory.PpiMulticlassDatasetFactory"
        model_factory = "models.bert_model_factory.BertModelFactory"

        batch = 3

        # Bert Config
        vocab_size = 20000
        sequence_len = 20
        num_classes = 7

        bert_config = {"vocab_size": vocab_size, "hidden_size": 10, "num_hidden_layers": 1,
                       "tokenisor_max_seq_len": sequence_len, "num_labels": num_classes,
                       "num_attention_heads": 1}

        # Additional args
        tokenisor_data_dir = os.path.join(os.path.dirname(__file__), "sample_data", "tokensior_data")
        additional_args = {"model_config": json.dumps(bert_config),
                           "tokenisor_data_dir": tokenisor_data_dir,
                           "datasetfactory": dataset_factory,
                           "modelfactory": model_factory,
                           "batch": batch,
                           "numworkers": 1,
                           "epochs": 2,
                           "earlystoppingpatience": 1
                           }
        tempdir_model = tempfile.mkdtemp()
        tempdir_output = tempfile.mkdtemp()

        conf_scores = self._run_train(train_data_file, additional_args, tempdir_model=tempdir_model)[-1]["result"][
            "conf"]

        # Act
        prediction, confidence_scores = BatchPredict().predict_from_file(train_data_file, tempdir_model, tempdir_output,
                                                                         is_ensemble=False)

        # Assert
        np.testing.assert_array_almost_equal(conf_scores, confidence_scores)

    def _run_train(self, train_data_file, additional_args, tempdir_model=None, tempdir_checkpoint=None):
        tempdir_model = tempdir_model or tempfile.mkdtemp()
        tempdir_checkpoint = tempdir_checkpoint or tempfile.mkdtemp()
        tempdir_out = tempfile.mkdtemp()

        # Runs
        return TrainPipeline().run_train_k_fold(train_data_file,
                                                train_data_file,
                                                kfold_trainprefix=None,
                                                checkpoint_dir=tempdir_checkpoint,
                                                model_dir=tempdir_model,
                                                output_dir=tempdir_out,
                                                additional_args=additional_args
                                                )
