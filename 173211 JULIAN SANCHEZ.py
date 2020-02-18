import math
import random
import matplotlib.pyplot as plt
import numpy as np

tamPoblacion = 4
tamTorne = 5
numRuta = 15 # Por los 15 Puntos en donde debe de pasar o Numero de ciudades
probMutacion = 0.8 # 80 %
coordenadaInicial = [] # Guarda las rutas iniciales de X e Y como puntos de ciudades
corInicialX = []
corInicialY = []
coordenadaFinal = []  # Guarda las rutas finales de X e Y
cordFilaX = []
cordFinalY = []
TotalFitness = []
BestFitness = []
BadFitness = []
BestBest = []
promedio =[]
numGeneraciones = 0   # Sólo es para guardar la cantidad de generaciones que serán necesarios


class Ciudad:
   def __init__(self, x=None, y=None):
      self.x = x
      self.y = y

   def getX(self):
      return self.x
   
   def getY(self):
      return self.y
      
   def distanciaDestino(self, ciudad):
      xDistance = abs(self.getX() - ciudad.getX()) #X2 = self.getX()  ,   X1 =  ciudad.getX()
      yDistance = abs(self.getY() - ciudad.getY()) #Y2 = self.getY()  ,   Y1 = ciudad.getY()
      # Fórmula:   √(x2-x1)^2 + (y2-y1)^2
      distance = math.sqrt(abs(((xDistance)*(xDistance)) + (yDistance) * (yDistance)))
      return distance
   
   def __repr__(self):
      coordenadaFinal.append([self.getX()] + [self.getY()])
      cordFilaX.append(self.getX())
      cordFinalY.append(self.getY())
      return str(self.getX()) + ", " + str(self.getY())

# Sólo es para agregar ciudades y extraer ciudades set & get 
class ControlViaje:
   ciudadDestino = []
   
   def addciudad(self, ciudad):
      self.ciudadDestino.append(ciudad)
   
   def getciudad(self, index):
      return self.ciudadDestino[index]

class Viaje:
   def __init__(self, controlViaje, recorrido=None):
      self.controlViaje = controlViaje
      self.recorrido = []
      self.fitness = 0.0
      self.distance = 0
      if recorrido is not None:
         self.recorrido = recorrido
      else:
         for i in range(0, numRuta):
            self.recorrido.append(None)
   
   def __len__(self):
      return len(self.recorrido)
   
   def __getitem__(self, index):
      return self.recorrido[index]
   
   def __setitem__(self, key, value):
      self.recorrido[key] = value
   
   def  __repr__ (self):
      genes = "|"
      for i in range(0, numRuta):
         genes += str(self.getciudad(i)) + "|"
         pass
      print("\nUnion  de X e Y\n")
      return genes

   
   def crearIndividuo(self):
      for ciudadIndex in range(0, numRuta):
         self.setciudad(ciudadIndex, self.controlViaje.getciudad(ciudadIndex))
      random.shuffle(self.recorrido)
   
   def getciudad(self, posAmbu):
      return self.recorrido[posAmbu]
   
   def setciudad(self, posAmbu, ciudad):
      self.recorrido[posAmbu] = ciudad
      self.fitness = 0.0
      self.distance = 0
   
   def Fitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance()) # A partir del val de la distancia de obtiene l fitness de la ruta
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         distanciaViaje = 0
         for ciudadIndex in range(0, numRuta):
            fromciudad = self.getciudad(ciudadIndex)
            destinationciudad = 0
            if ciudadIndex+1 < numRuta:
               destinationciudad = self.getciudad(ciudadIndex+1)
            else:
               destinationciudad = self.getciudad(0)
            distanciaViaje += fromciudad.distanciaDestino(destinationciudad)
           
         self.distance = distanciaViaje
      return self.distance
   
   def containsciudad(self, ciudad): # Almacenar la ciudades generadas 
      return ciudad in self.recorrido


