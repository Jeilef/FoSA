import argparse, os
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


# to get the summary both logistic-regression and support-vector-machines have to be run once with the output errors option
def save_error_values(model, train_dataset, predict_dataset, model_type):
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

    type_string = model_type + " error report\n"
    train_error = "train error: " + str(train_wrong*100/len(train_actual)) + "%\n"
    pred_error = "prediction error: " + str(pred_wrong * 100 / len(pred_actual)) + "%"
    output_string = type_string + train_error + pred_error
    with open(model_type + '-error-report.txt', 'w') as error_file:
        error_file.write(output_string)
        print(output_string)
    if os.path.exists('support-vector-machine-error-report.txt') and os.path.exists('logistic-regression-error-report.txt'):
        with open('error-report.txt', 'w') as error_report:
            with open('logistic-regression-error-report.txt') as lr_report:
                error_report.write(lr_report.read())
            error_report.write('\n\n')
            with open('support-vector-machine-error-report.txt') as svm_report:
                error_report.write(svm_report.read())


def actual_values(dataset):
    cols = dataset.columns.values
    return [i[0] for i in dataset[cols[-1]].to_numpy()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser('FSA')
    parser.add_argument('--type', type=str, help='which kind of regression', choices=["logistic-regression", "support-vector-machine"])
    parser.add_argument('--output-error-values', action='store_true', default=False, help='display error values instead of output')

    parser.add_argument('--train', type=str, help='training dataset', default='MC2-train.arff')
    parser.add_argument('--predict', type=str, help='prediction dataset', default='MC2-predict.arff')
    args = parser.parse_args()

    train_data_arff = arff.loadarff(args.train)
    train_data = pd.DataFrame(train_data_arff[0])
    train_data = train_data.fillna(0)

    prediction_data = pd.DataFrame(arff.loadarff(args.predict)[0])
    prediction_data = prediction_data.fillna(0)

    if args.type == "logistic-regression":
        model = train_log_reg(train_data)
    else:
        model = train_svm(train_data)

    if args.output_error_values:
        save_error_values(model, train_data, prediction_data, args.type)
    else:
        model_predict(model, prediction_data)

