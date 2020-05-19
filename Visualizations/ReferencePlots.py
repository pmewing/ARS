import csv
import pandas as pd
import numpy as np
import plotly
from DataFrame import DataFrame
from StatisticalTest import StatisticalTest


class PlotGeneration:
	# These are the rows found in map_data.csv
	# storing them here makes it easier for both create_csv() and create_map() to access them
	fips = 'fips'
	state_abbr = 'state_abbr'
	state_name = 'state_name'
	female_incidence = 'female_incidence'
	female_mortality = 'female_mortality'
	male_incidence = 'male_incidence'
	male_mortality = 'male_mortality'
	total_incidence = 'total_incidence'
	total_mortality = 'total_mortality'
	state_population = 'state_population'
	map_data = pd.read_csv(r"statistics/map_data.csv",
	                       dtype={fips: str,
	                              state_abbr: str,
	                              state_name: str,
	                              female_incidence: int,
	                              female_mortality: int,
	                              male_incidence: int,
	                              male_mortality: int,
	                              total_incidence: int,
	                              total_mortality: int
	                              })

	# FemaleMortalityCount and MaleMortalityCount functions will be needed in the DataFrame class
	@staticmethod
	def create_csv():
		"""
		data from https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv
		This function will create the map_data.csv file for reading later.
		"""
		data = r"statistics/state_fips_master.csv"
		state_info = pd.read_csv(data, sep=',', header=0, dtype={'state_name': str,
		                                                         'state_abbr': str,
		                                                         'long_name': str,
		                                                         'fips': str,
		                                                         'sumlev': str,
		                                                         'region': str,
		                                                         'division': str,
		                                                         'state': str,
		                                                         'region_name': str,
		                                                         'division_name': str,
		                                                         'state_population': str
		                                                         })

		# this csv file will act as the database for information on creating the map
		with open(r"statistics/map_data.csv", 'w', newline="") as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',')

			# column headers
			filewriter.writerow([PlotGeneration.fips,
			                     PlotGeneration.state_abbr,
			                     PlotGeneration.state_name,
			                     PlotGeneration.state_population,
			                     PlotGeneration.female_incidence,
			                     PlotGeneration.female_mortality,
			                     PlotGeneration.male_incidence,
			                     PlotGeneration.male_mortality,
			                     PlotGeneration.total_incidence,
			                     PlotGeneration.total_mortality
			                     ])

			# write lines from the state_info github content into the `database` csv file (previous `with open` statement)
			for index in range(len(state_info)):
				row = [state_info['fips'][index],
				       state_info['state_abbr'][index],
				       state_info['state_name'][index],
				       state_info['state_population'][index],
				       DataFrame.female_incidence[index].COUNT,
				       DataFrame.female_mortality[index].COUNT,
				       DataFrame.male_incidence[index].COUNT,
				       DataFrame.male_mortality[index].COUNT,
				       int(DataFrame.female_incidence[index].COUNT) + int(DataFrame.male_incidence[index].COUNT),
				       int(DataFrame.female_mortality[index].COUNT) + int(DataFrame.male_mortality[index].COUNT)
				       ]
				filewriter.writerow(row)

	@staticmethod
	def generate_choropleth():
		"""
		This function will create a choropleth map for each data available (male/female incidence/mortality)
		A total of six maps are created; they are outlined below

		Total incidence map: A choropleth map containing data about the incidences of cancer found within each state
		Total mortality map: A choropleth map containing data about death as a result of cancer found within each state
		Female incidence map: A choropleth map containing data about the incidences of cancer found within each state, for female only
		Female incidence map: A choropleth map containing data about the death as a result of cancer found within each state, for female only
		Male incidence map: A choropleth map containing data about the incidences of cancer found within each state, for male only
		Male incidence map: A choropleth map containing data about the death as a result of cancer found within each state, for male only
		"""

		# read data from the map_data CSV file
		#  key       [0]        [1]        [2]
		# {map type: [map_name, bar_title, COLOR_SCALE]}
		map_labels = {'total_incidence': ['Graph 1) Total Incidence Rate', 'Incidence Rate (people)'],
		              'total_mortality': ['Graph 2) Total Mortality Rate', 'Mortality Rate (people)'],
		              'female_incidence': ['Graph 3) Female Incidence Rate', 'Incidence Rate (people)'],
		              'female_mortality': ['Graph 4) Female Mortality Rate', 'Mortality Rat (people)e'],
		              'male_incidence': ['Graph 5) Male Incidence Rate', 'Incidence Rate (people)'],
		              'male_mortality': ['Graph 6) Male Mortality Rate', 'Mortality Rate (people)']
		              }

		# generate all map types: total/female/male incidence and mortality
		for key in map_labels:
			data = dict(type='choropleth',
			            locations=PlotGeneration.map_data['state_abbr'],
			            locationmode='USA-states',
			            text=PlotGeneration.map_data['state_name'],
			            zmin=0,
			            zmax=850000,  # 850,000
			            z=PlotGeneration.map_data[key],
			            colorscale='agsunset',
			            reversescale=True,
			            colorbar_title=map_labels[key][1])
			layout = dict(title=map_labels[key][0],
			              dragmode=False,
			              geo_scope='usa')

			# save maps
			file_name = r"HTML Files/project_files/%s.html" % key
			choropleth = dict(data=data, layout=layout)
			link = plotly.offline.plot(choropleth,
			                           filename=file_name,
			                           auto_open=False,
			                           show_link=True,
			                           link_text="View on Plotly")

	"""
	This function will visualize two pie charts. The first will show incidence rate, death rate, and survial rate. Once
	an individual has died from cancer, they are added to the death rate in addition to the incidence rate. This
	may not be correct. In addition, if an individual recovered from cancer, I assume that they are not taken out
	of the incidence rate.

	survival = incidence - death.
	"""

	@staticmethod
	def generate_sankey():
		labels = ["Total Incidence and Mortality",
		          "Female",
		          "Male",
		          "Incidence",  # Female
		          "Mortality",  # Female
		          "Incidence",  # Male
		          "Mortality"]  # Male

		colors = ["#999999",  # Total incidence and mortality
		          "#ff33cc",  # Female
		          "#0066ff",  # Male
		          "#009933",  # Female incidence
		          "#ff0000",  # Female mortality
		          "#009933",  # Male incidence
		          "#ff0000"]  # Male mortality
		sources = [0, 0, 1, 1, 2, 2]
		targets = [1, 2, 3, 4, 5, 6]
		values = PlotGeneration.return_sankey_values()

		data = dict(type='sankey',
		            node=dict(pad=15,
		                      thickness=20,
		                      line=dict(color="black", width=0.5),  # border thickness
		                      label=labels,
		                      color=colors),
		            link=dict(
			            # these are index values from the `label` section under `node`
			            source=sources,
			            target=targets,
			            value=values
		            ))
		layout = dict(title="Mortality and Incidence Visualization")

		file_name = r"HTML Files/project_files/sankey_plot.html"
		sankey = dict(data=data, layout=layout)
		link = [plotly.offline.plot(sankey,
		                            filename=file_name,
		                            auto_open=False,
		                            show_link=True)]

	@staticmethod
	def return_sankey_values():
		female_incidence = np.sum(PlotGeneration.map_data['female_incidence'])
		female_mortality = np.sum(PlotGeneration.map_data['female_mortality'])

		male_incidence = np.sum(PlotGeneration.map_data['male_incidence'])
		male_mortality = np.sum(PlotGeneration.map_data['male_mortality'])

		total_female = female_incidence + female_mortality
		total_male = male_incidence + male_mortality

		values = [
			total_female,
			total_male,
			female_incidence,
			female_mortality,
			male_incidence,
			male_mortality
		]
		return values

	@staticmethod
	def generate_boxplot():

		# returns a list of standardized data
		# returns a pd.DataFrame that has one dimension
		mortality_values = StatisticalTest.standardize_data(PlotGeneration.map_data['total_mortality'])
		incidence_values = StatisticalTest.standardize_data(PlotGeneration.map_data['total_incidence'])
		state_names = PlotGeneration.map_data['state_name']

		"""
		documentation: https://community.plotly.com/t/change-label-on-hover-in-ternary-plots/4667
		create a dictionary wrapped in a list of equal length to incidence-values
		The dictionary should have the state name as the key and its incidence_value as the value
		Format - South Dakota: 0.123
		
		{0:s} = format the first value as a string
		{1:.2f} = format the second value as a float with 2 decimal points
		"""
		outlier_text = ['{0:s}: {1:.2f} standard deviations away'.format(state_names[i], incidence_values[i]) for i in range(len(state_names))]

		incidence = plotly.graph_objs.Box(
			y=incidence_values,
			name="Incidence Rate",
			boxpoints='suspectedoutliers',
			text=outlier_text,
			hoverinfo='text',
			xaxis=dict(title="Standard Deviations"),
			marker=dict(
				color='rgb(8,81,156)',
				outliercolor='rgba(219, 64, 82, 0.6)',
				line=dict(
					outliercolor='rgba(219, 64, 82, 0.6)',
					outlierwidth=2)
			)
		)

		mortality = plotly.graph_objs.Box(
			y=mortality_values,
			name="Mortality Rate",
			boxpoints='suspectedoutliers',
			text=outlier_text,
			hoverinfo='text',
			marker=dict(
				color='rgb(43, 184, 0)',
				outliercolor='rgba(43, 184, 0, 0.6)',
				line=dict(
					outliercolor='rgba(43, 184, 0, 0.6)',
					outlierwidth=2)
			)
		)

		data = [incidence, mortality]

		layout = plotly.graph_objs.Layout(title="Standardized Box Plots")
		file_name = r"HTML Files/project_files/boxplot.html"
		fig = plotly.graph_objs.Figure(data=data, layout=layout)
		boxplot = plotly.offline.plot(fig,
		                              filename=file_name,
		                              auto_open=False,
		                              show_link=True)
