import os
from pathlib import Path
import tarfile
import json

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds


def package_model(model_directory: Path, model_output_archive: Path):
    print(f"Packaging the model artifacts into => {model_output_archive}")
    with tarfile.open(model_output_archive, "w:gz") as tar:
        tar.add(model_directory, arcname=os.path.basename(model_directory))


def train_and_save(model_export_path: Path):
    # Prepare data
    # Split the training set into 60% and 40% to end up with 15,000 examples
    # for training, 10,000 examples for validation and 25,000 examples for testing.
    train_data, validation_data, test_data = tfds.load(
        name="imdb_reviews", 
        split=('train[:60%]', 'train[60%:]', 'test'),
        as_supervised=True)

    # Prepare model
    embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
    hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy'])

    # Parameters
    parameters = dict({
        "epochs": 5,
        "batch_size": 512
    })
    with open('parameters.json', 'w') as fp:
        json.dump(parameters, fp)

    # Train
    model.fit(
        train_data.shuffle(10000).batch(parameters['batch_size']),
        epochs=parameters['epochs'],
        validation_data=validation_data.batch(parameters['batch_size']),
        verbose=1)

    # Evaluate
    metrics_dict = dict()
    results = model.evaluate(test_data.batch(parameters['batch_size']), verbose=2)
    for name, value in zip(model.metrics_names, results):
        print("%s: %.3f" % (name, value))
        metrics_dict[f"test_{name}"] = value
    # Export metrics to file
    with open('metrics.json', 'w') as fp:
        json.dump(metrics_dict, fp)    

    for sample in ["absolutely the best", "total crap, nightmare and misunderstanding"]:
        print(f"{sample} => {model.predict([sample])}")

    # Serialize model
    tf.keras.models.save_model(
        model,
        model_export_path,
        overwrite=True,
        include_optimizer=False,
        save_format=None,
        signatures=None,
        options=None
    )


if __name__ == "__main__":
    train_and_save(model_export_path=os.environ['MODEL_EXPORT_DIRECTORY'])
    package_model(
        model_directory=os.environ['MODEL_EXPORT_DIRECTORY'],
        model_output_archive=os.environ['MODEL_ARCHIVE_OUTPUT_PATH'])
