import time
import pandas as pd
import numpy as np
import calendar


CITY_DATA = {'chicago': 'csv-files/chicago.csv',
             'new york city': 'csv-files/new_york_city.csv',
             'washington': 'csv-files/washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']


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
    city = input("Please enter the name of the city\t").lower()
    while city not in CITY_DATA:
        city = input("Wrong input!\n Please enter a valid city name(E.g. {})\t".format(
            list(CITY_DATA.keys()))).lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month do you want to filter by?\t").lower()
    while month not in months:
        month = input(
            "Wrong input!\n Please enter a valid month name(E.g. {}\t)".format(months)).lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day do you want to filter by?\t").lower()
    while day not in days:
        day = input(
            "Wrong input!\n Please enter a valid month name(E.g. {})\t".format(days)).lower()
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
    # TO DO: load city data
    df = pd.read_csv(CITY_DATA[city])

    # To Do: convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # To Do: create month and dayofweek columns
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # TO DO: if month is given filter by month
    if month != 'all':
        #         month = months.index(month) + 1

        df = df.loc[df['month'].astype(str) == month.title()]

    # To Do: check if day filter is available
    if day != 'all':

        df = df.loc[df['day_of_week'].astype(str) == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    name = df['month'].value_counts()[0:1].index[0]
    count = df['month'].value_counts()[0]
    print("The most common month is {} and its count is {}\n".format(name, count))

    # TO DO: display the most common day of week
    name = df['day_of_week'].value_counts()[0:1].index[0]
    count = df['day_of_week'].value_counts()[0]
    print("The most common day of week is {} and its count is {}\n".format(name, count))

    # TO DO: display the most common start hour
    name = df['Start Time'].dt.hour.value_counts()[0:1].index[0]
    count = df['Start Time'].dt.hour.value_counts()[0]
    print("The most common start hour is {} and its count is {}\n".format(name, count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    name = df['Start Station'].value_counts()[0:1].index[0]
    count = df['Start Station'].value_counts()[0]
    print("The most commonly used start station is {} and its count is {}\n".format(
        name, count))

    # TO DO: display most commonly used end station
    name = df['End Station'].value_counts()[0:1].index[0]
    count = df['End Station'].value_counts()[0]
    print("The most commonly used end station is {} and its count is {}\n".format(
        name, count))

    # TO DO: display most frequent combination of start station and end station trip
    start_and_end_name = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is:\n",
          start_and_end_name)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # divmod returns both the quotient and remainder. Divides the first value by the second
    m, s = divmod(df['Trip Duration'].sum(), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("Total travel was {} day(s), {} hour(s), {} minute(s), and {} second(s) \n".format(d, h, m, s))

    # TO DO: display mean travel time
    print("The mean travel time is: ", df['Trip Duration'].mean(), " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Type count:\n", df['User Type'].value_counts(), "\n")

    # TO DO: Display counts of gender
    try:
        print("Gender Count:\n", df['Gender'].value_counts())
    except:
        print("Gender was not captured in {} data set\n".format(city))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min().astype(int)
        recent_birth_year = df['Birth Year'].max().astype(int)
        common_birth_year = df['Birth Year'].value_counts(
        ).index[0].astype(int)
        common_birth_year_count = df.groupby(
            ['Birth Year']).size().sort_values(ascending=False).values[0]
        print("The earliest birth year is {}, most recent birth year is {}, and the most common birth year is {} with a count of {}".format(
            earliest_birth_year, recent_birth_year, common_birth_year, common_birth_year_count))

    except:
        print("Birth year was not captured in {} data set\n".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_five_rows(df):
    """
    This function will display the raw data, five (5) rows at a time.

    Arg(s): 
        df :- this is pandas dataframe 
    Variables:
        user_input :- accepts either 'yes' or 'no'
    """
    start = 0
    user_input = input(
        "Do you want to see five (5) rows of raw data? Enter yes or no\t").lower()
    while True:
        if user_input == "yes":
            print(df.iloc[start: start+5])
            start += 5
            user_input = input("\nDo you want to see more?\t")
            if user_input == "no":
                break

        elif user_input == "no":
            print("\nThank you for using my app")
            break
        else:
            user_input = input(
                "\nWrong input!\n Please enter a valid input\t").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_five_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
