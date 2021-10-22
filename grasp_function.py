import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.preprocessing import PolynomialFeatures

DATA = './robotis_data.csv'


class Grasp_Distance:
    def __init__(self,flag=False,data=DATA,degree=3):
        '''
        This class learns the parameters of third order function 
        from the given csv_data
        '''
        
        self.flag = flag
        self.data = pd.read_csv(data).to_numpy()
        self.degree = degree
        self.x = self.data[:,1].reshape(-1,1)
        self.y = self.data[:,0].reshape(-1,1)
        self.polynomial_features= PolynomialFeatures(degree=degree)
        self.x_poly = self.polynomial_features.fit_transform(self.x)
        self.reg = LinearRegression().fit(self.x_poly,self.y)

    def __del__(self):
        pass

    def __learner(self):
        coef = self.reg.coef_
        intercept = self.reg.intercept_
        # print("Regression Score is :{}".format(self.reg.score(self.x_poly,self.y)))
        # print("Regression Coefficent: {} and Interacept: {}".format(coef, intercept))
        # print("Predicted coefficents:= {} and intercept {}".format(coef,intercept))
        return self.reg
        

    def prediction(self,value,flag=False):
        if type(value) is not float or value > 110.0 or value < 5.0:
            raise ValueError("Input argument is over min/max limits or not float!!!")
        value = self.polynomial_features.fit_transform([[value]])
        pred = self.__learner().predict(value)
        if flag:
            print("Plotting learned vs original function!!!")
            self.__plot()
        return int(pred)

    def __plot(self):
        fig,ax = plt.subplots()
        y_pred = self.reg.predict(self.x_poly)
        plt.plot(self.x,self.y,'*-',label="Robotis Data")
        plt.plot(self.x,y_pred,'o-',label="Learned Line Function")
        plt.xlabel("Robotis gripper closing distance (mm)")
        plt.ylabel("Data to input to packate handler (Units unknown)")
        plt.legend()
        plt.grid()
        plt.show()



# if __name__ == '__main__':
#     obj = Grasp_Distance()
#     out = obj.prediction(105.1,flag=False)
#     print(out)
