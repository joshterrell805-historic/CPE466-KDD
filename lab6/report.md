#data/1000/1000-out1.csv
1000 rows from data/1000/1000-out1.csv with `min_sup`=0.01 and `min_conf=0.65

##Skyline frequent itemsets
~~~
Itemset 0:
	Contains: AlmondBear Claw
	Support: 0.026
Itemset 1:
	Contains: ChocolateMeringue
	Support: 0.038
Itemset 2:
	Contains: GanacheCookie
	Support: 0.044
Itemset 3:
	Contains: VanillaMeringue
	Support: 0.047
Itemset 4:
	Contains: AlmondTart
	Support: 0.041
Itemset 5:
	Contains: AlmondCroissant
	Support: 0.049
Itemset 6:
	Contains: BlueberryDanish
	Support: 0.055
Itemset 7:
	Contains: PecanTart
	Support: 0.04
Itemset 8:
	Contains: VanillaEclair
	Support: 0.037
Itemset 9:
	Contains: ChocolateCroissant
	Support: 0.042
Itemset 10:
	Contains: ChocolateEclair
	Support: 0.034
Itemset 11:
	Contains: NapoleonCake, ApricotTart
	Support: 0.01
Itemset 12:
	Contains: NapoleonCake, HotCoffee
	Support: 0.01
Itemset 13:
	Contains: MarzipanCookie, TuileCookie
	Support: 0.053
Itemset 14:
	Contains: OrangeJuice, TruffleCake
	Support: 0.01
Itemset 15:
	Contains: NapoleonCake, StrawberryCake
	Support: 0.049
Itemset 16:
	Contains: LemonCake, LemonTart
	Support: 0.04
Itemset 17:
	Contains: TruffleCake, AppleCroissant
	Support: 0.01
Itemset 18:
	Contains: BottledWater, BerryTart
	Support: 0.034
Itemset 19:
	Contains: TruffleCake, BerryTart
	Support: 0.013
Itemset 20:
	Contains: CheeseCroissant, OrangeJuice
	Support: 0.038
Itemset 21:
	Contains: CheeseCroissant, RaspberryCookie
	Support: 0.01
Itemset 22:
	Contains: GongolaisCookie, BerryTart
	Support: 0.012
Itemset 23:
	Contains: OrangeJuice, RaspberryCookie
	Support: 0.011
Itemset 24:
	Contains: TruffleCake, GongolaisCookie
	Support: 0.058
Itemset 25:
	Contains: ApricotCroissant, BlueberryTart, HotCoffee
	Support: 0.032
Itemset 26:
	Contains: CoffeeEclair, SingleEspresso, BlackberryTart
	Support: 0.023
Itemset 27:
	Contains: ChocolateCake, CasinoCake, ChocolateCoffee
	Support: 0.038
Itemset 28:
	Contains: ChocolateTart, WalnutCookie, VanillaFrappuccino
	Support: 0.018
Itemset 29:
	Contains: CherryTart, ApricotDanish, OperaCake
	Support: 0.038
Itemset 30:
	Contains: CherrySoda, AppleDanish, AppleTart, AppleCroissant
	Support: 0.031
Itemset 31:
	Contains: AlmondTwist, CoffeeEclair, ApplePie, HotCoffee
	Support: 0.024
Itemset 32:
	Contains: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie, LemonCookie
	Support: 0.019
~~~

##Skyline association rules
~~~
Rule 0:
	LHS: BlueberryTart, HotCoffee
	RHS: ApricotCroissant
	Support: 3.2
	Confidence: 96.96969696969697
Rule 1:
	LHS: ApricotCroissant, HotCoffee
	RHS: BlueberryTart
	Support: 3.2
	Confidence: 100.0
Rule 2:
	LHS: ApricotCroissant, BlueberryTart
	RHS: HotCoffee
	Support: 3.2
	Confidence: 80.0
Rule 3:
	LHS: SingleEspresso, BlackberryTart
	RHS: CoffeeEclair
	Support: 2.3
	Confidence: 95.83333333333333
Rule 4:
	LHS: BlackberryTart, CoffeeEclair
	RHS: SingleEspresso
	Support: 2.3
	Confidence: 74.19354838709677
Rule 5:
	LHS: SingleEspresso, CoffeeEclair
	RHS: BlackberryTart
	Support: 2.3
	Confidence: 95.83333333333333
Rule 6:
	LHS: CasinoCake, ChocolateCoffee
	RHS: ChocolateCake
	Support: 3.8
	Confidence: 97.43589743589743
Rule 7:
	LHS: ChocolateCake, ChocolateCoffee
	RHS: CasinoCake
	Support: 3.8
	Confidence: 80.85106382978722
Rule 8:
	LHS: ChocolateCake, CasinoCake
	RHS: ChocolateCoffee
	Support: 3.8
	Confidence: 95.0
Rule 9:
	LHS: WalnutCookie, VanillaFrappuccino
	RHS: ChocolateTart
	Support: 1.7999999999999998
	Confidence: 100.0
Rule 10:
	LHS: ChocolateTart, VanillaFrappuccino
	RHS: WalnutCookie
	Support: 1.7999999999999998
	Confidence: 69.23076923076923
Rule 11:
	LHS: ChocolateTart, WalnutCookie
	RHS: VanillaFrappuccino
	Support: 1.7999999999999998
	Confidence: 100.0
Rule 12:
	LHS: ApricotDanish, OperaCake
	RHS: CherryTart
	Support: 3.8
	Confidence: 97.43589743589743
Rule 13:
	LHS: CherryTart, OperaCake
	RHS: ApricotDanish
	Support: 3.8
	Confidence: 92.68292682926828
Rule 14:
	LHS: CherryTart, ApricotDanish
	RHS: OperaCake
	Support: 3.8
	Confidence: 82.6086956521739
Rule 15:
	LHS: AppleDanish, AppleTart, AppleCroissant
	RHS: CherrySoda
	Support: 3.1
	Confidence: 77.5
Rule 16:
	LHS: CherrySoda, AppleTart, AppleCroissant
	RHS: AppleDanish
	Support: 3.1
	Confidence: 100.0
Rule 17:
	LHS: CherrySoda, AppleDanish, AppleCroissant
	RHS: AppleTart
	Support: 3.1
	Confidence: 100.0
Rule 18:
	LHS: CherrySoda, AppleDanish, AppleTart
	RHS: AppleCroissant
	Support: 3.1
	Confidence: 100.0
Rule 19:
	LHS: ApplePie, HotCoffee, CoffeeEclair
	RHS: AlmondTwist
	Support: 2.4
	Confidence: 100.0
Rule 20:
	LHS: ApplePie, AlmondTwist, HotCoffee
	RHS: CoffeeEclair
	Support: 2.4
	Confidence: 100.0
Rule 21:
	LHS: AlmondTwist, HotCoffee, CoffeeEclair
	RHS: ApplePie
	Support: 2.4
	Confidence: 100.0
Rule 22:
	LHS: ApplePie, AlmondTwist, CoffeeEclair
	RHS: HotCoffee
	Support: 2.4
	Confidence: 88.8888888888889
Rule 23:
	LHS: LemonCookie, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonLemonade
	Support: 1.9
	Confidence: 100.0
Rule 24:
	LHS: LemonLemonade, LemonCookie, GreenTea, RaspberryCookie
	RHS: RaspberryLemonade
	Support: 1.9
	Confidence: 100.0
Rule 25:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, RaspberryCookie
	RHS: GreenTea
	Support: 1.9
	Confidence: 67.85714285714285
Rule 26:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, GreenTea
	RHS: RaspberryCookie
	Support: 1.9
	Confidence: 100.0
Rule 27:
	LHS: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonCookie
	Support: 1.9
	Confidence: 100.0
~~~

#data/5000/5000-out1.csv
5000 rows from data/5000/5000-out1.csv with `min_sup`=0.01 and `min_conf=0.7

