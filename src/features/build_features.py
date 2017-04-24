import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class Dataset(object):

	def __init__(self, dataset):
		self.dataset = dataset

	def add_week(self):
		self.dataset = self.dataset.assign(week=self.dataset.date.dt.week)
		return self

	def add_month(self):
		self.dataset = self.dataset.assign(month=self.dataset.date.dt.month)
		return self

	def add_year(self):
		self.dataset = self.dataset.assign(year=self.dataset.date.dt.year)
		return self

	def add_weekday(self):
		self.dataset = self.dataset.assign(weekday=self.dataset.date.dt.weekday)
		return self

	def add_dayofyear(self):
		self.dataset = self.dataset.assign(day_of_year=self.dataset.date.dt.dayofyear)
		return self

	def ohe_features(self, features):
		feature_ohes = []
		for feature in features:
			feature_ohes.append(pd.get_dummies(self.dataset[feature], drop_first=True, prefix=feature))
		
		feature_ohes.append(self.dataset)

		self.dataset = pd.concat(feature_ohes, axis=1)

		return self

	def add_isweekend(self):
		self.dataset = self.dataset.assign(is_weekend=((self.dataset.weekday  == 5) | (self.dataset.weekday == 6)).astype(np.int))

		return self

	def add_islastweek(self):
		self.dataset = self.dataset.assign(is_lastweek=(self.dataset.week == 53).astype(np.int))
		return self

	def add_isspecialday(self):
		mask = (self.dataset.day_of_year == 1) | (self.dataset.day_of_year == 6) |\
		       (self.dataset.day_of_year == 2) | (self.dataset.day_of_year == 59)
		self.dataset = self.dataset.assign(isspecialday=mask.astype(np.int))

		return self

	
	def add_mean_num_contacts_by_week(self):
		mean_contacts = self.dataset.groupby(['weekday'])['num_contacts'].mean()
		self.dataset['mean_contact_week'] = self.dataset.weekday.map(mean_contacts)

		return self

	def add_median_num_contacts_by_type(self):
		median_contacts = self.dataset.groupby(['contact_type'])['num_contacts'].sum()
		self.dataset['median_contact_type'] = self.dataset.contact_type.map(median_contacts)

		return self
 
	def add_mean_num_contacts_by_type_month(self):
		mean_contacts = self.dataset.groupby(['contact_type', 'month'])['num_contacts'].median()
		self.dataset['mean_contact_type'] = self.dataset[['contact_type', 'month']].apply(lambda x: mean_contacts[x[0], x[1]], axis=1)

		return self

	def add_max_num_contacts_by_type_month(self):
		max_contacts = self.dataset.groupby(['contact_type', 'day_of_year'])['num_contacts'].max()
		self.dataset['max_contact_type'] = self.dataset[['contact_type', 'day_of_year']].apply(lambda x: max_contacts[x[0], x[1]], axis=1)

		return self

	def add_min_num_contacts_by_type_month(self):
		min_contacts = self.dataset.groupby(['contact_type', 'month'])['num_contacts'].min()
		self.dataset['min_contact_type'] = self.dataset[['contact_type', 'month']].apply(lambda x: min_contacts[x[0], x[1]], axis=1)

		return self

	def add_range_contacts_by_type_month(self):
		max_contacts = self.dataset.groupby(['contact_type', 'month'])['num_contacts'].max()
		min_contacts = self.dataset.groupby(['contact_type', 'month'])['num_contacts'].min()

		range_contacts = max_contacts - min_contacts
		self.dataset['range_contact_type'] = self.dataset[['contact_type', 'month']].apply(lambda x: range_contacts[x[0], x[1]], axis=1)

		return self


	def add_active_contracts(self, active_contracts):
		active_contract_by_day = self.dataset.day_of_year.map(active_contracts)
		self.dataset = self.dataset.assign(active_contract=active_contract_by_day)

		return self

	def add_change_in_trend_indicator(self):
		mask = (self.dataset.date.dt.year > 2014) & ((self.dataset.contact_type == 'Web - Input') | (self.dataset.contact_type == 'Tweet - Input'))
		self.dataset = self.dataset.assign(change_in_trend=mask.astype(np.int))
		return self

	def label_encode_features(self, features):
		for feature in features:
			lbl = LabelEncoder()
			lbl.fit(self.dataset[feature])

			self.dataset['encoded_%s'%(feature)] = lbl.transform(self.dataset[feature])


		return self