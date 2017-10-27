# EXO-SingleLQ3TauB-MCrequest

s-{mass} : s-channel process
t-{mass} : t-channel process

The production of the sample is baed on the recipes from theorist. 

===

1. Install latest Madgraph
https://launchpad.net/mg5amcnlo

2. copy UFO model (the one from Admir) under MG5_aMC_v2_6_0/models directory

3. preparation 

Launch madgraph in command line, 
> ./bin/mg5_aMC

 Then type followings, 

> import model Standard_Model+LQ_UFO/
> define p = p b b~

then, either 

> generate p p > r23 ta- 
or 
> "generate p p > r23 ta- , (r23 > b ta+)”

the latter is used when you want to let the LQ decay into other particle (in this case tau + b)

define similar thing to the anti-LQ, 

> add process p p > r23~ ta+
or 
> add process p p > r23~ ta+ , (r23~ > b~ ta-)

(For DY-like process, do, p p > ta+ ta- NP=2 QED=0)

then, 

> output SingleLQ
> open index.html 
> exit

You should now see “SingleLQ” directory created 



4. parameter modification

[4-1] edit "SingleLQ/Cards/param_card.dat” directory 

redefine parameter y1, y2 and y3. The meaning of this coupling constant is, 
y1: LQ couples to d + e
y2: LQ couples to s + mu
y3: LQ couples to b + tau

It is in the unit of GeV. For example, you can set y3 = 1, y1 = y2 = 0
to allow LQ only decays into tau + b

[4-2] LQ mass

modify this line
> 9000006 1.000000e+03 # Mr23

the unit is in GeV

[4-3] width is automatically determined following the formula

> (mr23*(abs(y1)**2 + abs(y2)**2 + abs(y3)**2))/(16.*cmath.pi)

so you don’t need to modify this 

[4-4] # of events to be generated 

edit 
> SingleLQ/Card/run_card.dat

check “cuts”, "5 flavour scheme", and "number of events"

5. run 

> ./bin/mg5_aMC
> launch SingleLQ (or the directory name you produced)

You will be asked some question by madgraph. Just press “enter” key

This should allow you to generate LHE files with specified number of events