##Skyline frequent itemsets
~~~
Itemset 0:
	Contains: AlmondBear Claw
	Support: 0.0428
Itemset 1:
	Contains: ChocolateMeringue
	Support: 0.0452
Itemset 2:
	Contains: GanacheCookie
	Support: 0.0388
Itemset 3:
	Contains: VanillaMeringue
	Support: 0.0398
Itemset 4:
	Contains: AlmondTart
	Support: 0.0386
Itemset 5:
	Contains: AlmondCroissant
	Support: 0.0456
Itemset 6:
	Contains: BlueberryDanish
	Support: 0.04
Itemset 7:
	Contains: PecanTart
	Support: 0.0444
Itemset 8:
	Contains: ApricotTart
	Support: 0.0422
Itemset 9:
	Contains: VanillaEclair
	Support: 0.046
Itemset 10:
	Contains: ChocolateCroissant
	Support: 0.0432
Itemset 11:
	Contains: ChocolateEclair
	Support: 0.0382
Itemset 12:
	Contains: CheeseCroissant, OrangeJuice
	Support: 0.043
Itemset 13:
	Contains: MarzipanCookie, TuileCookie
	Support: 0.0496
Itemset 14:
	Contains: TruffleCake, GongolaisCookie
	Support: 0.0472
Itemset 15:
	Contains: NapoleonCake, StrawberryCake
	Support: 0.0422
