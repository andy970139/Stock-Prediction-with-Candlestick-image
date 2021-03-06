import numpy as np
import pandas as pd
#import talib
import os
import mplfinance as mpf
import matplotlib as mpl
mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)

# kwargs = dict(type='candle', mav=(5,10,15), volume=False, figratio=(5,3), figscale=0.5
#               , title='', style=s,axisoff= True,scale_padding=0) 
kwargs = dict(type='candle', mav=(5,10,20), volume=False, figsize=(15/10,8/10),figscale=1
              , title='', style=s,axisoff= True,scale_padding=0) 

def outPic(x,y,stockname='tt',mode = 'train'):
    # mpl.rcParams['lines.linewidth']=0.01
    # x=Traindatax
    # y=Traindatay
    # apmavs = [ mpf.make_addplot(x['ma5l']),mpf.make_addplot(x['ma10l']) ]

    y=y.to_numpy()
    global kwargs
    global window
    save_url='Trainimg'
    if mode=='train': 
        save_url='candle'
    else:
        save_url='Testimg'
        
    # for i in range(len(x)-window):
    for i in range(0,len(x)-window,3):        
        # i=2
        # filename=save_url+"\\"+stockname+str(i)+'_'+str(y[i+window-1][0])+str(y[i+window-1][1])+str(y[i+window-1][2])+str(y[i+window-1][3])+'.png'
        filename=save_url+"\\"+stockname+str(i)+'_'+str(y[i+window-1][0])+'.png'  
        
        apmavs = [mpf.make_addplot(x[i:i+window]['ma5l'],color='#C6A300'),
                  mpf.make_addplot(x[i:i+window]['ma10l'],color='#17becf')
                  ,mpf.make_addplot(x[i:i+window]['ma20l'],color='#9467bd')]
        mpf.plot(x[i:i+window], **kwargs,savefig=filename,scale_width_adjustment=dict(lines=0.3),addplot=apmavs)

def convert2graph(data):
    
    # data=Secondary_x[0]
    rank=data.ravel().argsort().argsort().reshape(data.shape) 
    
    result =np.zeros((4*data.shape[0],data.shape[0],data.shape[1]+1)) #最後一維為k線圖 1最低 2開盤 3收盤 4最高
    
    

    for j in range(window):
        start=4*data.shape[0]-rank[j,0]-1
        end=4*data.shape[0]-rank[j,3]
        result[:,:,4][end:start][:,j]=1 
        #先把最低到最高的線補好
    
    for i in range(4):    
        for j in range(window):
            position=rank[:,i][j]
            result[:,:,i][4*data.shape[0]-position-1][j]=i+1
            
      
    #處理最後一維圖形        
    for j in range(window):
        open_price=rank[:,1][j]
        high=rank[:,3][j]
        low=rank[:,0][j]
        close_price=rank[:,2][j]
         
        result[:,:,4][4*data.shape[0]-high-1][j]=4   
        result[:,:,4][4*data.shape[0]-open_price-1][j]=2  
        result[:,:,4][4*data.shape[0]-close_price-1][j]=3  
        result[:,:,4][4*data.shape[0]-low-1][j]=1  
        
        
    return result

#%%

#%%


filelist=os.listdir('dataset')

# filelist=['2201.csv']
handlex=[]
# handlefdf=[]
handley=[]
window=20

Traindatax=[]
# Traindatafx=[]
Traindatay=[]
Testdatax=[]
# Testdatafx=[]
Testdatay=[]
for file in filelist: #處理時間序列破裂部分 只留完整的
    # x=[]
    # y=[]
    # # y2=[]
    # fx=[]
    df = pd.read_csv('dataset\\'+file,sep = ",")  
    fdf=pd.read_csv('fdataset\\'+file,sep = ",")    

    intersected_df = pd.merge(df['Date'], fdf['Date'], on=['Date'], how='inner') #都有的工作日
 
    
    df=df[['Date','low','open','close','high','Y','ma5l','ma10l','ma20l']]
    df.index = pd.DatetimeIndex(df['Date'])
    y=df[['Y']]
    # df=df[['Date','open','high','low','close','Y','Y5','Y10','Y20']].set_index('Date')

    fdf=fdf.set_index('Date')
    
    handlex=[]
    Traindatax=df[:int(len(df)*4/5)]
    Traindatay=y[:int(len(y)*4/5)] 
    
    Testdatax=df[int(len(df)*4/5):]  
    Testdatay=y[int(len(y)*4/5):] 
    
    # Testdatax=df[:40]  
    # Testdatay=y[:40]
    
    outPic(Traindatax,Traindatay,stockname=file.replace(".csv", ""),mode = 'train')
    # outPic(Testdatax,Testdatay,stockname=file.replace(".csv", ""),mode = 'test')    
    #%%
 
