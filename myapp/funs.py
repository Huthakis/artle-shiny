# Packages
import pandas as pd

# Function to remove artists that only appear once
def remove_singles(data):
    # Count the occurrences of each artist
    artist_counts = data['artist'].value_counts()
    # Filter artists that appear more than once
    artists_to_keep = artist_counts[artist_counts > 1].index
    # Keep only rows where the artist is in the list of artists to keep
    filtered_data = data[data['artist'].isin(artists_to_keep)]
    # Return data
    return filtered_data

def questioner(data, rand_number, guess, rounds, tolerance):
    # Logic for game
    if rounds <= 6:
        # Get user guess
        answer = guess
        try:
            answer = float(answer)
        except ValueError:
            answer = 0
        print('Your answer: $' + str(answer))
        # Logic for checking guess
        if answer == data.price.iloc[rand_number]:
            return f'You are right! The exact price was ${data.price.iloc[rand_number]}.'
        elif data.price.iloc[rand_number] * (1 - tolerance) <= answer <= data.price.iloc[rand_number] * (1 + tolerance):
            return f'You are within {100 * tolerance}%. The exact price was ${data.price.iloc[rand_number]}.'
        elif answer > data.price.iloc[rand_number]:
            return 'Too High'
        elif answer < data.price.iloc[rand_number]:
            return 'Too low'
        else:
            pass
        
    else:
        return f'''Out of rounds! This is {data.name.iloc[rand_number]}, by {data.artist.iloc[rand_number]}, and it was auctioned for ${data.price.iloc[rand_number]}'''
    #os.remove(file)  # Delete the downloaded image file

# Function for future seperation of questioner and clues
def get_clue(data, rand_number, rounds):
        if rounds == 1:
            return 'Make your first guess!'
        if rounds == 2:
            return f'The art is called: {data.name.iloc[rand_number]}'
        elif rounds == 3:
            return f'The artist is from: {data.country.iloc[rand_number]}'
        elif rounds == 4:
            if pd.isna(data.yearOfDeath.iloc[rand_number]):
                return 'The artist is alive.'
            else:
                return f'The artist died in: {data.yearOfDeath.iloc[rand_number]}'
        elif rounds == 5:
            return f'The artist is: {data.artist.iloc[rand_number]}'
        elif rounds == 6:
            artist_prices = data[data['artist'] == data.artist.iloc[rand_number]].price
            artist_other = artist_prices[artist_prices != data.price.iloc[rand_number]].sample(n=1).values[0]
            return f'Other art by this artist has sold for: ${artist_other}'
        else:
            return ''
