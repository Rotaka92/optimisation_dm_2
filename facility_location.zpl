# ZIMPL format

param graphfile := "man_data/man_laposte.txt";
param distance_graphfile := "man_data/man_laposte_distance.txt";

set V := { read graphfile as "<2n>" comment "p" };      # Crossroads
set P := { read graphfile as "<2n>" comment "v" };      # Possible post offices 
set V_CROSS_P := V * P;

param distances[V_CROSS_P] := read distance_graphfile as "<2n,3n> 4n";

var client[V_CROSS_P] binary;  # Is the client v going to the post office P ?
var open[P] binary;     # Is the post office P built ?

# We want to minimize the total distance

minimize cost: sum <p> in P: 500 * open[p]
             + sum <v,p> in V_CROSS_P: distances[v,p] * client[v, p];

subto assign:
    forall <v> in V do
        sum <p> in P: client[v, p] == 1;

subto build:
    forall <v,p> in V_CROSS_P do
        client[v,p] <= open[p];

subto initialize_post_office_1:
    open[283492455] == 1;

subto initialize_post_office_2:
    open[283494345] == 1;