#%%
import os
import cv2
import numpy as np
from PIL import Image
filelist=set(os.listdir('line\\Trainimg'))
filelist2=set(os.listdir('E:\\candle'))
filelist= list( filelist & filelist2 )
x=[]
x2=[]
y=[]

    # im_cv = cv2.imread('22018_0000.png')
for file in filelist: #處理時間序列破裂部分 只留完整的
    im_cv = cv2.imread('line\\Trainimg\\'+file)  #E:\candle
    im_cv2= cv2.imread('E:\\candle\\'+file)
    # im_cv = cv2.imread('Testimg\\'+file) 
    # print(im_cv.shape)
    # im_cv=cv2.resize(im_cv, (288,480), interpolation = cv2.INTER_AREA)
    # im_cv = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)   
    # im_cv2 = cv2.cvtColor(im_cv2, cv2.COLOR_BGR2RGB)       
    x.append(im_cv)
    x2.append(im_cv2) 
    answer =np.zeros((4))
    # answer[-1]=file.replace(".png", "")[-1]
    # answer[-2]=file.replace(".png", "")[-2]    
    # answer[-3]=file.replace(".png", "")[-3]
    # answer[-4]=file.replace(".png", "")[-4]
    y.append(int( file.replace(".png", "").split("_")[-1] ))

# for file in filelist: #處理時間序列破裂部分 只留完整的
#     im_cv2= cv2.imread('E:\\candle\\'+file)
   



x=np.array(x)
x2=np.array(x2)
# x2=np.vstack(x2)
y=np.vstack(y)
#%%

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" #會使用CPU
import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras import regularizers
from tensorflow.keras.layers import BatchNormalization,LayerNormalization,Flatten,Conv2D,Conv3D,GlobalAveragePooling2D,MaxPooling2D
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense,concatenate,Bidirectional
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LayerNormalization
# import tensorflow_addons as tfa
# from attention import Attention
# window=44
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 22
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

main_input = Input(shape=(80,150,3),name='inputLayer')


cnn3=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(main_input)



cnn5=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(main_input)
cnn5=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn5)

cnn7=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(main_input)
cnn7=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn7)
cnn7=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn7)


cocatlayer= concatenate([ cnn3,cnn5,cnn7])
print(cocatlayer.shape)
cocatlayer=Conv2D(filters = 16,kernel_size=(1,1),activation='relu')(cocatlayer)


candle_input = Input(shape=(80,150,3),name='candle_inputer')


cnn3c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(candle_input)



cnn5c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(candle_input)
cnn5c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn5c)

cnn7c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(candle_input)
cnn7c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn7c)
cnn7c=Conv2D(filters = 16,kernel_size=(3,3),activation='relu',padding='same')(cnn7c)


cocatlayerc= concatenate([ cnn3c,cnn5c,cnn7c])


cocatlayerc=Conv2D(filters = 16,kernel_size=(1,1),activation='relu')(cocatlayerc)


output= concatenate([ cocatlayer,cocatlayerc])

output=Conv2D(filters = 8,kernel_size=(1,1),activation='relu')(output)
print(output.shape)
output=GlobalAveragePooling2D()(output)
# print(x.shape)
# x=Flatten()(x)
output=Dense(units =1)(output)
# print(x.shape)
regressor=Model([main_input,candle_input],output)
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error',
              metrics=['mae'])
# regressor.compile(optimizer = 'adam', loss = 'binary_crossentropy',
#               metrics=[tf.keras.metrics.Precision(),'accuracy'])
regressor.summary()
#%%
from tensorflow.keras import backend as K
Trainx = K.cast_to_floatx(Trainx)
Trainfx = K.cast_to_floatx(Trainfx)
TrainY = K.cast_to_floatx(TrainY)



# X_val = K.cast_to_floatx(X_val)

# y_val = K.cast_to_floatx(y_val)


# Testdatax = K.cast_to_floatx(Testdatax)

# Testdatay = K.cast_to_floatx(Testdatay)

opts = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=22)
conf = tf.compat.v1.ConfigProto(gpu_options=opts)


from tensorflow.keras.callbacks import EarlyStopping
# history=regressor.fit(X_train, y_train, epochs = 100, batch_size = 64,validation_data=(X_val,y_val)
                      # ,callbacks=[EarlyStopping(monitor='val_loss', patience=10)])  
history=regressor.fit([Trainx,Trainfx], TrainY, epochs = 50, batch_size = 128, validation_split=0.2
                      ,callbacks=[EarlyStopping(monitor='val_loss', patience=10)]) 