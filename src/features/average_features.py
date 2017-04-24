import pandas as pd
import numpy as np


def prepare_average_features(contacts_df, contacts_df_sub, contacts_test):

	def get_quarter_mean(row):
		prev_start_date = row['date'] + pd.DateOffset(-90)
		
		# mask = (contacts_df.dates >= prev_quarter_start_date.values[0]) & (contacts_df.dates < row['date'].values[0]) \
		# 	   & (contacts_df.contact_types == row['contact_type'].values[0]) &\
		# 	   (contacts_df.dates.dt.weekday == row['date'].dt.weekday.values[0])

		mask = (contacts_df.dates <= prev_start_date.values[0]) &\
			   (contacts_df.contact_types == row['contact_type'].values[0]) &\
			   (contacts_df.dates.dt.weekday == row['date'].dt.weekday.values[0])
		
		return contacts_df.loc[mask, 'num_contacts'].mean()

	def get_last_7_days_mean(row):
		prev_start_date = row['date'] + pd.DateOffset(-15)
		
		mask = (contacts_df.dates >= prev_start_date.values[0]) & (contacts_df.dates < row['date'].values[0]) \
			   & (contacts_df.contact_types == row['contact_type'].values[0]) &\
			   (contacts_df.dates.dt.weekday == row['date'].dt.weekday.values[0])
			
		return contacts_df.loc[mask, 'num_contacts'].mean()

	def get_last_30_days_mean(row):
		prev_start_date = row['date'] + pd.DateOffset(-30)
		
		mask = (contacts_df.dates >= prev_start_date.values[0]) & (contacts_df.dates < row['date'].values[0]) \
			   & (contacts_df.contact_types == row['contact_type'].values[0]) &\
			   (contacts_df.dates.dt.weekday == row['date'].dt.weekday.values[0])
			
		return contacts_df.loc[mask, 'num_contacts'].mean()

	def get_last_60_days_mean(row):
		prev_start_date = row['date'] + pd.DateOffset(-60)
		
		mask = (contacts_df.dates >= prev_start_date.values[0]) & (contacts_df.dates < row['date'].values[0]) \
			   & (contacts_df.contact_types == row['contact_type'].values[0]) &\
			   (contacts_df.dates.dt.weekday == row['date'].dt.weekday.values[0])
			
		return contacts_df.loc[mask, 'num_contacts'].mean()




	prev_quarter_mean   = contacts_df_sub.groupby(['date', 'contact_type']).apply(get_quarter_mean)
	# last_7_days_mean    = contacts_df_sub.groupby(['date', 'contact_type']).apply(get_last_7_days_mean)
	# last_30_days_mean   = contacts_df_sub.groupby(['date', 'contact_type']).apply(get_last_30_days_mean)
	# last_60_days_mean   = contacts_df_sub.groupby(['date', 'contact_type']).apply(get_last_60_days_mean)


	quarter_mean     = contacts_df_sub[['date', 'contact_type']].apply(lambda x: prev_quarter_mean[x[0], x[1]], axis=1)
	# _7_days_mean     = contacts_df_sub[['date', 'contact_type']].apply(lambda x: last_7_days_mean[x[0], x[1]], axis=1)
	# _30_days_mean    = contacts_df_sub[['date', 'contact_type']].apply(lambda x: last_30_days_mean[x[0], x[1]], axis=1)
	# _60_days_mean    = contacts_df_sub[['date', 'contact_type']].apply(lambda x: last_60_days_mean[x[0], x[1]], axis=1)


	contacts_df_sub = contacts_df_sub.assign(quarter_mean=quarter_mean.values)
	# contacts_df_sub = contacts_df_sub.assign(_7_days_mean=_7_days_mean.values)
	# contacts_df_sub = contacts_df_sub.assign(_30_days_mean=_30_days_mean.values)
	# contacts_df_sub = contacts_df_sub.assign(_60_days_mean=_60_days_mean.values)



	prev_quarter_mean_test   = contacts_test.groupby(['date', 'contact_type']).apply(get_quarter_mean)
	# last_7_days_mean_test    = contacts_test.groupby(['date', 'contact_type']).apply(get_last_7_days_mean)
	# last_30_days_mean_test   = contacts_test.groupby(['date', 'contact_type']).apply(get_last_30_days_mean)
	# last_60_days_mean_test   = contacts_test.groupby(['date', 'contact_type']).apply(get_last_60_days_mean)


	quarter_mean_test     = contacts_test[['date', 'contact_type']].apply(lambda x: prev_quarter_mean_test[x[0], x[1]], axis=1)
	# _7_days_mean_test     = contacts_test[['date', 'contact_type']].apply(lambda x: last_7_days_mean_test[x[0], x[1]], axis=1)
	# _30_days_mean_test    = contacts_test[['date', 'contact_type']].apply(lambda x: last_30_days_mean_test[x[0], x[1]], axis=1)
	# _60_days_mean_test    = contacts_test[['date', 'contact_type']].apply(lambda x: last_60_days_mean_test[x[0], x[1]], axis=1)


	contacts_test = contacts_test.assign(quarter_mean=quarter_mean_test.values)
	# contacts_test = contacts_test.assign(_7_days_mean=_7_days_mean_test.values)
	# contacts_test = contacts_test.assign(_30_days_mean=_30_days_mean_test.values)
	# contacts_test = contacts_test.assign(_60_days_mean=_60_days_mean_test.values)


	return contacts_df_sub, contacts_test



def get_active_contracts_by_day(contracts_new_df, contracts_end_df):
	total_started = contracts_new_df.groupby('day_of_year')['NUMBER_OF_CONTRACTS'].sum()
	total_ended   = contracts_end_df.groupby('day_of_year')['NUMBER_OF_CONTRACTS_ENDED'].sum()
	diff = total_started - total_ended

	return diff