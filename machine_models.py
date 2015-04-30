
import numpy
import pprint
import pickle
from sklearn import linear_model


variable_y  = []
variables_x = []

model_params = {
	'CD': 0.85,
	'AB': 0.95,
	'EFG': 0.80
	}

# with open('ok_classes.txt') as f:

#     variables = f.readline().strip().split('\t')
#     for line in f:
#         line = line.strip().split('\t')
#         line[0] = line[0].replace('"', '')
#         #print(line)
#         line = [float(v) for v in line ]
#         variables_x.append(line[1:])
#         variable_y.append(line[0])

def numpyfy(x, y):

    x = numpy.reshape(x, (len(x), len(x[0])))
    y = numpy.reshape(y, (len(y), 1))
    return x,y

def run_regression(x, y):

    reg = linear_model.LogisticRegression()
    reg.fit(x, y)
    r_square = reg.score(x, y)
    coefs = reg.coef_
    coefs = [ '{0:.10f}'.format(float(x)) for x in numpy.nditer(coefs)]
    var = variables[1:]
    coefs = zip(var, coefs)
    print('coefficient of variables are: ')
    for var, coef in coefs:
        print(var + '\t' + coef + '\t')
    print('intercept is ' + str(reg.intercept_))
    print('R square is ' + str(r_square))
    
    probs = reg.predict_proba(variables_x)
    class_probs = []
    for n,p in probs:
    	if p>= 0.80:
    		class_probs.append(1)
    	else:
    		class_probs.append(0)
    p = zip(class_probs, variable_y)
    errors = 0 
    for p, r in p:
    	if p == 1 and r == 0:
    		errors +=1
    print(errors)
    print(sum(class_probs))
    print(float(errors)/sum(class_probs))
    return reg
    
    #print(reg.predict(test))
    #print(reg.predict_proba(test))
    #print(len(class_probs))
    


#test= [2500.0, 0.0, 0.1527, 59.83, 0.0, 1.0, 30000.0, 0.0, 0.0, 0.0, 0.0, 1.0, 15.90410959, 742.0, 5.0, 3.0, 0.0, 0.094, 4.0]
#ok_classes_model = run_regression(*numpyfy(variables_x, variable_y))
#pickle.dump(ok_classes_model, open('ok_classes_model.p', 'wb'))
#good_classes_model = pickle.load(open('great_classes_model.p', 'r'))
#print(good_classes_model.predict_proba(test))
	