Itemset 16:
	Contains: LemonCake, LemonTart
	Support: 0.0336
Itemset 17:
	Contains: BottledWater, BerryTart
	Support: 0.0366
Itemset 18:
	Contains: ApricotCroissant, BlueberryTart, HotCoffee
	Support: 0.0328
Itemset 19:
	Contains: CoffeeEclair, SingleEspresso, BlackberryTart
	Support: 0.0286
Itemset 20:
	Contains: ChocolateCake, CasinoCake, ChocolateCoffee
	Support: 0.0312
Itemset 21:
	Contains: ChocolateTart, WalnutCookie, VanillaFrappuccino
	Support: 0.0266
Itemset 22:
	Contains: CherryTart, ApricotDanish, OperaCake
	Support: 0.0408
Itemset 23:
	Contains: CherrySoda, AppleDanish, AppleTart, AppleCroissant
	Support: 0.0228
Itemset 24:
	Contains: AlmondTwist, CoffeeEclair, ApplePie, HotCoffee
	Support: 0.0308
Itemset 25:
	Contains: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie, LemonCookie
	Support: 0.0212
~~~

##Skyline association rules
~~~
Rule 0:
	LHS: BlueberryTart, HotCoffee
	RHS: ApricotCroissant
	Support: 3.2800000000000002
	Confidence: 93.71428571428572
Rule 1:
	LHS: ApricotCroissant, HotCoffee
	RHS: BlueberryTart
	Support: 3.2800000000000002
	Confidence: 94.25287356321842
Rule 2:
	LHS: ApricotCroissant, BlueberryTart
	RHS: HotCoffee
	Support: 3.2800000000000002
	Confidence: 74.54545454545456
Rule 3:
	LHS: SingleEspresso, BlackberryTart
	RHS: CoffeeEclair
	Support: 2.86
	Confidence: 91.08280254777071
Rule 4:
	LHS: BlackberryTart, CoffeeEclair
	RHS: SingleEspresso
	Support: 2.86
	Confidence: 80.33707865168539
Rule 5:
	LHS: SingleEspresso, CoffeeEclair
	RHS: BlackberryTart
	Support: 2.86
	Confidence: 96.62162162162163
Rule 6:
	LHS: CasinoCake, ChocolateCoffee
	RHS: ChocolateCake
	Support: 3.1199999999999997
	Confidence: 90.17341040462428
Rule 7:
	LHS: ChocolateCake, ChocolateCoffee
	RHS: CasinoCake
	Support: 3.1199999999999997
	Confidence: 79.18781725888326
Rule 8:
	LHS: ChocolateCake, CasinoCake
	RHS: ChocolateCoffee
	Support: 3.1199999999999997
	Confidence: 91.22807017543859
Rule 9:
	LHS: WalnutCookie, VanillaFrappuccino
	RHS: ChocolateTart
	Support: 2.6599999999999997
	Confidence: 89.26174496644295
Rule 10:
	LHS: ChocolateTart, VanillaFrappuccino
	RHS: WalnutCookie
	Support: 2.6599999999999997
	Confidence: 76.4367816091954
Rule 11:
	LHS: ChocolateTart, WalnutCookie
	RHS: VanillaFrappuccino
	Support: 2.6599999999999997
	Confidence: 93.006993006993
Rule 12:
	LHS: ApricotDanish, OperaCake
	RHS: CherryTart
	Support: 4.08
	Confidence: 94.44444444444444
Rule 13:
	LHS: CherryTart, OperaCake
	RHS: ApricotDanish
	Support: 4.08
	Confidence: 93.57798165137615
