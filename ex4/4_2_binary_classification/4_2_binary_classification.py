import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
import pandas as pd
from scipy.io import arff


def train_svm(train_dataset):
    cols = train_dataset.columns.values
    x = train_dataset[cols[:-1]].to_numpy()
    y = train_dataset[cols[-1]].to_numpy()
    y = [i[0] for i in y]
    # gamma = 2 since: gamma = 1/(2*sigma^2)
    return SVR(kernel="rbf", C=1, gamma=2).fit(x, y)


def train_log_reg(train_dataset):
    cols = train_dataset.columns.values
    x = train_dataset[cols[:-1]].to_numpy()
    y = train_dataset[cols[-1]].to_numpy()
    y = [i[0] for i in y]
    return LogisticRegression().fit(x, y)


def model_predict(model, predict_dataset, printing=True):
    cols = predict_dataset.columns.values
    x = predict_dataset[cols[:-1]].to_numpy()
    prediction = model.predict(x)
    if printing:
        for p in prediction:
            print(chr(int(p)))
    return prediction


def save_error_values(model, train_dataset, predict_dataset):
    train_res = model_predict(model, train_dataset, printing=False)
    pred_res = model_predict(model, predict_dataset, printing=False)

    train_actual = actual_values(train_dataset)
    pred_actual = actual_values(predict_dataset)

    train_wrong = 0
    pred_wrong = 0

    for a, p in zip(train_actual, train_res):
        if a != int(p):
            train_wrong += 1

    for a, p in zip(pred_actual, pred_res):
        if a != int(p):
            pred_wrong += 1

    print("train error:", str(train_wrong*100/len(train_actual))+"%")
    print("prediction error:", str(pred_wrong * 100 / len(pred_actual)) + "%")


def actual_values(dataset):
    cols = dataset.columns.values
    return [i[0] for i in dataset[cols[-1]].to_numpy()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser('FSA')
    parser.add_argument('--type', type=str, help='which kind of regression', choices=["Logistic-regression", "support-vector-machine"])
    parser.add_argument('--output-error-values', action='store_true', default=False, help='display error values instead of output')

    parser.add_argument('--train', type=str, help='training dataset', default='MC2-train.arff')
    parser.add_argument('--predict', type=str, help='prediction dataset', default='MC2-predict.arff')
    args = parser.parse_args()

    train_data_arff = arff.loadarff(args.train)
    train_data = pd.DataFrame(train_data_arff[0])
    train_data = train_data.fillna(0)

    prediction_data = pd.DataFrame(arff.loadarff(args.predict)[0])
    prediction_data = prediction_data.fillna(0)

    if args.type == "Logistic-regression":
        model = train_log_reg(train_data)
    else:
        model = train_svm(train_data)

    if args.output_error_values:
        print(args.type, "error report")
        save_error_values(model, train_data, prediction_data)
    else:
        model_predict(model, prediction_data)

