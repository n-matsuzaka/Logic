# Propositional Symbols:
# a,b,...

# Truth Function Symbols:
# C     Contradiction
# (Na)  Not a
# (aAb) a And b 
# (aOb) a Or b
# (aTb) if a Then b
# (aEb) a is Equivalent to b

def build_structures(structures, structure, remaining_psymbols):
	if remaining_psymbols == 0:
		if len(structure) > 0:
			structures.append(structure)
		return
	st_copied = structure.copy()
	structure.append(True)
	st_copied.append(False)	
	build_structures(structures, structure, remaining_psymbols - 1)
	build_structures(structures, st_copied, remaining_psymbols - 1)
	return

#return disjunctive or conjunctive normal form equivalent to the formula
def conv_to_normal_form(formula, tf_symbol):
	n_form = ""
	if not tf_symbol in ["O", "A"]:
		print("Error: conv_to_normal_form tf_symbol")
	if tf_symbol == "O":
		models = get_models(formula)
	else:
		models = get_models("(N" + formula + ")")
	for model in models:
		if tf_symbol == "O": #DNF 
			b_junction = get_basic_junction(model, "A")
		else: #CNF
			for i in range(0, len(model)):
				model[i] = not model[i] 
			b_junction = get_basic_junction(model, "O")
		if n_form == "":
			n_form = b_junction
		else:
			n_form = "("+n_form+tf_symbol+b_junction+")"
	return n_form

#Counts the number of propositional symbols.
#They must be a,b,...
def count_pro_symbols(formula):
	pro_symbols, ord_a, ord_z = "", ord("a"), ord("z")
	for char in formula:
		if (ord_a <= ord(char) <= ord_z) and not char in pro_symbols:
			pro_symbols = pro_symbols + char
	return len(pro_symbols)

def decompose_formula(formula):
	tf_symbol = ""
	subformulas = []
	if is_atomic(formula):
		subformulas.append(formula)
	for i in range(0, len(formula)):
		if is_tf_symbol(formula[i]) and get_depth(formula[0:i]) == 1:
			tf_symbol = formula[i]
			if tf_symbol != "N":
				subformulas.append(formula[1:i])
			subformulas.append(formula[i+1:len(formula)-1])			
	return tf_symbol, subformulas

def get_basic_junction(model, tf_symbol):
	b_junction = ""
	for i in range(0, len(model)):
		p_symbol = chr(ord("a") + i)  
		literal = p_symbol if model[i] else "(N"+p_symbol+")"
		if i == 0:
			b_junction = literal
		else:
			b_junction = "("+b_junction+tf_symbol+literal+")"
	return b_junction

def get_depth(ini_segment):
	return ini_segment.count("(") - ini_segment.count(")")

def get_models(formula):
	models = []
	structures = []
	build_structures(structures, [], count_pro_symbols(formula))
	for structure in structures:
		if is_model_of(structure, formula):
			models.append(structure)
	return models

def get_value(tf_symbol, values):
	if tf_symbol == "N":
		return not values[0]
	elif tf_symbol == "A":
		return values[0] and values[1]
	elif tf_symbol == "O":
		return values[0] or values[1]		 
	elif tf_symbol == "T":
		return ((not values[0]) or values[1])
	elif tf_symbol == "E":
		return (values[0] and values[1]) or (not values[0] and not values[1])		 

#Only characters from "a" to "z" are atomic formulas.
def is_atomic(formula):
	if len(formula) != 1:
		return False
	return formula.islower()

def is_model_of(structure, formula):
	if formula[0] != "(": #formula is atomic
		return structure[ord(formula)-ord("a")]
	tf_symbol, subformulas = decompose_formula(formula)
	values = []
	for subformula in subformulas:
		values.append(is_model_of(structure, subformula))
	return get_value(tf_symbol, values)

def is_tf_symbol(symbol):
	return symbol in ["C","N","A","O","T","E"]

def test():
	structures = []
	build_structures(structures, [], 0)
	print(structures == [])
	structures = []
	build_structures(structures, [], 2)
	print(structures == [[True, True], [True, False], [False, True], [False, False]])	

	print(count_pro_symbols("a") == 1)
	print(count_pro_symbols("(Na)") == 1)
	print(count_pro_symbols("(aAb)") == 2)

	print(conv_to_normal_form("(Na)", "O") == "(Na)")
	print(conv_to_normal_form("(aTb)", "O") == "(((aAb)O((Na)Ab))O((Na)A(Nb)))")
	print(conv_to_normal_form("(aTb)", "A") == "((Na)Ob)")

	print(decompose_formula("a") == ("", ["a"]))
	print(decompose_formula("(Na)") == ("N", ["a"]))
	print(decompose_formula("(aAb)") == ("A", ["a", "b"]))
	print(decompose_formula("(N(aAb))") == ("N", ["(aAb)"]))
	print(decompose_formula("((aAb)O(cAd))") == ("O", ["(aAb)", "(cAd)"]))

	print(get_basic_junction([True], "A") == "a")
	print(get_basic_junction([False], "A") == "(Na)")
	print(get_basic_junction([True,False], "A") == "(aA(Nb))")
	print(get_basic_junction([False,False], "O") == "((Na)O(Nb))")

	print(get_depth("a") == 0)
	print(get_depth("(N") == 1)	
	print(get_depth("(N(aAb))") == 0)	

	print(get_models("(aEb)") == [[True,True], [False,False]])
	print(get_models("(aTb)") == [[True,True],[False,True],[False,False]])
	print(get_models("(N(aTb))") == [[True,False]])
	print(get_models("(N(bTa))") == [[False,True]])
	print(get_models("(bE(aAc))") == [[True, True, True], [True, False, False], [False, False, True], [False, False, False]])

	print(get_value("N", [True]) == False)
	print(get_value("A", [True, True]) == True)
	print(get_value("T", [True, False]) == False)
	print(get_value("T", [False, True]) == True)
	print(get_value("E", [False, True]) == False)
	print(get_value("E", [False, False]) == True)

	print(is_atomic("a") == True)
	print(is_atomic("(Na)") == False)	

	print(is_model_of([True, False], "(aAb)") == False)

	print(is_tf_symbol("A") == True)
	print(is_tf_symbol("a") == False)	

test()