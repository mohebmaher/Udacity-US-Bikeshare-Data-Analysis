# Importing necessary libraries:
import pandas as pd
import datetime as dt


# Defining the available data sets & their associated file names:
cities = {'Chicago': 'chicago.csv',
          'New York': 'new_york_city.csv',
          'Washington': 'washington.csv'}


# Defining a greeting function:
def greeting_func():
    
    """
    Asks the user for his name.
    
    Args: Takes no args.
    
    Returns:
    prints a customized greeting message.
    (str) name.
    """
    
    # Defining the greeting according to current_hour:
    current_hour = dt.datetime.now().hour
    if current_hour < 5:
        greeting = 'Hi'
    elif current_hour < 12:
        greeting = 'Good morning'
    elif current_hour < 17:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    # Asking for name:
    name = input(
        'To customize this experience, please enter your name (to skip press enter): '
    ).strip().title()

    if name == '':
        name = 'reviewer'

    while True:
        confirm_msg = input(f'''
Thanks {name},
To confirm your name press enter,
To change it enter the new name: ''').strip().title()
        
        if confirm_msg == '':
            break
        else:
            name = confirm_msg
            
    print(f'''
{greeting} {name},
Looking forward to learn from your reviews & thanks in advance for your time!''')
    
    # Returning name:
    return name


# Defining a function to load the data:
def loading_func(cities):
    
    """
    Asks for which dataset to lead.
    
    Args:
    (dict) the dictionary containing city names & their associated files.
    
    Returns:
    (pandas dataframe) the required data set.
    """

    while True:
        # Asking for city name:
        print('\nYou can load the dataset for: Chicago, New York City or Washington.')
        city = input('Enter city name: ').strip().title()

        # Confirming city name:
        confirm_msg = input(f'''
You are loading the dataset for {city},
To confirm the city name press enter,
To change it enter the new name: ''').strip().title()

        # Assigning the city name:
        if confirm_msg:
            city = confirm_msg

        # Handling errors:
        try:
            file_name = cities[city]

        except KeyError:
            print('\nSomething went wrong! Make sure to type city name correctly!')

        else:
            # Loading data:
            print(f'\nLoading data for {city}..')
            folder = './data/'
            df = pd.read_csv(folder+file_name, parse_dates=['Start Time', 'End Time']).drop(columns='Unnamed: 0')
            print('Done!')

            # Renaming columns for more convenience:
            df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)

            # Creating the necessary extra columns:
            df['start_day'] = df['start_time'].dt.strftime('%A')
            df['start_month'] = df['start_time'].dt.strftime('%B')
            df['start_hour'] = df['start_time'].dt.strftime('%H')
            df['start_to_end'] = 'from ' + df['start_station'] + ' to ' + df['end_station']

            # Ending the loop
            break
            
    return city, df


# Defining a function to explore the raw data::
def exploring_func(df):
    
    """
    Asks for the number of rows by which the data set will be viewed.
    
    Args:
    (pandas dataframe) the data set to be explored.
    
    Returns:
    printing out the data according to the required number of rows.
    """
    
    i = 0
    while True:
        
        # Handling errors:
        try:
            # Asking for number of rows:
            print('\nYou can explore data by viewing a defined numer of rows at a time,')
            explore = input('Number of rows (to skip press enter): ').strip()
            
            # Validating input(s):
            if explore != '' and not explore.isnumeric():
                raise ValueError
                
        except ValueError:
            print('\nPlease, enter the number correctly!')
            
        else:
            if explore == '':
                break
            else:
                rows = int(explore)
                print('\n')
                print(df[i:i+rows])
                i += rows


