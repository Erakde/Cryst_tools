from numpy import arcsin, sin, pi
from numpy import radians as rad
from numpy import degrees as deg


      
print("\
Radiation \t\t| Energy \t| Wavelenght \t|\n\
---------------------------------------------------------\n\
Copper (Cu K-alpha)\t| 8.0478 keV \t| λ = 1.54059 Å \t|\n\
Iron (Fe)\t\t| 6.3998 keV \t| λ = 1.93604 Å \t|\n\
Cobalt (Co)\t\t| 6.9257 keV \t| λ = 1.7902 Å \t|\n\
Molybdenum (Mo K-alpha)\t| 17.45  keV \t| λ = 0.70932 Å \t|")


element1, element2 = input("\nConvert from __ To __:  [e.g. Cu Mo]").strip().split()

radiation = {"Cu": 1.5406, "Fe": 1.9373, "Co": 1.7902, "Mo": 0.7107}

while True:
   tetha1 = input("2Tetha angle in "+element1+": ")
   λ1 = radiation.get(element1)
   λ2 = radiation.get(element2)

   argumento = (λ1/λ2)*sin(rad(float(tetha1)/2))
   tetha2 = deg(arcsin(argumento))
   print("2Tetha angle in "+ element2 + ": " + str(tetha2)+"\n")
