# Facility Location Problem

This project deals with the Facility Location problem

You kind find the exercice [here](http://www-desir.lip6.fr/~durrc/Iut/optim/t/dm2-laposte)

## Getting started

Run the script below to calculate the potential post offices and the distances:
```
$ python main.py
```

This command creates or updates the two following files:
- [man_data/man_laposte.txt](man_data/man_laposte.txt):
..* ```v crossroad_id long lat``` : list of all the crossroads (with inhabitants) (5358)
..* ```p post_office_id``` : list of all the potential post offices (125)
- [man_data/man_laposte_distance.txt](man_data/man_laposte_distance.txt)
..** ```d crossroad_id post_office_id distance``` : list of all the distances between one inhabitant and one post office

Run the script below to solve the problem with SCIP and save the results in [results/facility_location.txt](results/facility_location.txt):
```
$ scip -c "read facility_location.zpl  optimize  display sols 0 quit" -l "results/facility_location.txt"
```

## Results :

We found that 13 post offices is the optimal solution:

|  # | crossroad id |
|----|--------------|
|  1 |    283478116 |
|  2 |    283483352 |
|  3 |    283484290 |
|  4 |    283492455 |
|  5 |    283494345 |
|  6 |    283498929 |
|  7 |    283508235 |
|  8 |    283511482 |
|  9 |    283511666 |
| 10 |    283520651 |
| 11 |    283523904 |
| 12 |    283523918 |
| 13 |   1110284545 |

Extract from [results/facility_location.txt](results/facility_location.txt):

```
open#283478116                                      1   (obj:500)
open#283483352                                      1   (obj:500)
open#283484290                                      1   (obj:500)
open#283492455                                      1   (obj:500)
open#283494345                                      1   (obj:500)
open#283498929                                      1   (obj:500)
open#283508235                                      1   (obj:500)
open#283511482                                      1   (obj:500)
open#283511666                                      1   (obj:500)
open#283520651                                      1   (obj:500)
open#283523904                                      1   (obj:500)
open#283523918                                      1   (obj:500)
open#1110284545                                     1   (obj:500)
```

## Authors

Melanie Berard