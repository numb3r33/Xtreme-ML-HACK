import numpy as np

from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def cross_validate_contacts(X, y, timestamps, model, features, plot=False, contact_types=None):
	
	errors = []
	
	for timestamp in timestamps:
		mask = X.date < timestamp
	
		Xtr = X.loc[mask, features]
		ytr = y.loc[mask]
		
		Xte = X.loc[~mask, features]
		yte = y.loc[~mask]
		
		model.fit(Xtr, ytr)

		mask_installation_report = Xte['contact_type_Installation Report - Input'] == 1
		mask_tweet_input         = Xte['contact_type_Tweet - Input'] == 1

		ypred = model.predict(Xte)

		# installation report input and tweet input are such rare events that we can replace them with zero.
		ypred[mask_installation_report.values] = 0.  
		ypred[mask_tweet_input.values] = 0.

		# anything that is less than zero turn it into zero.
		ypred[ypred < 0] = 0.

		if plot:
			if timestamp == '2016/01/01':
				for contact_type in contact_types:
					mask = Xte['contact_type_%s'%(contact_type)] == 1
					plt.scatter(yte[mask.values], ypred[mask.values], label='%s'%(contact_type))

				plt.legend(loc='best');
		
		fold_rmse = np.sqrt(mean_squared_error(yte, ypred))
		print('FOLD RMSE: ', fold_rmse)
		
		errors.append(fold_rmse)
		
	return errors


def cross_validate_resolutions(X, y, timestamps, model, features):
	
	errors = []
	
	for timestamp in timestamps:
		mask = X.date < timestamp
	
		Xtr = X.loc[mask, features]
		ytr = y.loc[mask]
		
		Xte = X.loc[~mask, features]
		yte = y.loc[~mask]
		
		model.fit(Xtr, ytr)

		ypred = model.predict(Xte)

		# anything that is less than zero turn it into zero.
		ypred[ypred < 0] = 0.
		
		fold_rmse = np.sqrt(mean_squared_error(yte, ypred))
		print('FOLD RMSE: ', fold_rmse)
		
		errors.append(fold_rmse)
		
	return errors