import pickle
"""n2 = pickle.load(open("/data/06333/aroraish/textnm1.pkl", "r"))
asd = n2.most_common(1000)
with open("/data/06333/aroraish/nm1.txt", "w") as f2:
	index = 1
	for a in asd:
	    f2.write(str(index) + ") " + a[0].encode('utf-8') + "  " + str(a[1]) + "\n")
	    index += 1
"""
n2 = pickle.load(open("/data/06333/aroraish/textnm2.pkl", "r"))
asd = n2.most_common(1000)
with open("/data/06333/aroraish/nm2.txt", "w") as f2:
	index = 1
	for a in asd:
	    f2.write(str(index) + ") " + a[0].encode('utf-8') + "  " + str(a[1]) + "\n")
	    index += 1

"""n2 = pickle.load(open("/data/06333/aroraish/textnm3.pkl", "r"))
asd = n2.most_common(1000)
with open("/data/06333/aroraish/nm3.txt", "w") as f2:
	index = 1
	for a in asd:
	    f2.write(str(index) + ") " + a[0].encode('utf-8') + "  " + str(a[1]) + "\n")
	    index += 1
"""
