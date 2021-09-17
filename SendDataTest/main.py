import matplotlib.pyplot as plt
import Operaciones as Op
import numpy as np
import time

def makeOp(h):
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
    np.savetxt("./Saves/perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
    np.savetxt("./Saves/funcionDeDispersion.csv", FDD, fmt='% s', delimiter=',', newline='\n')
    np.savetxt("./Saves/correlacionDeFrecuencia.csv", [FDA], fmt='% s', delimiter=',', newline='\n')
    np.savetxt("./Saves/densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
    np.savetxt("./Saves/correlacionTemporal.csv", [FDCT], fmt='% s', delimiter=',', newline='\n')
    print('time for saving the data in csv: ', time.time() - start)


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
    fig = plt.figure()
    ax3d = plt.axes(projection="3d")

    xdata = np.linspace(0,10,11)
    ydata = np.linspace(0,1023,1024)
    ydata = np.fft.fftshift(ydata)
    X,Y = np.meshgrid(xdata,ydata)

    ax3d = plt.axes(projection='3d')
    ax3d.plot_surface(X, Y, FDD, cmap='plasma')
    ax3d.set_title('Funcion de dispersion')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    
    plt.show() 

    # Densidad espectral de potencia
    plt.plot(np.fft.fftshift(DEDP))
    plt.ylabel('Densidad espectral de potencia')
    plt.show()

    # Funcion de correlacion temporal
    plt.plot(np.fft.fftshift(FDCT))

    plt.ylabel('Funcion de correlacion temporal')
    plt.show()