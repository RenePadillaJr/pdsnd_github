import time
import pandas as pd
from collections import Counter

import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    input_valid = False
    while not input_valid:
        city = input("Please select one of the following cities: Chicago, New York City, or Washington.\n").lower()
        if city in CITY_DATA.keys():
            input_valid = True
        else:
            print("Invalid input. Please try again.")
            city = ""

    # TO DO: get user input for month (all, january, february, ... , june)
    input_valid = False
    months = ["january", "february", "march", "april", "may", "june", "july", "august",
              "september", "ocotober", "november", "december", "all"]

    month = input("Please select the month you would like to analyze. Select 'all' for all months.\n").lower()
    if month in months:
        input_valid = True
    else:
        print("Invalid input. Please try again.")
        month = ""

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    input_valid = False
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

    while not input_valid:
        day = input("Please select the day of the week you would like to analyze. Select 'all' for all days.\n").lower()
        if day in days:
            input_valid = True
        else:
            print("Invalid input. Please try again.")
            days = ""

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june", "july", "august",
                  "september", "ocotober", "november", "december", "all"]
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

    ## convert the Start Time column to datetime
    # df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    # Get the current month (as a name)
    months = ["january", "february", "march", "april", "may", "june", "july", "august",
              "september", "ocotober", "november", "december", "all"]
    print('Most Frequent Month:', months[popular_month + 1].title())

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week:', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour (24 Hour Notation):', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent_combination = combination_counts.loc[combination_counts['count'].idxmax()]
    most_frequent_combination_dict = most_frequent_combination.to_dict()

    print('Most Frequent Combination of Start and End Stations:')
    print(f"\t\tStart Station: {most_frequent_combination_dict['Start Station']}")
    print(f"\t\tEnd Station: {most_frequent_combination_dict['End Station']}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total Travel Time (In Minutes):", total_time)

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean Travel Time (In Minutes):", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("Counts of User Types:", user_counts)

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Counts of Gender:", gender_count)
    else:
        print("Gender data not available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print("Earliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", recent_year)
        print("Most Common Year of Birth:", common_year)
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("Birth Year data not available for this city.")

    print('-'*40)

def user_display_raw_data(df):
    display_raw_data = True
    count =1
    while display_raw_data:
        if count == 1:
            raw = input("\nWould you like to see the first 5 lines of raw data?\n").lower()
        else:
            raw = input("\nWould you like to see the next 5 lines of raw data?\n").lower()
        if raw != 'yes': display_raw_data = False
        else:
            for index, row in df.iterrows():
                print(row)
                if index >= count + 4:
                    count += 5
                    break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    print("This is a new line of code. From Section IV: Refactor Code of Rubric")
    print("This is a new line of code (second change). From Section IV: Refactor Code of Rubric")
    main()
