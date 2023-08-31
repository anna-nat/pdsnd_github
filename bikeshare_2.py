import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': r'C:\Users\UI941428\Desktop\Udacity\chicago.csv',
              'new york city': r'C:\Users\UI941428\Desktop\Udacity\new_york_city.csv',
              'washington': r'C:\Users\UI941428\Desktop\Udacity\washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns: city, month, day.
    """
    name = input("What is your name?\n>")
    print('Hello {}! Let\'s explore some US bikeshare data!'.format(name.title()))
    
    # get user input for city 
    cities = ('Chicago', 'new york city', 'washington')
    while True:
        city = input('Which of these cities do you want to explore : Chicago, New York City or Washington? \n> ').lower()
    
        if city not in [c.lower() for c in cities]:
            print('Something went wrong... Please, check your answer.')
    
        else:
            break
            
    
    # get user input for month 
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = input('Which of these months do you want to explore : January, February, March, April, May, June or all? \n> ').lower()
    
        if month not in [m.lower() for m in months]:
            print('Something went wrong... Please, check your answer.')
    
        else:
            break
            
    # get user input for day of week 
    days = {'all':None, 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5,'sunday':6}
    while True:
        day = input('Which of these days do you want to explore : Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? \n> ').lower()
        
        if day not in [d.lower() for d in days]:
            print('Something went wrong... Please, check your answer.')
    
        else:
            break
        
    
    print("{}, you chose data for {} for month: {} and day: {}. Let\'s start!".format(name.title(),city.title(),month.title(),day.title()))
    print('-'*40)
    return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Returns DataFrame: data loated and optionally filtred; if there no rows after filtering it returns the full dataset.
    """

    data=pd.read_csv(CITY_DATA[city])
        
    all_data=pd.DataFrame(data)
    
    # convert to datetime and filtering
    all_data['Start Time']=pd.to_datetime(all_data['Start Time'])
    days = {'all':None, 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5,'sunday':6}
    day_number=days.get(day) if day in days else None
    
    if day_number is not None:
        filter_day=all_data[all_data['Start Time'].dt.dayofweek==day_number]
    else:
        filter_day=all_data.copy()
    
    months = {'all':None, 'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
    month_number=months.get(month) if month in months else None
    
    if month_number is not None:
        df=filter_day[filter_day['Start Time'].dt.month==month_number]
    else:
        df=filter_day.copy()


    return df if df.shape[0]>0 else all_data


# retrieve filters using the get_filters() function to receive filtered_data variable
#city,month,day=get_filters()
#filtered_data=load_data(city,month,day)



def time_stats(filtered_data, city, month, day):
    """Displays statistics on the most frequent times of travel based on the filtered data."""

    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    
    start_time = time.time()
    
    # convert data to datetime and count occurrances
    filtered_data['Start Time']=pd.to_datetime(filtered_data['Start Time'])
    filtered_data['Hour']=filtered_data['Start Time'].dt.hour
    hour_counts=filtered_data['Hour'].value_counts()
    most_common_hour=hour_counts.idxmax()

    
    filtered_data['Month']=filtered_data['Start Time'].dt.month
    month_counts=filtered_data['Month'].value_counts()
    most_common_month=month_counts.idxmax()
    month_name=calendar.month_name[most_common_month]


    filtered_data['Day']=filtered_data['Start Time'].dt.dayofweek
    day_counts=filtered_data['Day'].value_counts()
    most_common_day=day_counts.idxmax()
    day_name=calendar.day_name[most_common_day]
    
    
    days = {'all':None, 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5,'sunday':6}
    day_number=days.get(day) if day in days else None
    
    months = {'all':None, 'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
    month_number=months.get(month) if month in months else None
    
    # display the most common month, the most common day of week, the most common start hour and occurrances
    if day_number is None and month_number is None:
        print("-> The most popular HOUR is {} with occurrances {}\n".format(most_common_hour,hour_counts.iloc[0]))
        print("-> The most popular DAY is {} with occurrances {}\n".format(day_name, day_counts.iloc[0]))
        print("-> The most popular MONTH is {} with occurrances {}\n".format(month_name,month_counts.iloc[0]))
    elif day_number is None and month_number is not None:
        print("-> The most popular HOUR is {} with occurrances {}\n".format(most_common_hour,hour_counts.iloc[0]))
        print("-> The most popular DAY is {} with occurrances {}\n".format(day_name, day_counts.iloc[0]))
    elif day_number is not None and month_number is None:
        print("-> The most popular HOUR is {} with occurrances {}\n".format(most_common_hour,hour_counts.iloc[0]))
        print("-> The most popular MONTH is {} with occurrances {}\n".format(month_name,month_counts.iloc[0]))
    else:
        print("-> The most popular HOUR is {} with occurrances {}\n".format(most_common_hour,hour_counts.iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#time_stats(filtered_data)

def station_stats(filtered_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()
     
    # display the most common start station and occurrances
    start_station=filtered_data['Start Station'].value_counts()
    most_common_start_station=start_station.idxmax()
    print("-> The most popular START STATION is {} with occurrances {}\n".format(most_common_start_station,start_station.iloc[0]))
    
   
    # display the most common end station and occurrances
    end_station=filtered_data['End Station'].value_counts()
    most_common_end_station=end_station.idxmax()
    print("-> The most popular END STATION is {} with occurrances {}\n".format(most_common_end_station,end_station.iloc[0]))
     

    # display the most frequent combination of start station and end station trip and occurrances; create column 'Route'
    filtered_data['Route']=filtered_data['Start Station']+' to '+ filtered_data['End Station']
    route_counts=filtered_data['Route'].value_counts()
    most_common_route=route_counts.idxmax()
    trips=route_counts.max()
    print("-> The most popular TRIP is {} with occurrances {}\n".format(most_common_route, trips))

    # remove column 'Route'
    filtered_data.drop(columns=['Route'], inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
#station_stats(filtered_data)


def trip_duration_stats(filtered_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #data total duration presented in seconds, days, hours and minutes
    total_duration_seconds = filtered_data['Trip Duration'].sum()
    total_duration_days = total_duration_seconds // 86400
    rest_seconds = total_duration_seconds % 86400
    total_duration_hours = rest_seconds // 3600
    rest_seconds %= 3600
    total_duration_minutes = rest_seconds // 60
    total_duration_seconds %= 60
    
    print("-> TOTAL DURATION is {} days {} hours {} minutes and {} seconds\n".format(int(total_duration_days), int(total_duration_hours), int(total_duration_minutes), total_duration_seconds))#f"Calkowity czas trwania: {total_duration}")
    
    
    #data average duration presented in seconds, days, hours and minutes
    mean_duration_seconds = filtered_data['Trip Duration'].mean()
    mean_duration_days = mean_duration_seconds // 86400
    mean_rest_seconds = mean_duration_seconds % 86400
    mean_duration_hours = mean_rest_seconds // 3600
    mean_rest_seconds %= 3600
    mean_duration_minutes = mean_rest_seconds // 60
    mean_duration_seconds %= 60
    
    print("-> AVERAGE DURATION is {} days {} hours {} minutes and {} seconds\n".format(int(mean_duration_days), int(mean_duration_hours), int(mean_duration_minutes), mean_duration_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
#trip_duration_stats(filtered_data)


def user_stats(filtered_data,city):
    """Displays statistics on bikeshare users based on user type, gender and birth year.
    Gender and birth year may not be present for Washington"""

    print('\nCalculating User Stats...\n\n')
    start_time = time.time()

    user_type=filtered_data['User Type'].value_counts()
    
    # display counts of user types, gender and earliest, most recent, and most common year of birth
    if city=='washington':
        print("-> USER TYPE DIVISION:\n{}".format(user_type))
    else:
        gender=filtered_data['Gender'].value_counts()
        print("-> GENDER DIVISION:\n{}\n".format(gender))
        print("-> USER TYPE DIVISION:\n{}\n".format(user_type))
        print("-> YEAR OF BIRTH STATISTIC:")
        
        if 'Birth Year' in filtered_data:
            earliest_birth_year = int(filtered_data['Birth Year'].min())
            most_recent_birth_year = int(filtered_data['Birth Year'].max())
            most_common_birth_year = int(filtered_data['Birth Year'].value_counts().idxmax())

            count_earliest = filtered_data[filtered_data['Birth Year'] == earliest_birth_year].shape[0]
            count_most_recent = filtered_data[filtered_data['Birth Year'] == most_recent_birth_year].shape[0]
            count_most_common = filtered_data['Birth Year'].value_counts().max()

            if earliest_birth_year < 1923:
                print("{} - EARLIEST year of birth with {} occurrences - Oops... Someone entered the wrong year of birth!".format(earliest_birth_year, count_earliest))
            else:
                print("{} - EARLIEST year of birth with {} occurrences.".format(earliest_birth_year, count_earliest))

            print("{} - MOST RECENT year of birth with {} occurrences.".format(most_recent_birth_year, count_most_recent))
            print("{} - MOST COMMON year of birth with {} occurrences.".format(most_common_birth_year, count_most_common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
#user_stats(filtered_data,city)




def raw_data(filtered_data):
    """Allows the user to view raw data from dataset.
    Each batch consist of 5 rows of dataset"""
    
    pd.set_option('display.max_columns',None)
    
    # remove previously created columns
    filtered_data=filtered_data.drop(['Month', 'Day','Hour'], axis=1)
    
    # display next 5 rows of data and row numbering
    answer = ('yes', 'no')
    count = 0
    iteration = 5

    while True:
        raw = input('Would you like to see more raw data? Enter yes or no.  \n> ').lower()
        if raw not in[a.lower() for a in answer]:
            print('Something went wrong... Please, check your answer.')
        else:
            if raw != 'yes':
                print("Thank you, it's over!")
                break
            else:
                start = count * iteration
                end = (count + 1) * iteration
                if start>=len(filtered_data):
                    print("No more data available!")
                    break
            
            batch_data = filtered_data.iloc[start:end].copy()
            
            batch_data.insert(0, 'Nr', range(start, start+len(batch_data)))

            print("Displaying rows {} to {}...\n".format(start, end-1))
            print(batch_data)

            count += 1


#raw_data(filtered_data)



def restart():
    """ Prompts the user to decide whether to restart the process or not."""
    
    yes_no = ('yes', 'no')
    t_f = True
    while t_f:
        restart = input('Would you like to restart? Enter yes or no.\n> ').lower()
   
        if restart not in [r.lower() for r in yes_no]:
            print('Something went wrong... Please, check your answer.')
   
        else:
            if restart.lower() == 'yes':
                t_f = False
                return True
            else:
                print("Thanks, bye!")
                t_f = False
                return False
            

#%%
def main():
    """Executes the main workflow of te bikesharing data exploration program: 
    retrieve filters, loated filtered data, display statistics, allows to view raw data"""
    t_f = True;
    while t_f:
        city, month, day = get_filters()
        filtered_data = load_data(city, month, day)
        time_stats(filtered_data, city, month, day)
        station_stats(filtered_data)
        trip_duration_stats(filtered_data)
        user_stats(filtered_data,city)
        raw_data(filtered_data)
        
        
        if not restart():
            t_f = False
            break
    input("Press Enter to exit...")


if __name__ == "__main__":
	main()
