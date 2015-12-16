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
#6 for ATR
#ATR_UP > 0, ATR_Down <= 0, ATR_UP_Y > 0, ATR_Down_Y <= 0, ATR_UP_2da > 0, ATR_Down_2da <= 0
#6 inputs for SMA10
#SMA <= open, SMA > open, SMA <= SMA yesterday, SMA > SMA yesterday, SMA <= 2 days ago, SMA > 2  days ago
#
#Total Training Inputs : 25

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
    context.backwards = 300  #3275 = max from 01/03/2015
    
    #data
    context.close_data = 0
    context.open_data = 0
    context.high_data = 0
    context.low_data = 0
    context.training_outputs = 0
    context.training_data = 0
    
    #it takes several days to get valid data
    context.start = 0
    
    context.MAXTRAINIED = 100000
    context.syn1Done = False
    context.lastPrint = 0
    
    context.syn0Done = False
    context.lastRow = 0
    context.lastCol = 0
    
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
        sma = talib.EMA(context.open_data, timeperiod = 10)
        
        
#Technical Indicators
        rsi_test = talib.RSI(context.open_data)
        macd, signal, hist = talib.MACD(context.open_data, fastperiod=12, slowperiod=26, signalperiod=9)
#        macd_test = talib.MACD(context.open_data, fastperiod=12, slowperiod=26, signalperiod=9)
        atr_test = talib.ATR(context.high_data, context.low_data, context.close_data, timeperiod=14)
        

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
            if(math.isnan(sma[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
                break
        for j in xrange(200):
            if(math.isnan(sma[j])):
                continue
            else:
                if(j > context.start):
                    context.start = j
                break
                
        context.start = context.start + 2
        print "context.start"
        print context.start
        
        rsiL30 = []
        rsiGE30LE70 = []
        rsiG70 = []
        rsiGy = []
        rsiLy = []
        rsiG2da = []
        rsiL2da = []
        mmSigG1 = []
        mmSigL1 = []
        mmSigGy = []
        mmSigLy = []
        mmSigG2da = []
        mmSigL2da = []
        atrUp = []
        atrDown = []
        atrUpy = []
        atrDowny = []
        atrUp2da = []
        atrDown2da = []
        smaGo = []
        smaLo = []
        smaGy = []
        smaLy = []
        smaG2da = []
        smaL2da = []
        data_len = len(context.open_data)
        for x in range(context.start, data_len):
            if(rsi_test[x] < 30):
                rsiL30.append(1)
            else:
                rsiL30.append(0)
            if(rsi_test[x] >= 30 and rsi_test[x] <= 70):
                rsiGE30LE70.append(1)
            else:
                rsiGE30LE70.append(0)
            if(rsi_test[x] > 70):
                rsiG70.append(1)
            else:
                rsiG70.append(0)
            if(rsi_test[x] > rsi_test[x-1]):
                rsiGy.append(1)
                rsiLy.append(0)
            else:
                rsiGy.append(0)
                rsiLy.append(1)
            if(rsi_test[x] > rsi_test[x-2]):
                rsiG2da.append(1)
                rsiL2da.append(0)
            else:
                rsiG2da.append(0)
                rsiL2da.append(1)
            if((macd[x] - signal[x]) > 1):
                mmSigG1.append(1)
                mmSigL1.append(0)
            else:
                mmSigG1.append(0)
                mmSigL1.append(1)
            if((macd[x-1] - signal[x-1]) > 1):
                mmSigGy.append(1)
                mmSigLy.append(0)
            else:
                mmSigGy.append(0)
                mmSigLy.append(1)
            if((macd[x-2] - signal[x-2]) > 1):
                mmSigG2da.append(1)
                mmSigL2da.append(0)
            else:
                mmSigG2da.append(0)
                mmSigL2da.append(1)
            if(atr_test[x] > 0):
                atrUp.append(1)
                atrDown.append(0)
            else:
                atrUp.append(0)
                atrDown.append(1)
            if(atr_test[x-1] > 0):
                atrUpy.append(1)
                atrDowny.append(0)
            else:
                atrUpy.append(0)
                atrDowny.append(1)
            if(atr_test[x-2] > 0):
                atrUp2da.append(1)
                atrDown2da.append(0)
            else:
                atrUp2da.append(0)
                atrDown2da.append(1)
            if(sma[x] > context.open_data[x]):
                smaGo.append(1)
                smaLo.append(0)
            else:
                smaGo.append(0)
                smaLo.append(1)
            if(sma[x-1] > context.open_data[x-1]):
                smaGy.append(1)
                smaLy.append(0)
            else:
                smaGy.append(0)
                smaLy.append(1)
            if(sma[x-2] > context.open_data[x-2]):
                smaG2da.append(1)
                smaL2da.append(0)
            else:
                smaG2da.append(0)
                smaL2da.append(1)
        
        outputs = []
        ones = 0
        zeros = 0
        print str("len : ") + str(data_len)
        for x in range(context.start, data_len):
            buy_price = context.open_data[x]
            high_price = buy_price
            loss = 0
            percent_up = 0
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
                outputs.append(1)
                ones = ones + 1
            else:
                outputs.append(0)
                zeros = zeros + 1
                
        print ("ones then zeros : ") + str(ones) + str(" : ") + str(zeros)
                
        context.training_data = np.column_stack((rsiL30, rsiGE30LE70, rsiG70,rsiGy, rsiLy, rsiG2da, rsiL2da,
                                                mmSigG1, mmSigL1, mmSigGy, mmSigLy, mmSigG2da, mmSigL2da,
                                                atrUp, atrDown, atrUpy, atrDowny, atrUp2da, atrDown2da,
                                                smaGo, smaLo, smaGy, smaLy, smaG2da, smaL2da))

        context.training_outputs = np.column_stack((outputs)).T
        print str("shapes : ") + str(context.training_data.shape) + str(" : ") + str(context.training_outputs.shape)
        
    
        for e in range(0, len(outputs)):
            count_bad = 0
            count_good = 0
            if context.training_outputs[e,0] == 1:
                for y in range(0, len(outputs)):
                    if (context.training_data[e] == context.training_data[y]).all() and context.training_outputs[y] == 0:
                        count_bad = count_bad+1
                    elif (context.training_data[e] == context.training_data[y]).all() and context.training_outputs[y] == 1:
                        count_good = count_good + 1
                if count_bad != 0 :
                    print str(count_bad) + str(' : ') + str(count_good)
        
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
        
    elif context.runs < context.MAXTRAINIED:
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
            
            
            
            
        record(error = np.mean(np.abs(l2_error)))

#        print "shapes of the weights : " + str(context.syn0.shape) + str (" : ") + str(context.syn0.shape[0]) + str (" : ") + str(context.syn1.shape)
    elif context.syn1Done == False:
        if context.lastPrint < context.syn1.shape[0]:
            print context.syn1[context.lastPrint]
            context.lastPrint = context.lastPrint+1
        else:
            context.lastPrint = 0
            context.syn1Done = True
            print "shapes of the weights : " + str(context.syn0.shape) + str (" : ") + str(context.syn0.shape[0]) + str (" : ") + str(context.syn1.shape)
            print "syn1 Finished!"
    elif context.syn0Done == False:
        if context.lastCol < context.syn0.shape[1]:
            print context.syn0[context.lastRow, context.lastCol]
            if context.lastRow < context.syn0.shape[0]-1:
                context.lastRow = context.lastRow+1
            else:
                context.lastRow = 0
                print "col" + str(context.lastCol)
                context.lastCol = context.lastCol+1
               
               
            
               
        else:
            context.lastPrint = 0
            context.syn0Done = True
            print "syn0 Finished!"
            
    else:
        return
        
            
        
    # Implement your algorithm logic here.

    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.

    # Place orders with the order(SID, amount) method.

    # TODO: implement your own logic here.
#    order(sid(24), 50)