# Defining a function to filter the data:
def filtering_func(df):
    
    """
    Asks for the time frame by which the data will be filtered.
    
    Args:
    (pandas dataframe) the data set to be filtered.
    
    Returns:
    (pandas dataframe) the data set after being filtered.
    """
    
    to_continue = True
    while True:

        try:
            
            # Asking for filtering:
            print('\nYou can filter data by day, month or both.')
            do_filter = input('Continue? (y/n) ').strip().lower()

            # Validating inputs:
            if do_filter == 'n':
                break
            elif do_filter != 'y':
                raise Exception
            
            # Asking for time_filter:
            print('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
            day = input('You can enter more than one day separated by a space: ').strip().title().split(' ')
            
            print('\nWhich month - January, February, March, April, May, or June?')
            month = input('You can enter more than one day separated by a space: ').strip().title().split(' ')
            
            time_filter = day + month
            time_filter =[ x for x in time_filter if x in df[['start_day', 'start_month']].to_numpy()]

            # Validating inputs:
            if len(time_filter) == 0:
                raise Exception

        # Handling errors:
        except:
            print('\nSomething went wrong! Make sure to type day / month name correctly')

        else:
            
            # Defining & applying mask:
            filter_by = df[['start_day', 'start_day']].isin(time_filter).any(axis=1)
            df = df.query("@filter_by").copy()
            
            # Ending loop:
            break
    
    return df


# Defining available options for statistics & their associated result name, column name, action:
options = {'1': {'result': 'Most common month:',
                 'column': 'start_month',
                 'return_func': lambda series: series.mode()[0]},
           '2': {'result': 'Most common day of the week:',
                 'column': 'start_day',
                 'return_func': lambda series: series.mode()[0]},
           '3': {'result': 'Most common hour of the day:',
                 'column': 'start_hour',
                 'return_func': lambda series: series.mode()[0]},
           '4': {'result': 'Most common start station:',
                 'column': 'start_station',
                 'return_func': lambda series: series.mode()[0]},
           '5': {'result': 'Most common end station:',
                 'column': 'end_station',
                 'return_func': lambda series: series.mode()[0]},
           '6': {'result': 'Most common trip from start to end:',
                 'column': 'start_to_end',
                 'return_func': lambda series: series.mode()[0]},
           '7': {'result': 'Total travel time (in hours):',
                 'column': 'trip_uration',
                 'return_func': lambda series: series.sum()},
           '8': {'result': 'Average travel time (in hours):',
                 'column': 'trip_duration',
                 'return_func': lambda series: round(series.mean(), 2)},
           '9': {'result': 'Counts of each user type:\n',
                 'column': 'user_type',
                 'return_func': lambda series: series.value_counts().to_dict()},
           '10': {'result': 'Counts of each gender:\n',
                  'column': 'gender',
                  'return_func': lambda series: series.value_counts().to_dict()},
           '11': {'result': 'Earliest year of birth:',
                  'column': 'birth_year',
                  'return_func': lambda series: int(series.min())},
           '12': {'result': 'Most recent year of birth:',
                  'column': 'birth_year',
                  'return_func': lambda series: int(series.max())},
           '13': {'result': 'Most common year of birth:',
                  'column': 'birth_year',
                  'return_func': lambda series: int(series.mode()[0])}}


# Defining printing_func:
def printing_statistics(options, df):
    
    """
    Asks for the required statistics by which the data set will be analyzed.
    
    Args:
    (dict) a dictionary containing the available options for statistics.
    (pandas dataframe) the data set to be analyzed.
    
    Returns:
    printing out the required statistics.
    
    """
    
    outer_loop = True
    while outer_loop:
        
        # Printing out user instructions:
        print('''
Here is a list of the available options:
1. Most common month.
2. Most common day of week.
3. Most common hour of day.
4. Most common start station.
5. Most common end station.
6. Most common trip from start to end.
7. Total travel time.
8. Average travel time.
9. Counts of each user type.
10. Counts of each gender (only available for NYC and Chicago).
11. Earliest year of birth (only available for NYC and Chicago).
12. Most recent year of birth (only available for NYC and Chicago).
13. Most common year of birth (only available for NYC and Chicago).

Please, make sure to type the corresponding number correctrly,
You can also print out all statistics at once by typing 'all',
Or you can skip at anytime by pressing enter.''')
        
        # Handling errors:
        try:
            # Asking for the required statistics:
            option = input('Number: ').strip().lower()
            
            # Validating option(s):
            if option != 'all' and option not in options:
                raise ValueError
                
        except ValueError:
            print('\nSomething went wrong! Make sure to type your option correctrly')
            
        else:
            print('\n')
            
            # Determining outputs:
            if option == 'all':
                for number, associated_dict in options.items():
                    result = associated_dict['result']
                    column = associated_dict['column']
                    if column not in df.columns:
                        print(f'{number}.', result, 'Not available for this data set!')
                    else:
                        return_func = associated_dict['return_func']
                        print(f'{number}.', result, return_func(df[column]))
            else:
                result = options[option]['result']
                column = options[option]['column']
                if column not in df.columns:
                    print(result, 'Not available for this data set!')
                else:
                    return_func = options[option]['return_func']
                    print(result, return_func(df[column]))
                                
        finally:
            inner_loop = True
            while inner_loop:
                # Ending the loop:
                confirm_msg = input('\nDo you want to continue? (y/n) ')
                if confirm_msg == 'n':
                    inner_loop = False
                    outer_loop = False
                elif confirm_msg != 'y':
                    print('something went wrong!')
                elif confirm_msg == 'y':
                    inner_loop = False


def main():
    
    outer_loop = True
    while outer_loop:
        name = greeting_func()
        city, original_data = loading_func(cities)
        exploring_func(original_data)
        filtered_data = filtering_func(original_data)
        printing_statistics(options, filtered_data)
        
        print(f'''
Dear {name},
Data analysis for {city} is completed''')
        
        inner_loop = True
        while inner_loop:        
            try:
                restart = input('Would you like to explore another data set? (y/n) ').strip().lower()
                if restart != 'y' and restart != 'n':
                    raise ValueError
                
            except ValueError:
                print('\nSomething went wrong! Make sure to type correctrly')
            
            else:
                if restart == 'y':
                    inner_loop = False
                elif restart == 'n':
                    outer_loop = False
                    inner_loop = False


if __name__ == "__main__":
    main()


# All Done!
