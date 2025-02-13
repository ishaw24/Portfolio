from shiny.express import input, render, ui
from shinywidgets import render_widget
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('C:/Users/theis/Documents/GitHub/Personal-Projects/Percentile Plot/base_data_23-24.csv') 

id_colname = 'PLAYER_NAME' # define identifier column which dropdown menu selects
id_col = data[id_colname] 

data_pct = data.rank(axis=0, numeric_only=True, pct=True)
data_pct = data_pct.join(id_col, how='inner')

choices = pd.unique(id_col).tolist()

with ui.sidebar():
    ui.input_selectize("var", "Select player", choices=choices)



@render.plot
def percentileplot():
    global data_pct, id_colname
    name = input.var()
    data_pct_f = data_pct[data_pct[id_colname] == name]
    data_f = data[data[id_colname] == name].drop(id_colname, axis=1).values.flatten().tolist()
    ax = sns.barplot(data_pct_f)
    ax.set_ylim((0,1))
    ax.set_ylabel('Percentile')
    [ax.bar_label(con, fontsize=6, labels=[label,]) for con, label in zip(ax.containers,data_f)]


