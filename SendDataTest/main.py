import matplotlib.pyplot as plt
import csv
import Operaciones as Op
import numpy as np
import time
import os
from datetime import datetime

class Main:

    def __init__(self):
        self.count = 0
        self.date = datetime.today().strftime('%Y-%m-%d %H.%M')
        self.dir = "./Saves/" + self.date + "/"
        print(self.date)

    def makeOp(self, h):
        # Perfil de potencia de retardo
        startC = time.time()
        start = time.time()
        average = Op.Promedio(h)
        print('average time: ', time.time() - start)
        start = time.time()
        PDDR = Op.PPR(average)
        print('PDDR time: ', time.time() - start)
        start = time.time()
        # Funcion de dispersion
        FDD = Op.FDD(h)
        print('FDD time: ', time.time() - start)
        start = time.time()
        # Autocorrelación de frecuencia
        FDA = Op.FDA(Op.FillWith0s(PDDR, 2048))
        print('FDA time: ', time.time() - start)
        start = time.time()
        # Densidad espectral de potencia
        DEDP = Op.DEDP(FDD)
        print('DEDP time: ', time.time() - start)
        start = time.time()
        # Funcion de correlacion temporal
        FDCT = Op.FCT(DEDP)
        print('FDCT time: ', time.time() - start)
        print('time of operations: ', time.time() - startC)

        # Guardar los datos
        start = time.time()
        dir = self.dir + str(self.count)
        if not os.path.exists(dir):
            os.makedirs(dir)
        np.savetxt(dir + "/perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/funcionDeDispersion.csv", FDD, fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/correlacionDeFrecuencia.csv", [FDA], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/correlacionTemporal.csv", [FDCT], fmt='% s', delimiter=',', newline='\n')
        self.count += 1
        print('time for saving the data in csv: ', time.time() - start)
        #self.showGraphs(PDDR, FDA, FDD, DEDP, FDCT)

    def close(self):
        print("Closing the sesion")
        print("Making the average graphs")
        
        for index in range (self.count):
            dir = self.dir + str(index)
            with open(dir + "/perfilDePotenciaDeRetardo.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                PDDR = []
                for x in csv_reader:
                    PDDR.append(x)
                PDDR = np.array(PDDR).astype(float)

            with open(dir + "/correlacionDeFrecuencia.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                CDF = []
                for x in csv_reader:
                    CDF.append(x)
                CDF = np.array(CDF).astype(float)
            with open(dir + "/densidadEspectralDePotencia.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                DEDP = []
                for x in csv_reader:
                    DEDP.append(x)
                DEDP = np.array(DEDP).astype(float)
            with open(dir + "/correlacionTemporal.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                CT = []
                for x in csv_reader:
                    CT.append(x)
                CT = np.array(CT).astype(float)
        
        PDDR = np.mean(PDDR, axis=0)
        CDF = np.mean(CDF, axis=0)
        DEDP = np.mean(DEDP, axis=0)
        CT = np.mean(CT, axis=0)
        if not os.path.exists(self.dir+"average"):
            os.makedirs(self.dir+"average")
        np.savetxt(self.dir + "average/perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/correlacionDeFrecuencia.csv", [CDF], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/correlacionTemporal.csv", [CT], fmt='% s', delimiter=',', newline='\n')
        print("finished")
        self.showGraphs(PDDR, CDF, DEDP, CT)
    
    
    def showGraphs(self, PDDR, FDA, DEDP, FDCT):
        #Mostrar gráficas
        # Perfil de potencia de retardo
        plt.plot((PDDR))
        plt.ylabel('Perfil de potecia de retardo')
        plt.show()

        # Autocorrelación de frecuencia
        plt.plot(np.fft.fftshift(FDA))
        plt.ylabel('Autocorrelación de frecuencia')
        plt.show()

        # Funcion de dispersion
        #Op.Mostrar("Funcion de dispersion", FDD, 2)
        # fig = plt.figure()
        # ax3d = plt.axes(projection="3d")

        # xdata = np.linspace(0,10,11)
        # ydata = np.linspace(0,1023,1024)
        # ydata = np.fft.fftshift(ydata)
        # X,Y = np.meshgrid(xdata,ydata)

        # ax3d = plt.axes(projection='3d')
        # ax3d.plot_surface(X, Y, FDD, cmap='plasma')
        # ax3d.set_title('Funcion de dispersion')
        # ax3d.set_xlabel('X')
        # ax3d.set_ylabel('Y')
        # ax3d.set_zlabel('Z')
        
        # plt.show() 

        # Densidad espectral de potencia
        plt.plot(np.fft.fftshift(DEDP))
        plt.ylabel('Densidad espectral de potencia')
        plt.show()

        # Funcion de correlacion temporal
        plt.plot(np.fft.fftshift(FDCT))

        plt.ylabel('Funcion de correlacion temporal')
        plt.show()
