import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
THE_CITIES = ('chicago', 'new york city', 'washington')
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
         city = input("\nPlease enter one of the following cities? \nNew York City, Chicago or Washington\n")
         if city.lower() in THE_CITIES:
            city = city.lower()
            break
         else:
            print("You have entered the wrong city.\nPlease try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nPlease enter the following words:\nall, January, February, March, April, May, June\n")
        if (month.lower() in MONTHS) or (month.lower() == 'all'):
            month = month.lower()
            break
        else:
            print("You entered it wrong.\nPlease try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease enter the following words:\nall, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n")
        if (day.lower() in DAYS) or (day.lower() == 'all'):
            day = day.lower()
            break
        else:
            print("You entered it wrong.")
            print("Please try again.")

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
    df['month'] = df['Start Time'].dt.month
    df['days'] = df['Start Time'].dt.weekday
    if month in MONTHS:
        month_number = MONTHS.index(month) + 1
        df = df[df['month'] == month_number]

    if day in DAYS:
        day_number = DAYS.index(day)
        df = df[df['days'] == day_number]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Start Time'].dt.month.mode()[0]
    popular_month = popular_month - 1
    print('Most Common Month:', MONTHS[popular_month])

    # display the most common day of week
    popular_day = df['days'].mode()[0]
    print('Most Common day:', DAYS[popular_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station:', Start_Station)

    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost commonly used end station:', End_Station)

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost commonly used combination of start station and end station trip:', Start_Station, " & ", End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    # display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('User Types:\n', user_types)
    except KeyError:
        print("\nUser Types:\nData does not exist")

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nData does not exist")

    # Display earliest year of birth
    try:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest Year:', Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nData does not exist")

    # Display most recent year of birth
    try:
        Most_Recent_Year = df['Birth Year'].max()
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nData does not exist")

    # Display most common year of birth
    try:
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
        print("\nMost Recent Year:\nData does not exist")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_five_raw_data(df):
    print(df.head(5))
    next = 0
    while True:
        view_raw_data = input('\nDo you wish to continue?\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_five_raw_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no?\n')
            if view_five_raw_data.lower() != 'yes':
                break
            display_five_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
