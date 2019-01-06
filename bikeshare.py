import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_mod(input_print, error_print, enterable_list):
    while True:
        ret = input(input_print)
        ret = ret.lower()
        if ret in enterable_list:
            return ret
        else:
            print(error_print)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input_mod('Would you like to see data from Chicago, New York City, or Washington? \n',
                    'This input is not valid.',
                    ['chicago', 'new york city', 'washington'])

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input_mod("Would you like to see data for January, February, March, April, May, June, or all? \n",
    'This input is not valid.', ['january', 'february', 'march', 'april', 'may', 'june', 'all'])

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_mod("Would you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? \n",
    'This input is not valid.', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    month_reference = ["January", "February", "March", "April", "May", "June"]
    most_common_month = month_reference[most_common_month - 1]
    print('The most common month is: ', most_common_month, '\n')

    # TO DO: display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is: ', most_common_day_of_week, '\n')

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', most_common_start_hour, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start = df.groupby(['Start Station']).count().sort_values(by=['Start Time'], ascending = False).index[0]
    print('The most commonly used start station is: ', start, '\n')

    # TO DO: display most commonly used end station
    end = df.groupby(['End Station']).count().sort_values(by=['Start Time'], ascending = False).index[0]
    print('The most commonly used end station is: ', end, '\n')

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " -> " + df["End Station"]
    combination = df.groupby(['combination']).count().sort_values(by=['Start Time'], ascending = False).index[0]
    print('The most frequent combination of start station and end station trip is: ', combination, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: ', total_travel_time, '\n')

    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: ', avg_travel_time, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        print("There are {} subscribers". format(df['User Type'].value_counts()[0]))
    except:
        print("There are no subscribers")
    try:
        print(", and {} customers". format(df['User Type'].value_counts()[1]))
    except:
        print(", and no customers")
    try:
        print(", and {} dependents.\n". format(df['User Type'].value_counts()[2]))
    except:
        print(", and no dependents.\n")

    # TO DO: Display counts of gender
    try:
        print("There are {} male and {} female users.\n".format(df['Gender'].value_counts()[0], df['Gender'].value_counts()[1]))
    except:
        print("This dataset does not contain gender information.\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = df["Birth Year"].sort_values(ascending = True).iloc[0]
        recent = df["Birth Year"].sort_values(ascending = False).iloc[0]
        common = df["Birth Year"].mode().iloc[0]
        print("The earliest year of birth is: ", int(earliest))
        print("The most recent year of birth is: ", int(recent))
        print("The most common year of birth is: ", int(common))
    except:
        print("This dataset does not contain year of birth information.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
