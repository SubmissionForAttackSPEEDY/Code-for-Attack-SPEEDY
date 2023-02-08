# Code-for-Attack-SPEEDY
the Code for ACISP 2023 submission __Cryptanalysis of SPEEDY__.

Contain three parts, $i.e.$ the calculation of FTDDT， the code of generating cvc file for differential attack and linear attack. Users need to install STP (https://stp.github.io/) in advance.

If you want to obtain the cvc file of the firsttrail in differential attack, the code to run is as follows:

```
cd DifferentialAttack/FirstTrail/

python3 SPEEDY_Differential_FirstTrail_CVCmake.py
```

Then, run

```
nohup stp SPEEDY_Differential_FirstTrail.cvc --cryptominisat --threads 8 >SPEEDY_Differential_FirstTrail.txt &
```

to get the solution. It might take some time, usually several hours.

Finally, run 

```
python3 ExtractTrail.py
```
to get a visualization of the attack trail.
