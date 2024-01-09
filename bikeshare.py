#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**** Exploring US Bikeshare Data - Practical Project - UDACITY

Created on Jan 5, 2024 

@author: Frederik Lipowsky
"""

import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose the city you want to analyze (Chicago, New York City, Washington)\n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city. Please enter either Chicago, New York City or Washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month do you want to analyze? Please enter all, January, February, March, ...\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid time selection. Please enter either all, january, february, etc.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of the week want to analyze? Please enter all, monday, tuesday, ...\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day selection. Please enter either all, monday, tuesday, etc.')

    print('-'*40)
    print('The analysis will be performed for city: {}, month: {}, day: {}\n'.format(city, month, day))
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
    
    #set printing options to display all columns - for debugging purposes
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)    
    
    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    #convert start time colum to data type datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
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
    """Displays statistics on the most frequent times of travel.
    Args:
        (DataFrame) df - Pandas DataFrame with the city data filtered by previous functions
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = df['month'].mode()[0]
    
    #convert int month to string
    print('Most Popular Start Month:', months[popular_month-1])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (DataFrame) df - Pandas DataFrame with the city data filtered by previous functions
    """
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_station_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()    
    print('Most Popular Combination of Start and End Station: "{}" and "{}"'.format(popular_station_combination[0], popular_station_combination[1]))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (DataFrame) df - Pandas DataFrame with the city data filtered by previous functions
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    # print total travel time - convert seconds to days
    print('The Total travel time is: ', total_travel_time/86400, ' days.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: ', mean_travel_time/60, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (DataFrame) df - Pandas DataFrame with the city data filtered by previous functions
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_string(), '\n')
    
    # Display counts of gender - error handling for data sets without gender attribute
    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count.to_string(), '\n')
    except KeyError:
        print('Gender Types: No data available for this data set')

    # Display earliest, most recent, and most common year of birth - include error handling for null values 
    try:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year: ', earliest_birth_year)
    except KeyError:
        print('Earliest Birth Year: No data available for this data set')

    try:
        recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year: ', recent_birth_year)
    except KeyError:
        print('Most recent Birth Year: No data available for this data set')
    
    try:
        common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('Most Common birth year: ', common_birth_year)
    except KeyError:
        print('Most common Birth Year: No data available for this data set')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displays raw data when requested by user.
    Args:
        (DataFrame) df - Pandas DataFrame with the city data filtered by previous functions
    """
    #print first 5 rows of raw data from data frame
    print("\nFirst 5 rows of raw data: \n")
    row_index = 0 #row count from where the next 5 rows should be shown
    print(df.head(5))
    
    # Check if user wants to show the next 5 rows
    while True:
        next_raw_data = input('\nWould you like to query the next 5 rows of raw data? Enter yes or no.\n').lower()
        if next_raw_data == 'no':
            return
        elif next_raw_data == 'yes':
            row_index += 5
            print(df.iloc[row_index:row_index+5])
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Ask for raw data view - call function
        while True:
            raw_data = input('Would you like to query the first 5 rows of raw data? Please Enter yes or no.\n').lower()
            if raw_data == 'no':
                break
            elif raw_data == 'yes':
                show_raw_data(df)
                break

        restart = input('\nWould you like to restart? Please Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()