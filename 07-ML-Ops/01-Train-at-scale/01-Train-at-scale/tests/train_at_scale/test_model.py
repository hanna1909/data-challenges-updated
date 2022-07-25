import pytest
import numpy as np
import os

TEST_ENV = os.getenv("TEST_ENV")


@pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
def test_model_architecture_and_fit(X_processed_1k, y_1k):

    from taxifare_model.ml_logic.model import initialize_model,compile_model, train_model

    model = initialize_model(X_processed_1k)
    trainable_params = np.sum([np.prod(v.get_shape()) for v in model.trainable_weights])

    expected = 12621
    assert trainable_params == expected

    model = compile_model(model, learning_rate=0.001)

    model, history = train_model(model=model,
                                 X=X_processed_1k,
                                 y=y_1k,
                                 batch_size=256,
                                 validation_split=0.3)

    assert min(history.history['loss']) < 220
