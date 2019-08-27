#compare land and sea
verif land.nc sea.nc -l 34130 -m obsfcst -d 20160101:20160130

#compare land, sea and nearest neighbour
verif land.nc sea.nc nn.nc -l 34130 -m obsfcst -d 20160101:20160130

#check 



