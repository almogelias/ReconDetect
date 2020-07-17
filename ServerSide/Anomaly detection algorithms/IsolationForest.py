
# libraries
#%matplotlib notebook
import joblib
import pandas as pd
import numpy as np
import pyodbc
import matplotlib
import seaborn
import matplotlib.dates as md
from matplotlib import pyplot as plt
import time

from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.covariance import EllipticEnvelope
#from pyemma import msm # not available on Kaggle Kernel
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

'''
####Machine learning Functions#####
# return Series of distance between each point and his distance with the closest centroid
def getDistanceByPoint(data, model):
    distance = pd.Series()
    for i in range(0,len(data)):
        Xa = np.array(data.loc[i])
        Xb = model.cluster_centers_[model.labels_[i]-1]
        distance.set_value(i, np.linalg.norm(Xa-Xb))
    return distance

# train markov model to get transition matrix
def getTransitionMatrix (df):
	df = np.array(df)
	model = msm.estimate_markov_model(df, 1)
	return model.transition_matrix

def markovAnomaly(df, windows_size, threshold):
    transition_matrix = getTransitionMatrix(df)
    real_threshold = threshold**windows_size
    df_anomaly = []
    for j in range(0, len(df)):
        if (j < windows_size):
            df_anomaly.append(0)
        else:
            sequence = df[j-windows_size:j]
            sequence = sequence.reset_index(drop=True)
            df_anomaly.append(anomalyElement(sequence, real_threshold, transition_matrix))
    return df_anomaly
'''


#Main

