import time
import pandas as pd
import numpy as np
import datetime as dt

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
    cities = ['chicago', 'new york city', 'washington']
    city = ''
    while city not in cities:
        city = input('Which city do you want to explore? Please choose from Chicago, New York City or Washington. ').lower()
    print('Nice. '+city.capitalize()+' is a great choice.')


    # TO DO: get user input for month (january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = ''
    while month not in months:
        month = input('Which month do you want to investigate? ').lower()
    print(month.capitalize()+' is my favorite month. Awesome!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    day = ''
    while day not in days:
        day = input('Last but not least: Which day of the week do you want to take a look at? ').lower()
    print('You chose '+day.capitalize())

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

    # read the csv file
    data = pd.read_csv(CITY_DATA[city])

    #create a data frame containing all data
    df = pd.DataFrame(data)

    #note to myself: we need to filter the df by the month name from the user's input. The query below returns the months name only, without any filtering

    #converting the start time column with datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #converting the end time column with datetime
    df['Start Time'] = pd.to_datetime(df['End Time'])

    #extracting the month from start time
    df['month'] = df['Start Time'].dt.month

    #extracting the weekday from datetime
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if user input was not all
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #optional: print dataframe to verify if slection did work
    #print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month

    # find the most popular hour
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # TO DO: display the most common day of week
    df['dayofweek'] = df['Start Time'].dt.day_name()

    # find the most popular hour
    popular_weekday = df['dayofweek'].mode()[0]

    print('Most Popular Day Of The Week:', popular_weekday)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    #alternative approach
    """df['start_end_combination'] = df['Start Station'] + '; ' + df['End Station']
    #common_start_end_combination = df['start_end_combination'].mode()[0]
    #print('Most Commonly Used Combination of Start and End Station: ', common_start_end_combination)"""


    common_start_end_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('Most Commonly Used Combination of Start and End Station: ', common_start_end_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time in days
    total_travel_time = df['Trip Duration'].sum()/60/60/24
    print("The total travel time is :", total_travel_time, " days.")

    # TO DO: display mean travel time
    #calculating the mean average trip duration in minutes
    average_trip_duration = df['Trip Duration'].mean()/60
    print("The average trip duration is ", average_trip_duration, " minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #counting the number of unknown user types
    unknown_user_types = df['User Type'].isnull().sum()
    #Filling empty columns with 'Unknown'
    df['User Type'] = df['User Type'].fillna('Unknown')
    #counting the unique number of user types
    user_types = df['User Type'].nunique()
    #counting the total number of user types
    user_types_total = df['User Type'].value_counts()
    print("There are ", user_types, "different user types and a few users we cannot identify properly.")
    print(user_types_total)

    # TO DO: Display counts of gender
    #we need to check if there is a gender column in the dataframe before we perform calculations
    if "Gender" in df.columns:
        #counting the number of users with unknown gender
        unknown_gender = df['Gender'].isnull().sum()
        #filling empty gender information with the string unknown
        df['Gender'] = df['Gender'].fillna('unknown')
        #counting the unique number of genders in the dataframe
        gender_count = df['Gender'].nunique()
        print("There are ", gender_count, " different gender for your selection of city, date and day. \nBut there are also ", unknown_gender, " users who we do not know the gender for.")
    else:
        #if there is no gender column we return an information to the user
        print("There is no gender information about the bikeshare users for the city of Washington.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        #calculating the number of users we do not have birth year information
        unknown_birth_years = df['Birth Year'].isnull().sum()
        #calculating the minimum birth year entry
        earliest_year_of_birth = df['Birth Year'].min()
        #calculating the maximum birth year entry
        most_recent_year_of_birth = df['Birth Year'].max()
        #calculating the most common birth year
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("The earliest year of birth is ", earliest_year_of_birth, ".\nThe most recent year of birth is ", most_recent_year_of_birth, ". \nThe most common year of birth is: ", most_common_year_of_birth, ". \nThere are also ", unknown_birth_years, " users, who we do not know the birth year for.")
    else:
        print("There is no date of birth information for the bikeshare users in Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function to query the input to see raw data
def show_raw_data(df):
    #setting the lower index to 0
    lower_index = 0
    #setting the upper index to 5
    upper_index = 5
    #while function to ask for user input until the answer is not equal to 'yes'
    while True:
        raw_data_answer = input('Phew. That was a lot of data so far. Do you want to take a look at more raw data as well? ').lower()
        if raw_data_answer == 'yes':
            #printing the df rows from lower index to upper index
            print(df.iloc[lower_index:upper_index])
            #increasing the lower and upper index to show the next 5 rows if the user wants to see more raw data
            upper_index += 5
            lower_index += 5
        #breaking the loop if the user is answering anything else but 'yes' or 'Yes'
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