Rule 14:
	LHS: CherryTart, ApricotDanish
	RHS: OperaCake
	Support: 4.08
	Confidence: 79.6875
Rule 15:
	LHS: AppleDanish, AppleTart, AppleCroissant
	RHS: CherrySoda
	Support: 2.2800000000000002
	Confidence: 76.51006711409396
Rule 16:
	LHS: CherrySoda, AppleTart, AppleCroissant
	RHS: AppleDanish
	Support: 2.2800000000000002
	Confidence: 99.1304347826087
Rule 17:
	LHS: CherrySoda, AppleDanish, AppleCroissant
	RHS: AppleTart
	Support: 2.2800000000000002
	Confidence: 99.1304347826087
Rule 18:
	LHS: CherrySoda, AppleDanish, AppleTart
	RHS: AppleCroissant
	Support: 2.2800000000000002
	Confidence: 100.0
Rule 19:
	LHS: ApplePie, HotCoffee, CoffeeEclair
	RHS: AlmondTwist
	Support: 3.08
	Confidence: 100.0
Rule 20:
	LHS: ApplePie, AlmondTwist, HotCoffee
	RHS: CoffeeEclair
	Support: 3.08
	Confidence: 100.0
Rule 21:
	LHS: AlmondTwist, HotCoffee, CoffeeEclair
	RHS: ApplePie
	Support: 3.08
	Confidence: 100.0
Rule 22:
	LHS: ApplePie, AlmondTwist, CoffeeEclair
	RHS: HotCoffee
	Support: 3.08
	Confidence: 80.62827225130891
Rule 23:
	LHS: LemonCookie, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonLemonade
	Support: 2.12
	Confidence: 100.0
Rule 24:
	LHS: LemonLemonade, LemonCookie, GreenTea, RaspberryCookie
	RHS: RaspberryLemonade
	Support: 2.12
	Confidence: 100.0
Rule 25:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, RaspberryCookie
	RHS: GreenTea
	Support: 2.12
	Confidence: 80.91603053435115
Rule 26:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, GreenTea
	RHS: RaspberryCookie
	Support: 2.12
	Confidence: 100.0
Rule 27:
	LHS: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonCookie
	Support: 2.12
	Confidence: 100.0
~~~

