# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:41:44 2024

@author: Xenia Skorodelov
"""
#%% преобразование файлов с помощью pandas
def import_xl_df (path): #выгрузка xlsx файла (только первого листа)
    import pandas as pd
    xl = pd.ExcelFile(path)

    df = pd.read_excel(path)
    return (df)

def transform_df (df, focus_group):
    import pandas as pd

    df = df.dropna(axis='index', how='any')
    for col in df:
        if "54_51" in col:
            df.drop(col, inplace=True, axis=1)
        if "61_64" in col:
              df.drop(col, inplace=True, axis=1)
    df['number'] = 0
    for i, row in df.iterrows():
        df.loc[i, 'number'] = str(row.Name[3:5])
    df['day'] = '0'
    for i, row in df.iterrows():
        if "day12" in row.Name:
            df.loc[i, 'day'] = '12'
        if "day15" in row.Name:
            df.loc[i, 'day'] = '15'
        if "day17" in row.Name:
            df.loc[i, 'day'] = '17'
        if "day22" in row.Name:
            df.loc[i, 'day'] = '22'
        if "day24" in row.Name:
            df.loc[i, 'day'] = '24'
    df['group'] = 'контроль'
    for i, row in df.iterrows():
        for j in focus_group:
            if j in row['Name']:
                df.loc[i, 'group'] = 'лечение'
            if 'area3' in row['Name']:
                df.loc[i, 'group'] = 'здоровая ткань'
    df.columns = [col.replace('_4', '') for col in df.columns]
    df = df[~df.Name.str.contains('Rat24')]
    df = df[~df.Name.str.contains('Rat25')]
    df = df[~df.Name.str.contains('Rat41')]
    return (df)
#%% построение графиков seaborn и matplotlib.pyplot
def sns_boxp_dinam_wdots (df_plot, option, title_): #боксплоты с точками
    import seaborn as sns
    import matplotlib.pyplot as plt
    base_colors = {'контроль': '#D3D3D3', 'лечение': '#D3D3D3', 'здоровая ткань': '#D3D3D3'}
    water_colors =  {'контроль': '#32CD32', 'лечение': '#FF00FF', 'здоровая ткань': '#98FB98'}
    cblood_color = {'контроль': '#228B22', 'лечение': '#EE82EE', 'здоровая ткань': '#98FB98'}
    sto2_color = {'контроль': '#008000', 'лечение': '#800080', 'здоровая ткань': '#98FB98'}
    cchr_color = {'контроль': '#006400', 'лечение': '#DA70D6', 'здоровая ткань': '#98FB98'}

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('white')
    if option == 'Cwater':
        pal = water_colors
    if option == 'Cblood':
        pal = cblood_color
    if option == 'saturation':
        pal = sto2_color
    if option == 'mua_chr':
        pal = cchr_color

    sns.boxplot(data=df_plot,
                y=option, x = 'day', hue = 'group',
                palette=base_colors, linewidth=3, fill=True,
                gap= 0.3, legend=False) #palette=base_colors,
    sns.stripplot(data=df_plot, y=option, x = 'day', hue = 'group',
                  linewidth = .8, dodge=True,
                  palette=pal, alpha=0.6, size=6)#, palette = "Set3") dodge=True palette=pal,
    ax.tick_params(labelsize=12)
    ax.yaxis.grid(True)
    ax.set_title(title_, fontsize=14)
    ax.set_ylabel(option, fontsize=14)
    ax.set_xlabel('Дни регистрации', fontsize=14)
    ax.legend(fontsize = "14",
              loc='upper center', bbox_to_anchor=(0.47, -0.09),
              fancybox=True, shadow=True, ncol=2)
    import pathlib
    import os
    from pathlib import Path
    save_path = pathlib.Path('C:/') /'Users'/'user'/'Projects'/'Xenia_calculations'/'images'/'dinamics'
    from datetime import datetime
    file_name = '{}.png'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    fig.savefig(os.path.join(save_path, file_name))
    return

def sns_boxp_dinam (df_plot, option, title_): #боксплоты без точек
    import seaborn as sns
    import matplotlib.pyplot as plt
    water_colors =  {'контроль': '#32CD32', 'лечение': '#FF00FF', 'здоровая ткань': '#98FB98'}
    cblood_color = {'контроль': '#228B22', 'лечение': '#EE82EE', 'здоровая ткань': '#98FB98'}
    sto2_color = {'контроль': '#008000', 'лечение': '#800080', 'здоровая ткань': '#98FB98'}
    cchr_color = {'контроль': '#006400', 'лечение': '#DA70D6', 'здоровая ткань': '#98FB98'}

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.set_style('white')
    if option == 'Cwater':
        pal = water_colors
    if option == 'Cblood':
        pal = cblood_color
    if option == 'saturation':
        pal = sto2_color
    if option == 'mua_chr':
        pal = cchr_color

    sns.boxplot(data=df_plot,
                y=option, x = 'day', hue = 'group',
                palette=pal, linewidth=3, fill=True,
                gap= 0.3) #palette=base_colors,
    ax.tick_params(labelsize=12)
    ax.yaxis.grid(True)
    ax.set_title(title_, fontsize=14)
    ax.set_ylabel(option, fontsize=14)
    ax.set_xlabel('Дни регистрации', fontsize=14)
    ax.legend(fontsize = "14", loc='upper center',
              bbox_to_anchor=(0.47, -0.09),
              fancybox=True, shadow=True, ncol=2) #fontsize = "14", loc='upper center', bbox_to_anchor=(0.47, -0.09), fancybox=True, shadow=True, ncol=2
    import pathlib
    import os
    from pathlib import Path
    save_path = pathlib.Path('C:/') /'Users'/'user'/'Projects'/'Xenia_calculations'/'images'/'dinamics'
    from datetime import datetime
    file_name = '{}.png'.format(datetime.now().strftime("%d%m%Y_%H%M%S"))
    fig.savefig(os.path.join(save_path, file_name))
    return


def plotly_boxplots_dinamics (df_plot, option, title_, view='svg'): #боксплоты для каждой мыши по дням
    if view == 'browser':
        import plotly.io as pio
        pio.renderers.default='browser'
    if view == 'svg':
        import plotly.io as pio
        pio.renderers.default='svg'

    import plotly.express as px
    from plotly.offline import plot

    fig = px.box(df_plot, x = 'day', y=option, color="number",
                 category_orders={ # replaces default order by column name
                     "day": ["12", "15", "17", "22","24"]})
    # fig.update_traces(width=0.1)
    fig.update_layout(title_text=title_, height=800, width=1200)
    fig.show()
    return

#%% несколько графиков динамики с заголовками по одному xlsx файлу
def join_lst(lst_): #объединяет список в строку
    str_ = ' '.join(map(str, lst_))
    return (str_)

#строит графики динамики с заданным названием с отсечкой по RMSE, удаляет area3
def create_dinamics_plots (df, option, lambd, rmse, another = False, dots_=True):
    df_plot = df [df["RMSE"]<rmse]
    df_plot = df_plot[~df_plot.Name.str.contains('area3')]
    if another == False:
        title_ =  ['Динамика изменения', option, 'по дням, RMSE <', rmse, '\n\u03bb ', lambd, ' нм']
    else:
        title_ =  ['Динамика изменения', option, 'по дням, RMSE <', rmse, '\n\u03bb ', lambd, ' нм,', another]
    title_ = join_lst(title_)

    if dots_==True:
        box_ = sns_boxp_dinam_wdots (df_plot=df_plot, option=option,
                           title_ = title_)
    else:
        box_ = sns_boxp_dinam (df_plot=df_plot, option=option,
                           title_ = title_)
    return

#строит графики по дням с заданным названием с отсечкой по RMSE, удаляет area3
def create_days_plots (df, group, option, lambd, rmse, another = False):
    df_plot = df [df["RMSE"]<rmse]
    df_plot = df_plot[~df_plot.Name.str.contains('area3')]
    if another == False:
        title_ =  ['Динамика изменения', option, 'по дням для каждой мыши в группе ', group, ' <br> RMSE <', rmse, '\n\u03bb ', lambd, ' нм']
    else:
        title_ =  ['Динамика изменения', option, 'по дням для каждой мыши в группе ', group, ' <br> RMSE <', rmse, '\n\u03bb ', lambd, ' нм,', another]
    title_ = join_lst(title_)

    if group=='контроль':
        df_plot = df_plot [df_plot["group"]=='контроль']
        box_ = plotly_boxplots_dinamics (df_plot, option, title_, view='svg')
    else:
        df_plot = df_plot [df_plot["group"]=='лечение']
        box_ = plotly_boxplots_dinamics (df_plot, option, title_, view='svg')
    return

# lst_options = ['Cblood', 'saturation', 'Cwater', 'mua_chr']
# df_g0 = df [df["group"]=='контроль']
# l = sorted (list(set( df['number'].tolist())))
#%% построение графиков динамики по всем xlsx файлам из указанной папки root_path
def all_dinamics_plots_one_folder (root_path, rmse):
    import re
    import pandas as pd
    import pathlib
    from pathlib import Path
    lst_options = ['Cblood', 'saturation', 'Cwater', 'mua_chr']
    filenames = list(root_path.rglob('*.xlsx'))
    for file in filenames:
        df = import_xl_df(file)
        df = transform_df(df, focus_group)
        str_file = str(file)
        another = re.search(r'_a\d+', str_file) #с помощью регулярок узнаю о доп параметрах
        if another == None:
            re_lambd = re.search(r'\d+_\d+', str_file)
            re_lambd = re_lambd.group(0)
            lambd = re.sub('_', '-', re_lambd)
            for option in lst_options:
                create_dinamics_plots (df, option=option, lambd=lambd, rmse=rmse, another=False, dots_=False)
                create_dinamics_plots (df, option=option, lambd=lambd, rmse=rmse, another=False, dots_=True)

        else:
            re_lambd = re.search(r'\d+_\d+', str_file)
            re_lambd = re_lambd.group(0)
            lambd = re.sub('_', '-', re_lambd)
            another = re.search(r'_a\d+', str_file)
            another = another.group(0)
            another = re.sub('_', '', another)
            another = another[0]+' = '+another[1:]
            for option in lst_options:
                create_dinamics_plots (df, option=option, lambd=lambd, rmse=rmse, another=another, dots_=False)
                create_dinamics_plots (df, option=option, lambd=lambd, rmse=rmse, another=another, dots_=True)

    return

#%%
def all_days_plots_one_folder (root_path, rmse):
    import re
    import pandas as pd
    import pathlib
    from pathlib import Path
    lst_options = ['Cblood', 'saturation', 'Cwater', 'mua_chr']
    group = ['контроль','лечение']
    filenames = list(root_path.rglob('*.xlsx'))
    for file in filenames:
        df = import_xl_df(file)
        df = transform_df(df, focus_group)
        str_file = str(file)
        another = re.search(r'_a\d+', str_file) #с помощью регулярок узнаю о доп параметрах
        if another == None:
            re_lambd = re.search(r'\d+_\d+', str_file)
            re_lambd = re_lambd.group(0)
            lambd = re.sub('_', '-', re_lambd)
            for g in group:
                for option in lst_options:
                    create_days_plots (df, group=g, option=option, lambd=lambd, rmse=rmse, another=False)
        else:
            re_lambd = re.search(r'\d+_\d+', str_file)
            re_lambd = re_lambd.group(0)
            lambd = re.sub('_', '-', re_lambd)
            another = re.search(r'_a\d+', str_file)
            another = another.group(0)
            another = re.sub('_', '', another)
            another = another[0]+' = '+another[1:]
            for g in group:
                for option in lst_options:
                    create_days_plots (df, group=g, option=option, lambd=lambd, rmse=rmse, another=another)
    return

#%% пример использования для всех файлов
import pandas as pd
import pathlib
from pathlib import Path
root_path = pathlib.Path('C:/') /'Users'/'user'/'Projects'/'данные'/'data'
focus_group = ['Rat12', 'Rat13', 'Rat14', 'Rat15', 'Rat32', 'Rat33',\
          'Rat34', 'Rat35']
all_dinamics_plots_one_folder (root_path, rmse=0.051)
#%%
all_days_plots_one_folder (root_path, rmse=0.051)

#%%520-580, пример использования для одного диапазона
df_520_580_path = Path(root_path, 'data_520_580.xlsx')
df_520_580 = import_xl_df(df_520_580_path)
df_520_580 = transform_df(df_520_580, focus_group)
lst_options = ['Cblood', 'saturation', 'Cwater', 'mua_chr']
for option in lst_options:
    create_dinamics_plots (df_520_580, option=option, lambd = '520-580', rmse = 0.051, another = False, dots_=False)
group = ['контроль','лечение']
for g in group:
    for option in lst_options:
        create_dinamics_plots (df_520_580, group=g, option=option, lambd = '520-580', rmse = 0.051, another = False)
all_dinamics_plots_one_folder (root_path, rmse=0.051)

df_plot = df_520_580 [df_520_580["RMSE"]<0.051]
df_plot = df_plot[~df_plot.Name.str.contains('area3')]
title_ =  'Динамика изменения'

sns_boxp_dinam (df_plot, option, title_)
