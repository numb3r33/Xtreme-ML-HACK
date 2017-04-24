import numpy as np
import pandas as pd

from itertools import product

def get_contacts_df(contacts):
	contacts_grouped = contacts.groupby(['CONTACT.TYPE', 'START.DATE'])['Contacts'].sum().unstack().fillna(0)

	dates        = np.tile(contacts_grouped.columns.values, contacts['CONTACT.TYPE'].nunique())

	contact_types = []
	for i in range(len(contacts_grouped.index)):
		contact_type = [contacts_grouped.index[i]]
		contact_types.append(np.repeat(contact_type, contacts_grouped.shape[1]))

	contact_types = np.array(contact_types)
	contact_types = contact_types.flatten()

	contacts_df = pd.DataFrame(contacts_grouped.values.reshape(contacts_grouped.shape[1]*contacts['CONTACT.TYPE'].nunique(), 1))
	contacts_df = contacts_df.assign(dates=dates)
	contacts_df = contacts_df.assign(contact_types=contact_types)
	contacts_df = contacts_df.rename(columns={0: 'num_contacts'})

	return contacts_df


def get_resolutions_df(resolution):
	resolution_grouped = resolution.groupby(['Category', 'Subject', 'Date'])['Resolution'].sum()\
										.unstack()\
										.unstack()\
										.fillna(0)
			
			
	dates_res = np.tile(resolution_grouped.columns.levels[0].values, \
						resolution.Category.nunique() * resolution.Subject.nunique())

	category_subject_pairs = list(product(resolution.Category.unique(), resolution.Subject.unique()))

	cs_pairs = []
	for i in range(len(category_subject_pairs)):
		cs_pair_repeated = []
		for j in range(len(resolution_grouped.columns.levels[0].values)):
			cs_pair_repeated.append((category_subject_pairs[i]))

		cs_pairs.append(cs_pair_repeated)
		
	cs_pairs = np.array(cs_pairs)


	categories = []
	subjects   = []

	for i in range(cs_pairs.shape[0]):
		for j in range(cs_pairs.shape[1]):
			categories.append(cs_pairs[i][j][0])
			subjects.append(cs_pairs[i][j][1])
			
	resolution_grouped = resolution_grouped.stack()

	df_res = pd.DataFrame(resolution_grouped.values.reshape(cs_pairs.shape[0] * cs_pairs.shape[1], 1))
	df_res = df_res.assign(dates=dates_res)
	df_res = df_res.assign(categories=categories)
	df_res = df_res.assign(subjects=subjects)

	df_res = df_res.rename(columns={0: 'num_resolutions'})

	return df_res


# month to number mapping

month_dict = {
    'jan.': 1,
    'feb.': 2,
    'mar.': 3,
    'apr.': 4,
    'may.': 5,
    'jun.': 6,
    'jul.': 7,
    'ago.': 8,
    'sep.': 9,
    'oct.': 10,
    'nov.': 11,
    'dec.': 12
}

def create_contract_start_date(row):
    year = row['YEAR_CONTRACT']
    month = month_dict[row['MONTH_CONTRACT']]
    day  = row['DAY_ALTA_CONTR']
    
    return pd.to_datetime('%s/%s/%s'%(year, month, day))

def create_contract_end_date(row):
    year = row['YEAR_END_CONTRACT']
    month = month_dict[row['MONTH_END_CONTRACT']]
    day  = row['DAY_END_CONTRACT']
    
    return pd.to_datetime('%s/%s/%s'%(year, month, day))


def modify_contracts(contracts_new, contracts_end):
	contract_start_date = contracts_new.apply(create_contract_start_date, axis=1)
	contract_end_date   = contracts_end.apply(create_contract_end_date, axis=1)

	contracts_new   = contracts_new.assign(date=contract_start_date)
	contracts_end   = contracts_end.assign(date=contract_end_date)

	contracts_new   = contracts_new.assign(day_of_year=contracts_new.date.dt.dayofyear)
	contracts_end   = contracts_end.assign(day_of_year=contracts_end.date.dt.dayofyear)


	return contracts_new, contracts_end