#data/20000/20000-out1.csv
20000 rows from data/20000/20000-out1.csv with `min_sup`=0.01 and `min_conf=0.7

##Skyline frequent itemsets
~~~
Itemset 0:
	Contains: AlmondBear Claw
	Support: 0.04425
Itemset 1:
	Contains: ChocolateMeringue
	Support: 0.0445
Itemset 2:
	Contains: GanacheCookie
	Support: 0.0433
Itemset 3:
	Contains: VanillaMeringue
	Support: 0.0424
Itemset 4:
	Contains: AlmondTart
	Support: 0.04055
Itemset 5:
	Contains: AlmondCroissant
	Support: 0.04205
Itemset 6:
	Contains: BlueberryDanish
	Support: 0.04115
Itemset 7:
	Contains: PecanTart
	Support: 0.04155
Itemset 8:
	Contains: ApricotTart
	Support: 0.04275
Itemset 9:
	Contains: VanillaEclair
	Support: 0.0427
Itemset 10:
	Contains: ChocolateCroissant
	Support: 0.0446
Itemset 11:
	Contains: ChocolateEclair
	Support: 0.0426
Itemset 12:
	Contains: CheeseCroissant, OrangeJuice
	Support: 0.0439
Itemset 13:
	Contains: MarzipanCookie, TuileCookie
	Support: 0.04855
Itemset 14:
	Contains: TruffleCake, GongolaisCookie
	Support: 0.04335
Itemset 15:
	Contains: NapoleonCake, StrawberryCake
	Support: 0.04455
Itemset 16:
	Contains: LemonCake, LemonTart
	Support: 0.037
Itemset 17:
	Contains: BottledWater, BerryTart
	Support: 0.0357
Itemset 18:
	Contains: ApricotCroissant, BlueberryTart, HotCoffee
	Support: 0.0326
Itemset 19:
	Contains: CoffeeEclair, SingleEspresso, BlackberryTart
	Support: 0.02695
Itemset 20:
	Contains: ChocolateCake, CasinoCake, ChocolateCoffee
	Support: 0.0339
Itemset 21:
	Contains: ChocolateTart, WalnutCookie, VanillaFrappuccino
	Support: 0.02825
Itemset 22:
	Contains: CherryTart, ApricotDanish, OperaCake
	Support: 0.041
Itemset 23:
	Contains: CherrySoda, AppleDanish, AppleTart, AppleCroissant
	Support: 0.021
Itemset 24:
	Contains: AlmondTwist, CoffeeEclair, ApplePie, HotCoffee
	Support: 0.0281
Itemset 25:
	Contains: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie, LemonCookie
	Support: 0.0204
~~~

##Skyline association rules
~~~
Rule 0:
	LHS: BlueberryTart, HotCoffee
	RHS: ApricotCroissant
	Support: 3.26
	Confidence: 91.31652661064425
Rule 1:
	LHS: ApricotCroissant, HotCoffee
	RHS: BlueberryTart
	Support: 3.26
	Confidence: 92.87749287749287
Rule 2:
	LHS: ApricotCroissant, BlueberryTart
	RHS: HotCoffee
	Support: 3.26
	Confidence: 77.89725209080048
Rule 3:
	LHS: SingleEspresso, BlackberryTart
	RHS: CoffeeEclair
	Support: 2.6950000000000003
	Confidence: 89.38640132669984
Rule 4:
	LHS: BlackberryTart, CoffeeEclair
	RHS: SingleEspresso
	Support: 2.6950000000000003
	Confidence: 73.33333333333334
Rule 5:
	LHS: SingleEspresso, CoffeeEclair
	RHS: BlackberryTart
	Support: 2.6950000000000003
	Confidence: 91.97952218430035
Rule 6:
	LHS: CasinoCake, ChocolateCoffee
	RHS: ChocolateCake
	Support: 3.39
	Confidence: 94.9579831932773
Rule 7:
	LHS: ChocolateCake, ChocolateCoffee
	RHS: CasinoCake
	Support: 3.39
	Confidence: 76.95800227014756
Rule 8:
	LHS: ChocolateCake, CasinoCake
	RHS: ChocolateCoffee
	Support: 3.39
	Confidence: 94.56066945606695
Rule 9:
	LHS: WalnutCookie, VanillaFrappuccino
	RHS: ChocolateTart
	Support: 2.825
	Confidence: 91.27625201938612
Rule 10:
	LHS: ChocolateTart, VanillaFrappuccino
	RHS: WalnutCookie
	Support: 2.825
	Confidence: 76.87074829931973
Rule 11:
	LHS: ChocolateTart, WalnutCookie
	RHS: VanillaFrappuccino
	Support: 2.825
	Confidence: 92.47135842880525
Rule 12:
	LHS: ApricotDanish, OperaCake
	RHS: CherryTart
	Support: 4.1000000000000005
	Confidence: 94.57900807381777
Rule 13:
	LHS: CherryTart, OperaCake
	RHS: ApricotDanish
	Support: 4.1000000000000005
	Confidence: 93.92898052691866
Rule 14:
	LHS: CherryTart, ApricotDanish
	RHS: OperaCake
	Support: 4.1000000000000005
	Confidence: 78.0209324452902
Rule 15:
	LHS: AppleDanish, AppleTart, AppleCroissant
	RHS: CherrySoda
	Support: 2.1
	Confidence: 80.76923076923079
Rule 16:
	LHS: CherrySoda, AppleTart, AppleCroissant
	RHS: AppleDanish
	Support: 2.1
	Confidence: 99.29078014184398
Rule 17:
	LHS: CherrySoda, AppleDanish, AppleCroissant
	RHS: AppleTart
	Support: 2.1
	Confidence: 98.82352941176471
Rule 18:
	LHS: CherrySoda, AppleDanish, AppleTart
	RHS: AppleCroissant
	Support: 2.1
	Confidence: 99.5260663507109
Rule 19:
	LHS: ApplePie, HotCoffee, CoffeeEclair
	RHS: AlmondTwist
	Support: 2.81
	Confidence: 99.64539007092199
Rule 20:
	LHS: ApplePie, AlmondTwist, HotCoffee
	RHS: CoffeeEclair
	Support: 2.81
	Confidence: 99.46902654867257
Rule 21:
	LHS: AlmondTwist, HotCoffee, CoffeeEclair
	RHS: ApplePie
	Support: 2.81
	Confidence: 99.82238010657193
Rule 22:
	LHS: ApplePie, AlmondTwist, CoffeeEclair
	RHS: HotCoffee
	Support: 2.81
	Confidence: 82.28404099560761
Rule 23:
	LHS: LemonCookie, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonLemonade
	Support: 2.04
	Confidence: 100.0
Rule 24:
	LHS: LemonLemonade, LemonCookie, GreenTea, RaspberryCookie
	RHS: RaspberryLemonade
	Support: 2.04
	Confidence: 100.0
Rule 25:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, RaspberryCookie
	RHS: GreenTea
	Support: 2.04
	Confidence: 80.15717092337918
Rule 26:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, GreenTea
	RHS: RaspberryCookie
	Support: 2.04
	Confidence: 99.75550122249389
Rule 27:
	LHS: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonCookie
	Support: 2.04
	Confidence: 99.75550122249389
~~~

#data/75000/75000-out1.csv
75000 rows from data/75000/75000-out1.csv with `min_sup`=0.01 and `min_conf=0.7