class Poblacion:
   def __init__(self, controlViaje, tamanio, estado):  # El estado puede ser False or True
      self.ArrayViaje = []
      for i in range(0, tamanio):
         self.ArrayViaje.append(None)
      
      if estado: #Si se crea una nueva Poblacion, perfecto va a entrar aca y si no... quiere decir que se esta evolucionando
         for i in range(0, tamanio):
            nuevoViaje = Viaje(controlViaje)
            nuevoViaje.crearIndividuo()
            self.guardarRecorrido(i, nuevoViaje)
      
   def __setitem__(self, key, value):
      self.ArrayViaje[key] = value
   
   def __getitem__(self, index):
      return self.ArrayViaje[index]
   
   def guardarRecorrido(self, index, recorrido):
      self.ArrayViaje[index] = recorrido
   
   def getAmbulante(self, index):
      return self.ArrayViaje[index]
   
   def evalFitness(self):
      fitness = self.ArrayViaje[0]
      fitnessIteracion = []  # Se almacena los valores de cada generación y es de 4 en 4
      pasaron = []
      val = 0
      valAnexados = []

      for i in range(0, tamPoblacion): # Iteraciones
         fitnessIteracion.append(self.getAmbulante(i).Fitness())

         if fitness.Fitness() <= self.getAmbulante(i).Fitness(): # Los mejores fitness Pasan y los que no -> sus valores son reemplazados
            fitness = self.getAmbulante(i)
            pasaron.append(fitness.Fitness()) # Los que pasaron se inserta en pasaron[] -> para luego de los que pasaron elegir el mejor
      
      # Esta parte es para seleccionar el mayor de los fitness seleccionados y se le agregagará al Array BestFitness
      for pfp2 in range(len(pasaron)):
         val = pasaron[pfp2]
         valAnexados.append(val)
         val = 0

      valAnexados = sorted(valAnexados)
      mayor = valAnexados[0]  # Mejor
      menor = valAnexados[0]  # Sólo lo uso para comparar los valores

      for numPasada in range(len(valAnexados)-1,0,-1):
         for i in range(numPasada):
               if valAnexados[i]>mayor:
                  temp = valAnexados[i]
                  valAnexados[i] = valAnexados[i+1]
                  valAnexados[i+1] = temp
                  valAnexados.append(mayor)


      BestBest.append(mayor)
      TotalFitness.append(fitnessIteracion)
      return fitness

