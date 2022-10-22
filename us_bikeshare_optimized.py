import pandas as pd
import datetime as dt

# Declare some CONSTANTS for validating user inputs
CITIES = {'Chicago': './data/chicago.csv',
          'New York': './data/new_york_city.csv',
          'Washington': './data/washington.csv'}

DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday']

MONTHS = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']


def load_data():

    """Loads one of the three datasets.

    Args:
        This function takes no arguments.

    Returns:
        loaded_data (pd.DataFrame): The requested dataset.
        None: if the user have chosen to quit.
    """

    # Print some user instructions
    print("\nPlease, choose on of the following datasets:")
    print("  1. Chicago,")
    print("  2. New York,")
    print("  3. Washington.")
    print("NOTE: you can quit by pressing <enter>.")

    while True:
        # Get the user input
        user_input = input("City: ").strip().title()

        # Validate the user input
        if not user_input:
            print("\nThank you!")
            return None
        elif user_input in CITIES:
            print("\nLoading data..")
            loaded_data = pd.read_csv(filepath_or_buffer=f"{CITIES[user_input]}",
                                      parse_dates=['Start Time', 'End Time']).iloc[:, 1:]
            print("Done!")
            return loaded_data
        else:
            print("\nPlease, make sure to type the city name correctly!\n")


def get_data_ready(raw_data):

    """Set the correct data types & create new columns as needed.

    Args:
        raw_data (pd.DataFrame): data before processing.

    Returns:
        data (pd.DataFrame): data after processing.
    """

    print("\nProcessing data..")

    # Drop NaNs
    raw_data.dropna(inplace=True)

    # Rename columns
    raw_data.rename(columns=lambda x: x.replace(' ', '_').lower(), inplace=True)

    # Reset data type for birth_year
    if 'birth_year' in raw_data.columns:
        raw_data['birth_year'] = raw_data['birth_year'].astype(int)

    # Create new columns as needed
    raw_data['month'] = raw_data['start_time'].dt.strftime("%B")
    raw_data['day'] = raw_data['start_time'].dt.strftime("%A")
    raw_data['start_hour'] = raw_data['start_time'].dt.strftime("%I %p")
    raw_data['travel_time'] = (raw_data['end_time'] - raw_data['start_time']).dt.total_seconds() // 60
    raw_data['start_end_combination'] = raw_data['start_station'] + " | " + raw_data['end_station']

    # Return data after processing
    processed_data = raw_data
    print('Done!')
    return processed_data


def explore_data(data):

    """Views a segment of data according to the user's request.

    Args:
        data (pd.DataFrame): the dataset being explored.

    Returns:
        This function returns nothing.
    """

    # Print some user instructions
    print('\nYou can explore data by viewing a defined numer of rows at a time.')
    print("NOTE: you can quit by pressing <enter>.")

    i = 0
    while True:
        # Get the user input
        rows = input('\nNumber of rows: ').strip()

        # Validate the user input
        if not rows:
            print("\nThank you!")
            break
        if rows.isnumeric():
            rows = int(rows)
            print('\n')
            print(data[i:i+rows])
            i += rows
        else:
            print("\nPlease, make sure to type number correctly!\n")


def filter_data(data):

    """Filters the data according to the user's request.

    Args:
        data (pd.DataFrame): data before being filtered.

    Returns:
        data (pd.DataFrame): data after being filtered.
    """

    # Print some user instructions
    print("\nYou can filter the data either by day or month,")
    print("  1. Weekday: Saturday - Friday.")
    print("  2. Month: January - December.")
    print("NOTE: you can enter any number of words separated by a space.")
    print("NOTE: you can quit by pressing enter.")

    while True:
        # Get the user filters
        user_filters = input("\nFilter by: ").strip().title().split(' ')
        filter_by = [f for f in user_filters if f in (*DAYS, *MONTHS)]

        # Validate the user input
        if len(user_filters) == 1 and not user_filters[0]:
            print("\nProceeding with data analysis without filtration..")
            return data
        elif len(filter_by) == len(user_filters):
            print("\nFiltering data..")
            mask = data.isin(filter_by).any(axis=1)
            filtered_data = data[mask]
            print("Done!")
            return filtered_data
        else:
            print("\nIt appears that you have one or typo(s)!")
            print("Please, make sure to type day / month name correctly!\n")


def time_stats(data):

    """Displays statistics on the most frequent times of travel.

    Args:
        data (pd.DataFrame): the data used in calculation.

    Returns:
        This function returns nothing.
    """

    # Marking the start time
    start = dt.datetime.now()

    # The most common month
    most_common_month = data['month'].value_counts(ascending=False).index[0]
    print(f"Most common travel month: {most_common_month},")

    # The most common month
    most_common_day = data['day'].value_counts(ascending=False).index[0]
    print(f"Most common travel day: {most_common_day},")

    # The most common month
    most_common_hour = data['start_hour'].value_counts(ascending=False).index[0]
    print(f"Most common travel hour: {most_common_hour}.")

    # Marking the end time
    end = dt.datetime.now()
    time_delta = end - start
    print(f"\nThis took {time_delta.total_seconds()} seconds.")