##Skyline frequent itemsets
~~~
Itemset 0:
	Contains: AlmondBear Claw
	Support: 0.04244
Itemset 1:
	Contains: ChocolateMeringue
	Support: 0.041933333333333336
Itemset 2:
	Contains: GanacheCookie
	Support: 0.04324
Itemset 3:
	Contains: VanillaMeringue
	Support: 0.04238666666666667
Itemset 4:
	Contains: AlmondTart
	Support: 0.04204
Itemset 5:
	Contains: AlmondCroissant
	Support: 0.04273333333333333
Itemset 6:
	Contains: BlueberryDanish
	Support: 0.04409333333333333
Itemset 7:
	Contains: PecanTart
	Support: 0.04337333333333333
Itemset 8:
	Contains: ApricotTart
	Support: 0.04236
Itemset 9:
	Contains: VanillaEclair
	Support: 0.04252
Itemset 10:
	Contains: ChocolateCroissant
	Support: 0.04324
Itemset 11:
	Contains: ChocolateEclair
	Support: 0.04237333333333333
Itemset 12:
	Contains: CheeseCroissant, OrangeJuice
	Support: 0.04306666666666667
Itemset 13:
	Contains: MarzipanCookie, TuileCookie
	Support: 0.05092
Itemset 14:
	Contains: TruffleCake, GongolaisCookie
	Support: 0.04392
Itemset 15:
	Contains: NapoleonCake, StrawberryCake
	Support: 0.043146666666666667
Itemset 16:
	Contains: LemonCake, LemonTart
	Support: 0.036853333333333335
Itemset 17:
	Contains: BottledWater, BerryTart
	Support: 0.0378
Itemset 18:
	Contains: ApricotCroissant, BlueberryTart, HotCoffee
	Support: 0.032826666666666664
Itemset 19:
	Contains: CoffeeEclair, SingleEspresso, BlackberryTart
	Support: 0.0272
Itemset 20:
	Contains: ChocolateCake, CasinoCake, ChocolateCoffee
	Support: 0.03338666666666667
Itemset 21:
	Contains: ChocolateTart, WalnutCookie, VanillaFrappuccino
	Support: 0.02676
Itemset 22:
	Contains: CherryTart, ApricotDanish, OperaCake
	Support: 0.041106666666666666
Itemset 23:
	Contains: CherrySoda, AppleDanish, AppleTart, AppleCroissant
	Support: 0.020586666666666666
Itemset 24:
	Contains: AlmondTwist, CoffeeEclair, ApplePie, HotCoffee
	Support: 0.02792
Itemset 25:
	Contains: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie, LemonCookie
	Support: 0.020733333333333333
~~~

##Skyline association rules
~~~
Rule 0:
	LHS: BlueberryTart, HotCoffee
	RHS: ApricotCroissant
	Support: 3.282666666666666
	Confidence: 93.68340943683408
Rule 1:
	LHS: ApricotCroissant, HotCoffee
	RHS: BlueberryTart
	Support: 3.282666666666666
	Confidence: 92.80060309084055
Rule 2:
	LHS: ApricotCroissant, BlueberryTart
	RHS: HotCoffee
	Support: 3.282666666666666
	Confidence: 75.4520380018388
Rule 3:
	LHS: SingleEspresso, BlackberryTart
	RHS: CoffeeEclair
	Support: 2.7199999999999998
	Confidence: 92.3076923076923