class IAreporte:

   def __init__(self, controlViaje):
      self.controlViaje = controlViaje
   
   # De la evolucion de la Poblacion
   def evolucionP(self, pop):
      nuevaPoblacion = Poblacion(self.controlViaje, tamPoblacion, False)
      posEvol = 0
      if True:
         nuevaPoblacion.guardarRecorrido(0, pop.evalFitness())
         posEvol = 1
      
      for i in range(posEvol, tamPoblacion):
         parent1 = self.seleccion(pop)
         parent2 = self.seleccion(pop)
         hijos = self.crossover(parent1, parent2)
         nuevaPoblacion.guardarRecorrido(i, hijos) # Los padres son reemplazados por los hijos
      
      for i in range(posEvol, tamPoblacion):
         self.mutacion(nuevaPoblacion.getAmbulante(i))
      return nuevaPoblacion
   
   def crossover(self, parent1, parent2):
      hijos = Viaje(self.controlViaje)
      
      startPos = int(random.random() * numRuta)
      endPos = int(random.random() * numRuta)
      
      for i in range(0, numRuta):
         if startPos < endPos and i > startPos and i < endPos:
            hijos.setciudad(i, parent1.getciudad(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               hijos.setciudad(i, parent1.getciudad(i))
      
      for i in range(0, numRuta):
         if not hijos.containsciudad(parent2.getciudad(i)):
            for ii in range(0, numRuta):
               if hijos.getciudad(ii) == None:
                  hijos.setciudad(ii, parent2.getciudad(i))
                  break
      return hijos
   
   def mutacion(self, recorrido):
      for i in range(0, numRuta):
         if random.random() < probMutacion:
            pos2 = int(numRuta * random.random())
            
            ciudad1 = recorrido.getciudad(i)
            ciudad2 = recorrido.getciudad(pos2)
            
            recorrido.setciudad(pos2, ciudad1)
            recorrido.setciudad(i, ciudad2)
            pass
      
   
   def seleccion(self, pobla):
      select = Poblacion(controlViaje, tamTorne, False)
      for i in range(0, tamTorne):
         randomId = int(random.random() * tamPoblacion)
         select.guardarRecorrido(i, pobla.getAmbulante(randomId))
         pass
      fitness = select.evalFitness()
      return fitness

   def calDistancia(self, dataX, dataY):
      x1 = []
      y1 = []
      x2 = []
      y2 = []
      total = 0 
      for pff in range(1, len(dataX)):
         x2.append(dataX[pff])
         y2.append(dataY[pff])
         pass
      for ff in range(0, len(dataY)-1):
         x1.append(dataX[ff])
         y1.append(dataY[ff])
         pass

      for ff2 in range(len(x1)):
         d = math.sqrt(abs(((x2[ff2]-x1[ff2])*(x2[ff2]-x1[ff2])) + ((y2[ff2]-y1[ff2]) * (y2[ff2]-y1[ff2]))))
         total += d
         print("Distancias:  ", d, " --  De: ", x1[ff2],",",y1[ff2]," -- ", x2[ff2],",",y2[ff2])
         pass
      print("Total: ",total, "\n")
      return total

   def badFitFunction(self, data):
      valmal = 0
      valAnexadosmal = [] # Valores anexados de los Fitness

      for vm in range(len(data)):
         for vm2 in range(len(data[vm])):
            valmal = data[vm][vm2]
            valAnexadosmal.append(valmal)
            valmal = 0

         valAnexadosmal = sorted(valAnexadosmal)
         may = valAnexadosmal[0] # El valor del Mayor sólo lo uso para comparar los valores
         men = valAnexadosmal[0] # Peor
               
         for xx in range(0, len(valAnexadosmal)):
            if valAnexadosmal[xx] > may:
               may = valAnexadosmal[xx]
            else: 
               men = (valAnexadosmal[xx]/tamPoblacion)
         BadFitness.append(men) 
      return BadFitness

if __name__ == '__main__':
   controlViaje = ControlViaje()
   # Crear las ciudades
   for cc in range (15):
      pxx = random.randint(20,200)
      pyy = random.randint(20,200)
      ciudad = Ciudad(pxx, pyy)
      corInicialX.append(pxx)
      corInicialY.append(pyy)
      coordenadaInicial.append([pxx] + [pyy])
      controlViaje.addciudad(ciudad)
      pass
   print("\nInicial X: ", corInicialX)
   print("Inicial Y: ", corInicialY,"\n")
   print("Coordenada Inicial:  ",coordenadaInicial, "\n")

   # Poblacion Inicial
   pop = Poblacion(controlViaje, tamPoblacion, True)
   
   # Evolucion de la Poblacion  de los 50
   IAreporte = IAreporte(controlViaje)
   IAreporte.calDistancia(corInicialX, corInicialY) # Para la distancia Inicial

   pop = IAreporte.evolucionP(pop)
   for i in range(0, 100): #Evoluciona 100 veces
      pop = IAreporte.evolucionP(pop)
      pass

   BestFitness = sorted(BestBest) # Aca ya esta los mejores Fitness de cada Generación
   IAreporte.badFitFunction(TotalFitness)  # Para los peores de cada Generación
   print(BadFitness.sort(reverse=True))  


   #print("Total de Fitness:      ", TotalFitness, "\n")
   print("\n =================================          F   I  T  N  E  S  S        =================================\n")


   print("\n  -  -  -  -   F I  T  N  E  S  S           B - A - D     y     B - E - S - T     -  -  -  -  \n")     

   #  - - - - Para determinar el mejor y el peor FITNESS por generación - - - - -
   val2 = 0
   numGeneraciones = len(BestFitness)
   print("que verga hace esto")
   print(numGeneraciones)
   promedioFit = []   # Promedio de los Fitness de c/ Generación
   for i in range(len(TotalFitness)):
      for j in range(len(TotalFitness[i])):
         val2 += (TotalFitness[i][j]/tamPoblacion)  # PROMEDIO DE LOS FITNESS
      #print("\nPromedio Total del Fitness de C/Generación:    ", val2)
      promedioFit.append(val2)
      for numPasada in range(len(promedioFit)-1,0,-1):
         for i in range(numPasada):
               if promedioFit[i]>promedioFit[i+1]:
                  temp = promedioFit[i]
                  promedioFit[i] = promedioFit[i+1]
                  promedioFit[i+1] = temp
      
      val2 = 0
   promedio = sorted(promedioFit)
   


   grafic = []
   for xxx in range(0, len(BestFitness)):
      valor = (BestFitness[xxx] + BadFitness[xxx])/2
      grafic.append(valor)
      grafic = sorted(grafic)
   promedioFit = grafic

   print("\n  ->  P  E  O  R  :   Fitness: ", promedio[0], "\n")
   print("    ->  M E  J  O  R  :   Fitness: ", promedio[len(promedioFit)-1], "\n")

   print("\n - - - - -    T o  t  a  l        d  e     G  e  n  e  r  a  c  i  o  n  e  s    - - - - -", numGeneraciones,"\n")

   print(" =================================   R U  T  A        O  P  T  I  M  A  =================================")
   print(pop.evalFitness())
   print("\nFinal X  : ", cordFilaX)
   print("Final Y  : ", cordFinalY)
   print("\n - - - - - Distancia recorrida de la ruta Optimizada  - - - - - \n")
   IAreporte.calDistancia(cordFilaX, cordFinalY)  # Para la distancia Final


plt.subplot(1,3,1)
plt.plot(corInicialX, corInicialY, marker="o", color="r", linewidth=1.5, linestyle="-", label= " Coordenada Inicial ")
plt.subplot(1,3,2)
plt.plot(cordFilaX, cordFinalY, marker="o", color="g", linewidth=1.5, linestyle="-", label= "Coordenada Final ")
plt.subplot(1,3,3)
plt.plot(BadFitness, color="r", linewidth=1.5, linestyle="-", label= " Bad Fitness ") 
plt.plot(BestFitness, color="g", linewidth=1.5, linestyle="-", label= " Best Fitness ")   
plt.plot(promedioFit, color="b", linewidth=1.5, linestyle="-", label= "Promedio Fitness ") 
plt.show()



