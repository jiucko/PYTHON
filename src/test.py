import pandas as pd

path = './melb_data.csv'
melb_data = pd.read_csv(path)
melb_data.describe()

#print(melb_data.columns)

y = melb_data.Price

melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

X = melb_data[melbourne_features]

print(X.describe())


#print(X.head())


#print(y