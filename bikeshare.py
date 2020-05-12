import time
import pandas as pd
import numpy as np
import calendar

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
    month_allowed = ['all', 'january', 'february', 'march','april', 'may', 'june']
    days_allowed = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington? ")
    while city.lower() not in CITY_DATA:
        city = input("Data for the city {} does not exist. Please enter Chicago, New York City or Washington. ".format(city))
                    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Would you like to filter the data by month or all (all, january, february, ... , june)?")
    while month.lower() not in month_allowed:
        month = input("Month {} does not exist. Please enter all, january, february, ... or june. ".format(month))
           
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Would you like to filter the data by day or all (all, monday, tuesday, ... sunday)?")
    while day.lower() not in days_allowed:
        day = input("Day {} does not exist. Please enter all, monday, tuesday, ... or sunday. ".format(day))    
    

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
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month,day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour    
    
    
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
        
    #Handle nan
    if 'Birth Year' in df.columns:
        df[['Birth Year']] = df[['Birth Year']].fillna(value=9999)
        df[['Birth Year']] = df[['Birth Year']].astype(int)
    if 'Gender' in df.columns:
        df[['Gender']] = df[['Gender']].fillna(value='Unknown')
        
    return df  

                                               
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is {}".format(calendar.month_name[int(df['month'].mode().to_string(index=False))]))
    
    # TO DO: display the most common day of week
    print("The most common day of week{}".format(df['day_of_week'].mode().to_string(index=False)))

    # TO DO: display the most common start hour
    print("The most common start hour is{}".format(df['hour'].mode().to_string(index=False)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
                                               
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is{}".format(df['Start Station'].mode().to_string(index=False)))

    # TO DO: display most commonly used end station
    print("The most commonly used end station is{}".format(df['End Station'].mode().to_string(index=False)))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station']     = df['Start Station'] + ' to ' + df['End Station']   
    print("The most frequent combination of start station and end station trip is{}".format(df['Start End Station'].mode().to_string(index=False)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    
                                               
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time is {}".format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print("The mean travel time is {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
                                               
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types:")
    print( df.groupby('User Type').size().to_string())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of gender:")
        print(df.groupby('Gender').size().to_string())
    else:
        print("\nNo gender information included.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df_birth = df[df['Birth Year'] < 9999]
        print("\nThe earliest year of birth is {}".format(df_birth['Birth Year'].min()))
        print("The most recent year of birth is {}".format(df_birth['Birth Year'].max()))
        print("The most common year of birth is{}".format(df_birth['Birth Year'].mode().to_string(index=False)))
        
    else:
        print("\nNo birth year information included.") 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def see_stats(df):    
    lines_from = 0
    lines_to   = 5
    
    while input("Do you want so see the first 5 lines of raw data (yes/no) ?") == 'yes':
        print(df.iloc[lines_from:lines_to, :])
        lines_from +=5
        lines_to   +=5
    
    
                                               
def main():
    while True:
        city, month, day = get_filters()         
        df = load_data(city, month, day) 
        see_stats(df)
        time_stats(df)
        station_stats(df) 
        trip_duration_stats(df)        
        user_stats(df)
                                               
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
