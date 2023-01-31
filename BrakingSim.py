#--------------------------Simulation of the braking distance of a vehicle----------------------------------------------------------------------------------
# Course: Vehicle components and driving dynamics 
# Lecturer: Dr. Altinger
# Student:  Valerie Daroß, s2210710005, MeWi / Smart Mobility
# Task: - Simulate the braking distance and the velocity of a vehicle
#       - Use variance parameters: mass, velocity before braking, road type, wet or dry surface, inclination
#       - Compare simply physics model to driving lecture rule of thumb
#-------------------------1. define the varaince parameters: mass, velocity, road type, wet/dry, inclination------------------------------------------------
# inport argument parser
import argparse
import sys
# import mathematical operators
import math
# import matplotlib to plot functions
import matplotlib as mlp
import matplotlib.pyplot as plt
# import numpy
import numpy as np
import sympy
from sympy import *
# set up arcparser
# --help or -h shows the arguments
# -h appears also if there are no input values
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(argparse.ArgumentParser(description= "finds the variance parameters"))
parser.add_argument('m',metavar='m', type= float, choices =np.arange(0, 11, 0.01), help= 'Please enter the mass in tons')
parser.add_argument('v0', choices = np.arange(0, 500, 0.01),metavar='v0', type= float, help= 'Please enter the velocity in km/h')
parser.add_argument('rt', choices=[1,2,3,4,5], metavar='rt', type= int, help= 'Please enter the road type (only the number): concrete(1) / ice(2) / aquaplaning(3) / gravel(4) / sand(5)')
parser.add_argument('sur', choices=[1,2], metavar='sur', type= int, help= 'Please enter whether the surface is wet(1) / dry(2)(only the number)')
parser.add_argument('incl', choices=range(-51, 51),metavar='incl', type= float, help= 'Please enter the inclination in percent as an integer')
args = parser.parse_args()
print('The inputs are:')
print('Mass:', args.m, 't')
print('Velocity:', args.v0, 'km/h')
print('Road type:', args.rt,'(expl.: concrete(1), ice(2), aquaplaning(3), gravel(4), sand(5))')
print('Surface:', args.sur, '(expl: wet(1), dry(2))')
print('Inclination:', args.incl, '%')
#-------------------------2. Derive formulars to calculate the braking distance from simple physics model ------------------------------------------------
# function to calculate the braking time with the simplified physical model
# Assign arguments to variables:
# velocity before braking in m/s:
v0 = args.v0/3.6
# inclination in degrees:
alpha = math.degrees(np.arctan(args.incl/100))
# my, depending on road surface:
if args.rt == 1 and args.sur == 1:
    my = 0.35
elif args.rt == 1 and args.sur == 2:
    my = 0.5
elif args.rt == 2 and args.sur == 1:
    my = 0.08
elif args.rt == 2 and args.sur == 2:
    my = 0.15
elif args.rt == 3:
    my = 0.05
elif args.rt == 4:
    my = 0.35
elif args.rt == 5:
    my = 0.3
# gravity:
g = 9.81
# Derive formulars for simple physics model:
# deacceleration including the inclination:
a = my*g*np.cos(alpha*np.pi/180)+g*np.sin(alpha * np.pi/180)
if a > 0:
    # vehicle is able to stop
    stop = True
    # time needed for braking, including 1 second as a reaction time
    tbr = (v0 / a) 
    tbr2 = (v0 / a) + 1
    # distance during reaction time:
    s0 = v0 * 1
    # distance for braking:
    s = v0*tbr-((1/2)*a*(tbr**2))
    # Distance including the reaction time:
    s2 = s0+v0*tbr-((1/2)*a*(tbr**2))
    print('\n')
    print('Calculation with simple physics  model:')
    print ('The time needed for braking is', round(tbr,2), 'seconds.')
    print ('The braking distance is', round(s,2),  'meters.')
    print ('Calculating one second as the reaction time:') 
    print ('The time needed for braking is',round(tbr2,2),'seconds.')
    print ('The braking distance is',round(s2,2),'meters.') 
else:
    print('Calculation with simple physics  model:')
    print('Due to these parameters the vehicle cannot be stopped.')
    # Vehicle is not able to stop
    stop = False

#-------------------------3. Derive formulars to calculate the braking distance from the rule of thumbs-------------------------------------------------
# function to calculate the braking time with the rule of thumb
# plots the functions for velocity and distance for the rule of thumb
# starting velocity
v02 = args.v0
# normal breaking distance
sn = (v02/10)**2
# breaking distance in danger
sd = ((v02/10)**2)/2
# breaking distance 
sr = (v02/10)*3
print('\n')
print('Calculation with rule of thumb:')
print('The normal braking distance is', round(sn,2), 'meters.')
print('The braking distance including the reaction time is', round((sn+sr),2),'meters.')
print('The braking distance in danger is', round((sr+sd),2),'meters.')
#---------------------------4. Plot the diagrams-------------------------------------------------------------------------------------------------------
# check if vehicle will stop
if stop == True:
    steps=200
    t = np.linspace(0, tbr+1, steps)
    # 1st graph for the velocity
    # use piecewise to include the reaction time
    v = np.piecewise(t,[t<=1, t>1],[v0, lambda i: v0 -(i-1)*a])
    fig, ax1 = plt.subplots()
    color = 'tab:blue'  
    ax1.set_xlabel('Beaking time in s')  
    ax1.set_ylabel('Velocity in m/s', color = color)  
    ax1.plot(t, v, color = color)  
    ax1.tick_params(axis ='y', labelcolor = color)

    # 2nd graph for the distance
    ax2 = ax1.twinx()  
    # use piecewise to include the reaction time
    s = np.piecewise(t,[t<1, t>=1],[lambda i: v0*i, lambda i: (v0*1) + v0*(i-1)-((1/2)*a*((i-1)**2))])
    color = 'tab:green'
    ax2.set_ylabel('Beaking distance in m', color = color)  
    ax2.plot(t, s, color = color)  
    ax2.tick_params(axis ='y', labelcolor = color)  
    plt.title('Breaking velocity and distance over time')
    plt.show()



