import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation

def stock_analysis(name):

    #name = "LG전자"
    naming = "{name}.csv".format(name=name)
    data = pd.read_csv(naming,  engine='python')
    data.head()
    high_prices = data['고가'].values
    low_prices = data['저가'].values
    mid_prices = (high_prices + low_prices) / 2
    seq_len = 50
    sequence_length = seq_len + 1
    result = []
    for index in range(len(mid_prices) - sequence_length):
        result.append(mid_prices[index: index + sequence_length])
    

    
    normalized_data = []
    for window in result:
        normalized_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalized_data.append(normalized_window)
        
    result = np.array(normalized_data)
    
    # split train and test data
    row = int(round(result.shape[0] * 0.9))
    train = result[:row, :]
    np.random.shuffle(train)
    
    x_train = train[:, :-1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_train = train[:, -1]
    
    x_test = result[row:, :-1]
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = result[row:, -1]
    
    x_train.shape, x_test.shape


    model = Sequential() 
    model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='rmsprop')
    model.summary()


    model.fit(x_train, y_train,
        validation_data=(x_test, y_test),
        batch_size=10,
        epochs=20)



    pred = model.predict(x_test)

    fig = plt.figure(facecolor='white', figsize=(20, 10))
    ax = fig.add_subplot(111)
    ax.plot(y_test, label='True')
    ax.plot(pred, label='Prediction')
    ax.legend()
    img_name = "{name}.png".format(name=name)
    plt.savefig(img_name, dpi=350)
    
    plt.show()
    
    
stock_analysis("LG전자")

