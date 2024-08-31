#%% Package Imports
from funs import get_clue, questioner, remove_singles
from shiny import App, reactive, render, ui
from pathlib import Path
import pandas as pd
import random as rd

#%% Data Preparation
app_dir = Path(__file__).parent

# Load data
useful_cols = ['artist', 'country', 'yearOfBirth', 'yearOfDeath',
               'name', 'year', 'price', 'material',
               'height', 'width', 'link', 'source']
art_df = pd.read_csv(app_dir / 'sdata.txt', sep='\t', usecols=useful_cols)
art_df = remove_singles(art_df)

# Game setup
rand_number = rd.randint(0, len(art_df) +1)
# Get and display image of random art
url = art_df.source.iloc[rand_number]
filename = art_df.source.iloc[rand_number].split('/')[-1]


#%% Frontend Definition
app_ui = ui.page_fluid(
    ui.row(
        ui.column(11,ui.panel_title('Artle! How much is art worth?')),
        ui.column(1, ui.input_dark_mode())
    ),
    ui.img(src=url, width='400px'),
    ui.output_text('round_number'),
    ui.column(6, ui.output_ui('input_hider')),
    ui.column(6, ui.input_action_button("submit", "Submit")),
    ui.output_text('outcome'),
    ui.output_text('clue'),
    ui.br(),
    ui.br(),
    ui.p('Data Source: Jason Shi. Art Auction Valuation, ', ui.a('GitHub Dataset', href= 'https://github.com/jasonshi10/art_auction_valuation/blob/master/data.txt'), style='font-size: 12px')
)

#%% Backend Definition
def server(input, output, session):
    # Initialize variables
    tolerance = 0.1

    @render.ui
    def input_hider():
        rounds = input.submit()+1
        if rounds <= 6:
            return ui.TagList(
                #ui.input_numeric('g', 'Enter your guess!', min=1, value=0),
                ui.input_text('g', 'Enter your guess!', None),  
            )

    # Give round
    @output
    @render.text
    def round_number():
        rounds = input.submit()+1
        remaining = 7-rounds
        if remaining > 0:
            return f'There are {remaining} rounds remaining'
        else:
            return 'There are no rounds remaining'


    # Give clue
    @output
    @render.text
    def clue():
        rounds = input.submit()+1
        clue = get_clue(art_df, rand_number, rounds)
        return clue
    
    # Give answer
    @output
    @render.text
    def real_price():
        return art_df.price.iloc[rand_number]

    # Render result based on guess
    @output
    @render.text
    @reactive.event(input.submit)
    def outcome():
        #answer = input.g()
        rounds = input.submit()+1
        out = questioner(art_df, rand_number, input.g(), rounds, tolerance)
        return out

    @reactive.effect
    @reactive.event(input.submit)
    def _():
        ui.insert_ui(ui.p(input.g()), selector='#g', where='afterEnd')

#%% Run App
app = App(app_ui, server)

