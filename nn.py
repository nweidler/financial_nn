# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.

#
##nerual net code greatly used the following site
##http://iamtrask.github.io/2015/07/12/basic-python-network/
#

#Training column inputs (binary):
#7 inputs for RSI
#RSI < 30, 30 <= RSI <= 70, RSI > 70, RSI > RSI yesterday, RSI < RSI yesterday, RSI > RSI 2 days ago, RSI < RSI 2 days ago
#6 inputs for MACD
#MACD-SIG > 1, MACD-SIG < 1, MACD-SIG > yesterday, MACD-SIG < yesterday, MACD-SIG > 2 days ago, MACD-SIG < 2 days ago
#2 for ATR
#ATR_UP > 0, ATR_UP <= 0
#6 inputs for SMA5
#SMA5 <= open, SMA5 > open, SMA5 <= SMA5 yesterday, SMA5 > SMA5 yesterday, SMA5 <= 2 days ago, SMA5 > 2  days ago
#
#open to open, close to close, ema to ema

import talib
import numpy as np
import math
    
# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def initialize(context):
    context.stock = symbol('SPY')
    context.syn0 = 0
    context.syn1 = 0
    context.runs = 0
    context.x = 0
    context.y = 0
    context.init = False
    context.backwards = 150  #3275 = max from 01/03/2015
    
    #data
    context.close_data = 0
    context.open_data = 0
    context.high_data = 0
    context.low_data = 0
    context.training_outputs = 0
    context.training_data = 0
    
    #it takes several days to get valid data
    context.start = 0
    
    # input dataset
    # 510 day, 200 day
        

#    schedule_function(rebalance, 
#                      date_rules.month_end(days_offset=0),
#                      time_rules.market_close(hours = 0, minutes = 15)) 
# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    
    if(context.init == False):
        open_price =  history(context.backwards, '1d', 'open_price')
        close =  history(context.backwards, '1d', 'close_price')
        high = history(context.backwards, '1d', 'high')
        low = history(context.backwards, '1d', 'low')
        context.close_data = close[context.stock]
        context.open_data = open_price[context.stock]
        context.high_data = high[context.stock]
        context.low_data = low[context.stock]
        sma5 = talib.EMA(context.open_data, timeperiod = 5)
        sma10 = talib.EMA(context.open_data, timeperiod = 10)
        percent_total = 0
        
        
#Technical Indicators
        rsi_test = talib.RSI(context.open_data)
        macd, signal, hist = talib.MACD(context.open_data, fastperiod=12, slowperiod=26, signalperiod=9)
#        macd_test = talib.MACD(context.open_data, fastperiod=12, slowperiod=26, signalperiod=9)
        atr_test = talib.ATR(context.high_data, context.low_data, context.close_data, timeperiod=14)
        

        print "macd"
        for j in xrange(100):
            if(math.isnan(macd[j])):
                continue
            else:
                context.start = j
                break
#        print macd[j:-1]
#        print "signal"
        for j in xrange(100):
            if(math.isnan(signal[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
                break
#        print signal[j-1:-1]
#        print "hist"
        for j in xrange(100):
            if(math.isnan(hist[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
#                print j
                break
#        print hist[j-1:-1]
#        print "open data"
        print open_price
#        print "rsi test!"
        for j in xrange(100):
            if(math.isnan(rsi_test[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
#                print j
                break
#        print rsi_test[j-1:-1]
#        print "atr test!"
        for j in xrange(100):
            if(math.isnan(atr_test[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
#                print j
                break
        for j in xrange(100):
            if(math.isnan(sma5[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
                break
        for j in xrange(200):
            if(math.isnan(sma10[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
                break
        print "context.start"
        print context.start
        
        
        outputs = []
        data_len = len(context.open_data)
        print str("len : ") + str(data_len)
        for x in range(context.start, data_len):
            buy_price = context.open_data[x]
            high_price = buy_price
            loss = 0
            for y in range(0, data_len):
                if(y+x+1 < data_len) and (loss <= 0.01):
                    if(context.open_data[x+y] > high_price):
                        high_price = context.open_data[x+y]
                    loss = (high_price - context.open_data[x+y])/high_price
                else:
                    money_made = context.open_data[x+y] - buy_price
                    percent_up = money_made / buy_price
                    break
            if(percent_up > 0.05):
#                print str("stoped making money x: ") + str(x) + str(" b: ")  + str(buy_price) + str(" c: ") + str(context.open_data[x+y]) + str(" y: ") + str(y) + str(" h: ") + str(high_price) + str(" : ") + str(high_price-buy_price) + str(" mm: ") + str(money_made) + str(" pu: ") + str(percent_up) 
#            percent_increase = (context.close_data[x]-context.open_data[x])/context.open_data[x]
        
#        if(context.close_data[x] > context.open_data[x]):
#            outputs.append(1)
#            if(sma5[x] > context.open_data[x]):
                outputs.append(1)
#                percent_total = percent_total + percent_increase
#            print str(percent_increase) + " : " + str(context.close_data[x]) + " : " + str(context.open_data[x]) + " : " + str(sma5[x])
            else:
                outputs.append(0)
        
#        print str("made it here!!!!!!!!!!") + str(len(outputs))
        context.training_data = np.column_stack((sma5[context.start:-1], context.open_data[context.start:-1]))
#        print "training data shape"
#        print context.training_data.shape
#        print len(sma5)
#        print len(context.open_data)
#        print len(outputs)
        context.training_outputs = np.column_stack((outputs[0:-1])).T
        print(context.training_outputs)
#        print len(context.training_outputs)
#        print context.training_outputs
        
        context.x = context.training_data
        context.y = context.training_outputs
#        context.x = np.array([[0,0,1],
#                              [0,1,1],
#                              [1,0,1],
#                              [1,1,1]])
#        context.y =([[0],
#                     [1],
#                     [1],
#                     [0]])
#        context.x = np.array([[0,0,1],
#                              [0,0,1],
#                              [0,0,1],
#                              [0,0,1]])
#        context.y =([[0],
#                     [1],
#                     [1],
#                     [0]])
        
        np.random.seed(1)
        # randomly initialize our weights with mean 0
        context.syn0 = 2*np.random.random((len(context.x[0]),len(context.x))) - 1
        context.syn1 = 2*np.random.random((len(context.y),len(context.y[0]))) - 1
    
    context.init = True
    context.runs = context.runs + 1
    if(context.runs % 100 == 0):
        print str("runs : ") + str(context.runs)
    for j in xrange(10):
        # Feed forward through layers 0, 1, and 2
        l0 = context.x
        l1 = nonlin(np.dot(l0,context.syn0))
        l2 = nonlin(np.dot(l1,context.syn1))
        # how much did we miss the target value?
        l2_error = context.y - l2
        if (context.runs % 100 == 0 and j == 1):
            print "Error:" + str(np.mean(np.abs(l2_error)))
        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        l2_delta = l2_error*nonlin(l2,deriv=True)
        # how much did each l1 value contribute to the l2 error (according to the weights)?
        l1_error = l2_delta.dot(context.syn1.T)
        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        l1_delta = l1_error * nonlin(l1,deriv=True)
        context.syn1 += l1.T.dot(l2_delta)
        context.syn0 += l0.T.dot(l1_delta)

        
    # Implement your algorithm logic here.

    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.

    # Place orders with the order(SID, amount) method.

    # TODO: implement your own logic here.
#    order(sid(24), 50)