counter=0
while (True):
    driver = 'ODBC Driver 17 for SQL Server'
    server = 'DESKTOP-GRTRD9G'
    db = 'FinalProject'
    filenamePackets = 'C:\\Model\\modelPackets.sav'
    filenameFlows = 'C:\\Model\\modelFlows.sav'
    # load the model from disk

    try:
        model = joblib.load(filenamePackets)
        model = joblib.load(filenameFlows)
        print("Models found!")
    except:
        print ("Didn't find models, starting without model")

    #Data
    #### Add Loop + Delay
    connSQLServer = pyodbc.connect(
            r'DRIVER={' + driver + '};'
                                   r'SERVER=' + server + ';'
                                                         r'DATABASE=' + db + ';'
                                                                             r'UID=sa;'
                                                                             r'PWD=Ll123456'
    )

    ### Main query

    queryFlows = """SELECT TOP 30 FlowID,counterOfPackets,dstPort,counterOfSyn,counterOfPa,counterOfR,counterOfRA,counterOfFin,packetsTotalSize
    FROM [FinalProject].[dbo].[Flows] order by FlowID desc"""

    queryPackets="""SELECT TOP 30 [PacketCountTenID]
          ,[packetCount]
          ,[counterOfSyn]
          ,[counterOfPa]
          ,[counterOfR]
          ,[counterOfRA]
          ,[counterOfFin]
          ,[packetsTotalSize]
      FROM [FinalProject].[dbo].[packetsCountTenSecond]
      ORDER BY [PacketCountTenID] DESC"""

    time.sleep(11)
    counter+=1
    if(counter == 3):
        counter=0
        df2 = pd.read_sql(queryFlows, connSQLServer)
        print("\n###### FEATURES STATISTICS ######")
        print("\n###### Features Type ######\n")
        print(df2.info())
        print("\n###### Mean Statistics ######\n")
        print(
            df2[['counterOfPackets', 'counterOfSyn', 'counterOfPa','counterOfR','counterOfRA', 'packetsTotalSize']].mean())

        if (not df2.empty):
            outliers_fraction = 0.14

            # Isolation Tree

            data = df2[['dstPort','counterOfPackets', 'counterOfSyn', 'counterOfPa','counterOfR','counterOfRA', 'packetsTotalSize']]
            min_max_scaler = preprocessing.StandardScaler()
            np_scaled = min_max_scaler.fit_transform(data)
            # data['scaled'] = pd.DataFrame(np_scaled)
            data = pd.DataFrame(np_scaled)
            # train isolation forest
            model = IsolationForest(contamination=outliers_fraction, behaviour="new")
            model.fit(data)

            ## save model
            joblib.dump(model, filenameFlows)

            # add the data to the main
            df2['Anomaly'] = pd.Series(model.predict(data))
            df2['Anomaly'] = df2['Anomaly'].map({1: 0, -1: 1})

            # anomaly_result=df.loc[df['Anomaly'] == 1]

            print(df2)
            cursor = connSQLServer.cursor()
            cursor.execute("""UPDATE [FinalProject].[dbo].[packetsCountTenSecond]
                                SET Anomaly=0
                                WHERE PacketCountTenID BETWEEN {} AND {}""".format(df1["PacketCountTenID"].iloc[-1],df1["PacketCountTenID"].iloc[0]))
            connSQLServer.commit()
            for index, row in df2.iterrows():
                cursor.execute("""UPDATE [FinalProject].[dbo].[Flows]
                SET Anomaly={}
                WHERE FlowID={}""".format(row['Anomaly'], row['FlowID']))
                connSQLServer.commit()
            cursor.close()


    df1 = pd.read_sql(queryPackets, connSQLServer)
    ## Show Default data Plot
    #df.plot(x='FlowID', y='counterOfSyn')

    print("\n###### FEATURES STATISTICS ######")
    print("\n###### Features Type ######\n")
    print(df1.info())
    print("\n###### Mean Statistics ######\n")
    # for flows  -   print(df[['counterOfPackets', 'counterOfSyn', 'counterOfPa','counterOfR','counterOfRA', 'packetsTotalSize']].mean())
    print(df1[['packetCount', 'counterOfSyn', 'counterOfPa','counterOfR','counterOfRA', 'packetsTotalSize']].mean())
    #Fit Data
    # time with int to plot easily
    #df['time_epoch'] = (df['timestamp'].astype(np.int64)/100000000000).astype(np.int64)
    # the hours and if it's night or day (7:00-22:00)
    #df['hours'] = df['timestamp'].dt.hour
    #df['daylight'] = ((df['hours'] >= 7) & (df['hours'] <= 22)).astype(int)
    # the day of the week (Monday=0, Sunday=6) and if it's a week end day or week day.
    #df['DayOfTheWeek'] = df['timestamp'].dt.dayofweek
    #df['WeekDay'] = (df['DayOfTheWeek'] < 5).astype(int)
    # An estimation of anomly population of the dataset (necessary for several algorithm)

    if (not df1.empty):
        outliers_fraction = 0.14

        # Isolation Tree
        #data = df[['dstPort','counterOfPackets', 'counterOfSyn', 'counterOfPa','counterOfR','counterOfRA', 'packetsTotalSize']]
        data = df1[['packetCount', 'counterOfSyn', 'counterOfPa', 'counterOfR', 'counterOfRA', 'packetsTotalSize']]
        min_max_scaler = preprocessing.StandardScaler()
        np_scaled = min_max_scaler.fit_transform(data)
        #data['scaled'] = pd.DataFrame(np_scaled)
        data = pd.DataFrame(np_scaled)
        # train isolation forest
        model = IsolationForest(contamination = outliers_fraction, behaviour="new")
        model.fit(data)

        ## save model
        joblib.dump(model, filenamePackets)

        # add the data to the main
        df1['Anomaly'] = pd.Series(model.predict(data))
        df1['Anomaly'] = df1['Anomaly'].map( {1: 0, -1: 1} )

        #anomaly_result=df.loc[df['Anomaly'] == 1]

        print(df1)
        cursor = connSQLServer.cursor()
        cursor.execute("""UPDATE [FinalProject].[dbo].[packetsCountTenSecond]
                    SET Anomaly=0
                    WHERE PacketCountTenID BETWEEN {} AND {}""".format(df1["PacketCountTenID"].iloc[-1],df1["PacketCountTenID"].iloc[0]))
        connSQLServer.commit()
        for index, row in df1.iterrows():
            cursor.execute("""UPDATE [FinalProject].[dbo].[packetsCountTenSecond]
            SET Anomaly={}
            WHERE PacketCountTenID={}""".format(row['Anomaly'], row['PacketCountTenID']))
            connSQLServer.commit()
        cursor.close()
        connSQLServer.close()

        '''
            for index,row in df.iterrows():
                cursor.execute("""UPDATE [FinalProject].[dbo].[Flows] 
                SET Anomaly={}
                WHERE FlowID={}""".format(row['Anomaly'],row['FlowID']))
                connSQLServer.commit()
            cursor.close()
            connSQLServer.close()
        '''

        ## Show anomaly points
        '''
        fig, ax = plt.subplots()
        
        a = df.loc[df['Anomaly'] == 1, ['FlowID', 'packetsTotalSize']] #anomaly
        ax.plot(df['FlowID'], df['packetsTotalSize'], color='blue')
        ax.scatter(a['FlowID'],a['packetsTotalSize'], color='red')
        plt.show()
        '''
