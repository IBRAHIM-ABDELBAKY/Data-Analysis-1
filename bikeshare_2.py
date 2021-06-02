import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York or Washington?\n')
        city =city.lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print ('please select one of (Chicago, New York or Washington)!\n')
    
    # get user filter type
    filter_type = input('Would you like to filter the data by month, day or no-filters? Type "none" for no-filters.\n')    
    
    if filter_type.lower() == 'none':
        month = 'none'
        day = 'none'
        print('It looks like you want see data for {} city without any time filter!\nIf this is not true restart the program!\n'.format(city.title()))
   
   # get user input for month (all, january, february, ... , june)
    if filter_type.lower() == 'month':
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        mon = input('Which month?  (Jan, Feb, Mar, Apr, May, Jun)\n')
        day = 'none'
        month = months.index(mon.title()) + 1
        print('It looks like you want see data for {} city filterd by {} month!. If this is not true restart the program!\n'.format(city.title(), mon.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_type.lower() == 'day':
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        da_abb = ['Sa', 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr']
        da = input('Which day?  (Sa, Su, Mo, TU, We, Th, Fr)\n')
        day = days[da_abb.index(da.title())]
        month = 'none'
        print('It looks like you want see data for {} city filterd by {} day!. If this is not true restart the program!\n'.format(city.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if month != 'none':
        df['month'] = df['Start Time'].dt.month
        df = df[df['month'] == month]
    if day != 'none':
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df = df.loc[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel According to Filters...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    comon_month = df['month'].mode()[0]
    print('Month',comon_month)
    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    comon_day = df['day'].mode()[0]
    print('Day', comon_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    comon_hour = df['hour'].mode()[0]
    print('Hour', comon_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    comon_start = df['Start Station'].mode()[0]
    print('Start Station:    ',comon_start)

    # display most commonly used end station
    comon_end = df['End Station'].mode()[0]
    print('End Station:    ',comon_end)

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).idxmax()
    print('Most Popular Trip is From "{}" to "{}"'.format(frequent_combination[0],frequent_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['diff'] = df['End Time'] - df['Start Time']
    total_time = df['diff'].sum()
    print('Total Trip Duration = ',total_time)
    # display mean travel time
    aver_time = np.mean(df['diff'])
    print('Average Trip Duration = ', aver_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df.groupby(['User Type']).size()
    print(types)
    print()
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df.groupby(['Gender']).size()
        print(gender)
        print()
    else:
        print('No Gender Data!\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        print('Oldest Birth Year', earliest)
        print()
        recet = int(df['Birth Year'].max())
        print('Youngest Birth Year', recet)
        print()
        comm = int(df['Birth Year'].mode()[0])
        print('Popular Birth Year ', comm)
    else:
        print('No Birth Year!\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
