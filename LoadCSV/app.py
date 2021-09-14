import csv
import matplotlib.pyplot as plt
import Operaciones as Op
import numpy
from mpl_toolkits.mplot3d import Axes3D

# Declaración de matriz que contiene todas las iteraciones
h = []

ChannelRealizationFileName = "./ChannelRealizations/realizationArray"
for i in range(0, 100):
    fileRoute = ChannelRealizationFileName + str(i+1) + ".csv"
    with open(fileRoute) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        temph = []
        for row in csv_reader:
            temprow = []
            for column in row:
                column = column.replace(" ","")
                column = column.replace("i","j")
                column = column.split("+")
                if column[1][0] == '-':
                    column = column[0] + column[1]
                else:
                    column = column[0] + "+" + column[1]
                temprow.append(complex(column))
            temph.append(temprow)
        h.append(temph)

print(len(h))
print(len(h[0]))
print(len(h[0][0]))

# Perfil de potencia de retardo
average = Op.Promedio(h)
PDDR = Op.PPR(average)

# Funcion de dispersion
FDD = Op.FDD(h)

# Autocorrelación de frecuencia
FDA = Op.FDA(Op.FillWith0s(PDDR, 2048))

# Densidad espectral de potencia
DEDP = Op.DEDP(FDD)

# Funcion de correlacion temporal
FDCT = Op.FCT(DEDP)


# Guardar los datos
numpy.savetxt("perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
numpy.savetxt("funcionDeDispersion.csv", FDD, fmt='% s', delimiter=',', newline='\n')
numpy.savetxt("correlacionDeFrecuencia.csv", [FDA], fmt='% s', delimiter=',', newline='\n')
numpy.savetxt("densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
numpy.savetxt("correlacionTemporal.csv", [FDCT], fmt='% s', delimiter=',', newline='\n')



#Mostrar gráficas
# Perfil de potencia de retardo
plt.plot((PDDR))
plt.ylabel('Perfil de potecia de retardo')
plt.show()

# Autocorrelación de frecuencia
plt.plot(numpy.fft.fftshift(FDA))
plt.ylabel('Autocorrelación de frecuencia')
plt.show()

# Funcion de dispersion
#Op.Mostrar("Funcion de dispersion", FDD, 2)
fig = plt.figure()
ax3d = plt.axes(projection="3d")

xdata = numpy.linspace(0,10,11)
ydata = numpy.linspace(0,1023,1024)
ydata = numpy.fft.fftshift(ydata)
X,Y = numpy.meshgrid(xdata,ydata)

ax3d = plt.axes(projection='3d')
ax3d.plot_surface(X, Y, FDD, cmap='plasma')
ax3d.set_title('Funcion de dispersion')
ax3d.set_xlabel('X')
ax3d.set_ylabel('Y')
ax3d.set_zlabel('Z')
  
plt.show() 

# Densidad espectral de potencia
plt.plot(numpy.fft.fftshift(DEDP))
plt.ylabel('Densidad espectral de potencia')
plt.show()

# Funcion de correlacion temporal
plt.plot(numpy.fft.fftshift(FDCT))

plt.ylabel('Funcion de correlacion temporal')
plt.show()