Rule 4:
	LHS: BlackberryTart, CoffeeEclair
	RHS: SingleEspresso
	Support: 2.7199999999999998
	Confidence: 74.697912852435
Rule 5:
	LHS: SingleEspresso, CoffeeEclair
	RHS: BlackberryTart
	Support: 2.7199999999999998
	Confidence: 92.2242314647378
Rule 6:
	LHS: CasinoCake, ChocolateCoffee
	RHS: ChocolateCake
	Support: 3.3386666666666667
	Confidence: 94.74082482027998
Rule 7:
	LHS: ChocolateCake, ChocolateCoffee
	RHS: CasinoCake
	Support: 3.3386666666666667
	Confidence: 75.8098698153194
Rule 8:
	LHS: ChocolateCake, CasinoCake
	RHS: ChocolateCoffee
	Support: 3.3386666666666667
	Confidence: 93.95872420262664
Rule 9:
	LHS: WalnutCookie, VanillaFrappuccino
	RHS: ChocolateTart
	Support: 2.6759999999999997
	Confidence: 93.96067415730337
Rule 10:
	LHS: ChocolateTart, VanillaFrappuccino
	RHS: WalnutCookie
	Support: 2.6759999999999997
	Confidence: 74.41601779755284
Rule 11:
	LHS: ChocolateTart, WalnutCookie
	RHS: VanillaFrappuccino
	Support: 2.6759999999999997
	Confidence: 93.69747899159664
Rule 12:
	LHS: ApricotDanish, OperaCake
	RHS: CherryTart
	Support: 4.110666666666667
	Confidence: 95.53765106910444
Rule 13:
	LHS: CherryTart, OperaCake
	RHS: ApricotDanish
	Support: 4.110666666666667
	Confidence: 94.77405471872117
Rule 14:
	LHS: CherryTart, ApricotDanish
	RHS: OperaCake
	Support: 4.110666666666667
	Confidence: 77.42340532395781
Rule 15:
	LHS: AppleDanish, AppleTart, AppleCroissant
	RHS: CherrySoda
	Support: 2.0586666666666664
	Confidence: 80.7109252483011
Rule 16:
	LHS: CherrySoda, AppleTart, AppleCroissant
	RHS: AppleDanish
	Support: 2.0586666666666664
	Confidence: 99.10141206675223
Rule 17:
	LHS: CherrySoda, AppleDanish, AppleCroissant
	RHS: AppleTart
	Support: 2.0586666666666664
	Confidence: 98.97435897435898
Rule 18:
	LHS: CherrySoda, AppleDanish, AppleTart
	RHS: AppleCroissant
	Support: 2.0586666666666664
	Confidence: 99.29260450160771
Rule 19:
	LHS: ApplePie, HotCoffee, CoffeeEclair
	RHS: AlmondTwist
	Support: 2.792
	Confidence: 99.38300901756051
Rule 20:
	LHS: ApplePie, AlmondTwist, HotCoffee
	RHS: CoffeeEclair
	Support: 2.792
	Confidence: 99.52471482889734
Rule 21:
	LHS: AlmondTwist, HotCoffee, CoffeeEclair
	RHS: ApplePie
	Support: 2.792
	Confidence: 99.28876244665719
Rule 22:
	LHS: ApplePie, AlmondTwist, CoffeeEclair
	RHS: HotCoffee
	Support: 2.792
	Confidence: 81.35198135198135
Rule 23:
	LHS: LemonCookie, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonLemonade
	Support: 2.0733333333333333
	Confidence: 100.0
Rule 24:
	LHS: LemonLemonade, LemonCookie, GreenTea, RaspberryCookie
	RHS: RaspberryLemonade
	Support: 2.0733333333333333
	Confidence: 100.0
Rule 25:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, RaspberryCookie
	RHS: GreenTea
	Support: 2.0733333333333333
	Confidence: 81.11632759520083
Rule 26:
	LHS: LemonLemonade, RaspberryLemonade, LemonCookie, GreenTea
	RHS: RaspberryCookie
	Support: 2.0733333333333333
	Confidence: 100.0
Rule 27:
	LHS: LemonLemonade, RaspberryLemonade, GreenTea, RaspberryCookie
	RHS: LemonCookie
	Support: 2.0733333333333333
	Confidence: 99.93573264781492
~~~