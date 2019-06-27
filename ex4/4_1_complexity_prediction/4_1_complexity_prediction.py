import argparse
from sklearn.linear_model import LinearRegression
import pandas as pd


def train_model(train_dataset, train_columns, predict_columns):
    data = pd.read_csv(train_dataset, sep=";")
    data = data.fillna(0)
    X = data[train_columns.split(";")]
    Y = data[predict_columns.split(";")]
    return LinearRegression().fit(X.to_numpy(), Y.to_numpy())


def model_predict(model, predict_dataset, train_columns):
    data = pd.read_csv(predict_dataset, sep=";")
    files = data[["filename"]].to_numpy()
    prediction_data = data[train_columns.split(";")]
    prediction = model.predict(prediction_data.to_numpy())
    for f, p in zip(files, prediction):
        print(str(f[0]) + ";" + str(p[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser('FSA')
    parser.add_argument('--training-columns', type=str, help='columns that should be used for training')
    parser.add_argument('--prediction-column', type=str, help='columns that should be predicted')

    parser.add_argument('--train', type=str, help='training dataset', default='training-data.csv')
    parser.add_argument('--predict', type=str, help='prediction dataset', default='prediction-data.csv')
    args = parser.parse_args()

    model = train_model(args.train, args.training_columns, args.prediction_column)
    model_predict(model, args.predict, args.training_columns)