def station_stats(data):

    """
    Displays statistics on the most popular stations and trip.

    Args:
        data (pd.DataFrame): the data used in calculation.

    Returns:
        This function returns nothing.
    """

    # Marking the start time
    start = dt.datetime.now()

    # The most common start station
    most_common_start = data['start_station'].value_counts(ascending=False).index[0]
    print(f"Most common start-end combination: {most_common_start}.")

    # The most common end station
    most_common_end = data['end_station'].value_counts(ascending=False).index[0]
    print(f"Most common start-end combination: {most_common_end}.")

    # The most common start-end combination
    most_common_combination = data['start_end_combination'].value_counts(ascending=False).index[0]
    print(f"Most common start-end combination: {most_common_combination}.")

    # Marking the end time
    end = dt.datetime.now()
    time_delta = end - start
    print(f"\nThis took {time_delta.total_seconds()} seconds.")


def trip_duration_stats(data):

    """
    Displays statistics on the total and average trip duration.

    Args:
        data (pd.DataFrame): the data used in calculation.

    Returns:
        This function returns nothing.
    """

    # Marking the start time
    start = dt.datetime.now()

    # The mean travel time
    mean_travel_time = data['travel_time'].mean()
    print(f"Mean travel time: {round(mean_travel_time, 2)} minutes.")

    # The total travel time
    total_travel_time = data['travel_time'].sum()
    print(f"Total travel time: {round(total_travel_time/60, 2)} hours.")

    # Marking the end time
    end = dt.datetime.now()
    time_delta = end - start
    print(f"\nThis took {time_delta.total_seconds()} seconds.")


def user_stats(data):

    """
    Displays statistics on bike-share users.

    Args:
        data (pd.DataFrame): the data used in calculation.

    Returns:
        This function returns nothing.
    """

    # Marking the start time
    start = dt.datetime.now()

    # The counts of user type
    subscribers = len(data.query("user_type == 'Subscriber'"))
    customers = len(data.query("user_type == 'Customer'"))
    print(f"Counts of user types:")
    print(f"  1. Subscribers: {subscribers},")
    print(f"  2. Customers: {customers}.")

    # The counts of gender
    if 'gender' in data.columns:
        males = len(data.query("gender == 'Male'"))
        females = len(data.query("gender == 'Female'"))
        print(f"\nCounts of user genders:")
        print(f"  1. Males: {males},")
        print(f"  2. Females: {females}.")
    else:
        print("\nNOTE: this dataset has no information about user genders.")

    # The earliest, most recent, and most common year of birth
    if 'birth_year' in data.columns:
        earliest_birth_year = data['birth_year'].min()
        print(f"\nEarliest birth year: {earliest_birth_year},")

        most_recent_birth_year = data['birth_year'].max()
        print(f"Most recent birth year: {most_recent_birth_year},")

        most_common_birth_year = data['birth_year'].mode()[0]
        print(f"Most common birth year: {most_common_birth_year}.")
    else:
        print("\nNOTE: this dataset has no information about user birth year.")

    # Marking the end time
    end = dt.datetime.now()
    time_delta = end - start
    print(f"\nThis took {time_delta.total_seconds()} seconds.")


def main():

    """Executes the script."""

    outer_loop = True
    while outer_loop:
        # Load the data
        city_raw_data = load_data()

        # Give the user the option to quit
        if city_raw_data is None:
            break

        # Continue with the analysis process
        city_data = get_data_ready(city_raw_data)

        # Explore data
        explore_data(city_data)

        # Filter data
        city_data_filtered = filter_data(city_data)

        # View time stats
        print('*' * 20)
        time_stats(city_data_filtered)

        # View station stats
        print('*' * 20)
        station_stats(city_data_filtered)

        # View trip duration stats
        print('*' * 20)
        trip_duration_stats(city_data_filtered)

        # View user stats
        print('*' * 20)
        user_stats(city_data_filtered)
        print('*' * 20)

        # Ask if the user wants to repeat the whole process
        print("\nYou can proceed to analyzing another dataset if you would like!")

        while True:
            print("\nPress any key to restart, or you can quit by pressing <enter>.")
            to_repeat = input('Restart? ').strip().lower()
            if to_repeat == '':
                print("\nThank you!")
                outer_loop = False
                break
            else:
                print('\nRestarting..')
                break


if __name__ == "__main__":
    main()
