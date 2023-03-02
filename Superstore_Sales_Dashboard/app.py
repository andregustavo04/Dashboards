import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd 
import numpy as np 

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server


# ====================== READ AND CLEAN DATA ====================== #

df = pd.read_csv('superstore_sales_data.csv')

# DataFrame que será utilizado para gerar os gráficos
df_copy = df.copy()



options = ['Todos os Anos'] 
options = options + list(df_copy['Ano'].value_counts().index.values)
regions = df_copy['Region'].value_counts().index.values


# ====================== STYLES ====================== #

template_theme1 = 'quartz'
template_theme2 = 'darkly'

url_theme1 = dbc.themes.QUARTZ
url_theme2 = dbc.themes.DARKLY


config = {"hovermode": "x unified", 
		"legend": {"yanchor":"top", 
					"y":0.9, 
					"xanchor":"left", "x":0.1, 
					"title": {"text": None}, 
					"font" :{"color":"white"}, 
					"bgcolor": "rgba(0,0,0,0.5)"}, 
		"margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph = {"displayModeBar": False, "showTips": False}

card_style = {'margin':'5px'}


# ====================== LAYOUT ====================== #

app.layout = html.Div(children=[
				dbc.Row([
					dbc.Col([
						dbc.Card([
							dbc.Row([
									html.H4('Dashboard de Vendas Regionais', style={'text-align':'center', 'margin-top':'10px'}),
									dbc.Col([
										ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
									], style={'margin-left':'20px', 'margin':'10px', 'display':'flex', 'align-items':'center'})
								], justify="center"),

							dbc.Card([
								dbc.CardBody([
									html.H6("Ano"),
									dcc.RadioItems(options=options, value='Todos os Anos', id='year_dropdown'),
									])
								], style={'margin':'10px', 'background-color': 'rgba(0, 0, 0, 0.3)'}),
							dbc.Card([
								dbc.CardBody([
									html.H6("Regiões"),
									dcc.Dropdown(regions, regions[0], id='regions_dropdown', clearable=False, searchable=False, style={'color':'purple'}),
									])
								], style={'margin':'10px', 'background-color': 'rgba(0, 0, 0, 0.3)'}),

							dbc.Row([
								dbc.Col([
									dbc.Button('Visite o Site', color='primary', className='me-1', href="https://www.linkedin.com/in/andr%C3%A9-gustavo-lopes-984bb119a/", target="_blank")
									])
								], style={'margin':'15px'})
							], style={'height':'110vh', 'alignment':'center', 'margin-top':'10px'})

						], sm=2),

					dbc.Col([
						dbc.Row([
							dbc.Col([
								dbc.Card([
									html.Div(id='fat_indicator'),
									], style={'margin-top':'10px'})
								], sm=12, md=4, lg=4),
							dbc.Col([
								dbc.Card([
									html.Div(id='sales_indicator', style={'text-align':'center'}),
									], style={'margin-top':'10px'})
								], sm=12, md=4, lg=4),
							dbc.Col([
								dbc.Card([
									html.Div(id='ticket_indicator', style={'text-align':'center'}),
									], style={'margin-top':'10px', 'margin-right':'10px'})
								], sm=12, md=4, lg=4),
							]),

						dbc.Row([
							dbc.Col([
								dbc.Row([
									dbc.Col([
										dbc.Card([
											html.H6('Faturamento por Segmento de Cliente', style={'margin':'5px', 'text-align':'center'}),
											dcc.Graph(id='client_seg', style={'margin':'10px'}),
											], style={'margin-top':'10px'}),
										], sm=12, md=5, lg=5),

									dbc.Col([
										dbc.Card([
											html.Div(id='title_vendas_mes', style={'margin-top':'10px'}),
											dcc.Graph(id='vendas_ano_mes', style={'margin':'10px'}),
											], style={'margin-top':'10px'}),
										], sm=12, md=7, lg=7),

									]),
								dbc.Row([
									dbc.Col([
										dbc.Card([
											html.H6('Faturamento por Categoria de Produto', style={'margin':'5px', 'text-align':'center'}),
											dcc.Graph(id='product_cat', style={'margin':'10px'}),
											], style={'margin-top':'10px', 'margin-bottom':'10px'})
										], sm=12, md=5, lg=5),
									dbc.Col([
										dbc.Card([
											html.H6('Vendas por Dia da Semana', style={'text-align':'center', 'margin-top':'10px'}),
											dcc.Graph(id='vendas_dia_semana', style={'margin':'10px'})
										], style={'margin-top':'10px'})
									], sm=12, md=7, lg=7)
								])
							], sm=12, md=7, lg=7),
							
							dbc.Col([
								dbc.Row([
									dbc.Col([
										dbc.Card([
											html.H6('Vendas por Estado', style={'text-align':'center', 'margin-top':'10px'}),
											dcc.Graph(id='fig_estados', style={'margin':'10px'}),
											], style={'margin-top':'10px', 'margin-right':'10px'}),
										])
									]),
								], sm=12, md=5, lg=5),
							])
						], sm=10)

					])

	])



# ================= CALLBACKS ================= #
@app.callback(
	[
	Output('client_seg', 'figure'),
	Output('product_cat', 'figure'),
	Output('vendas_dia_semana', 'figure'),
	Output('fig_estados', 'figure'),
	Output('fat_indicator', 'children'),
	Output('sales_indicator', 'children'),
	Output('ticket_indicator', 'children'),
	Output('vendas_ano_mes', 'figure'),
	Output('title_vendas_mes', 'children')
	],

	[
	Input('year_dropdown', 'value'),
	Input('regions_dropdown', 'value'),
	Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
	]
	)
def graphs(year, region, theme):
	template = template_theme1 if theme else template_theme2

	title_vendas_mes = html.H6('Vendas por Ano', style={'text-align':'center'})
	if year != 'Todos os Anos':
		df_return = df_copy[(df_copy['Ano'] == year) & (df_copy['Region'] == region)]
		title_vendas_mes = html.H6('Vendas por Mês', style={'text-align':'center'})
	else:
		df_return = df_copy[df_copy['Region'] == region]

	# Faturamento por Segmento de Cliente
	df_seg = df_return.groupby('Segment').sum().reset_index()[['Segment', 'Sales']]
	fig1 = go.Figure(go.Pie(labels=df_seg['Segment'], values=df_seg['Sales'], hole=.6))
	fig1.update_layout(config, height=200, template=template)
	fig1.update_traces(hoverinfo="label+percent+value", textinfo='label+percent')
	fig1.update(layout_showlegend=False)

	# Faturamento por Categoria de Produto
	df_cat = df_return.groupby('Category').sum().reset_index()[['Category', 'Sales']]
	fig2 = go.Figure(go.Pie(labels=df_cat['Category'].unique(), values=df_cat['Sales'], hole=.6))
	fig2.update_layout(config, height=200, template=template)
	fig2.update_traces(hoverinfo="label+percent+value", textinfo='label+percent')
	fig2.update(layout_showlegend=False)


	# Vendas Dia de Semana
	semana = {0: 'Segunda-Feira', 1:'Terça-Feira', 2:'Quarta-Feira', 3:'Quinta-Feira', 4:'Sexta-Feira', 5:'Sábado', 6:'Domingo'}
	df_week = df_return[['Day of Week', 'Sales']]
	df_week = df_week.groupby('Day of Week').sum().reset_index().sort_values(by='Day of Week', ascending=True)
	df_week['Day of Week'] = df_week['Day of Week'].map(semana)
	fig4 = go.Figure(go.Bar(x=df_week['Day of Week'], y=df_week['Sales']))
	fig4.update_layout(config, template=template, height=200, width=350)


	# Vendas por Estado
	df_state = df_return[['Ano', 'State', 'Sales']]
	df_state = df_state.groupby('State').sum().reset_index()[['State', 'Sales']].sort_values(by='Sales', ascending=True)
	df_state = df_state.iloc[:10]
	fig_text = [f'{x} - R$ {y:.2f}' for x,y in zip(df_state['State'].unique(), df_state['Sales'].unique())]
	fig5 = go.Figure(go.Bar(x=df_state['Sales'], y=df_state['State'], orientation='h', text=fig_text, insidetextanchor='end', insidetextfont=dict(family='Times', size=12)))
	fig5.update_layout(config, template=template, height=500, width=350, yaxis={'showticklabels':False})



	# Indicador de Faturamento
	faturamento = df_return['Sales'].sum() 
	indicator_faturamento = html.Div([
		html.H6(f'Faturamento Total em {year}'),
		html.Legend(f'R$ {faturamento:.2f}'),
		], style={'text-align':'center', 'padding':'10px'})



	# Indicador do Número de Vendas
	numero_vendas = df_return['Order ID'].nunique()
	indicator_num_vendas = html.Div([
		html.H6(f'Número de Vendas em {year}'),
		html.Legend(f'{numero_vendas}'),
		], style={'text-align':'center', 'padding':'10px'})


	# Indicador do Ticket Médio
	ticket_medio = faturamento / numero_vendas
	indicator_tick_medio = html.Div([
		html.H6(f'Ticket Médio em {year}'),
		html.Legend(f'R$ {ticket_medio:.2f}'),
		], style={'text-align':'center', 'padding':'10px'})


	# Vendas por Ano ou Mês
	df_period = df_return[['Month','Ano', 'Sales']]
	
	if year != 'Todos os Anos':
		meses = {1: 'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}
		df_period = df_period.groupby('Month').sum().reset_index()
		df_period['Month'] = df_period['Month'].map(meses) 
		fig6 = go.Figure(go.Bar(x=df_period['Month'], y=df_period['Sales']))
		fig6.update_layout(config, template=template, height=230, width=350)
	else:
		df_period = df_period.groupby('Ano').sum().reset_index()
		fig6 = go.Figure(go.Bar(x=df_period['Ano'], y=df_period['Sales']))
		fig6.update_layout(config, template=template, height=220, width=350)

	return fig1, fig2, fig4, fig5, indicator_faturamento, indicator_num_vendas, indicator_tick_medio, fig6, title_vendas_mes



# ================= RUN SERVER ================= #

if __name__ == "__main__":
	app.run_server(debug=False) 