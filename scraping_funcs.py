def date_time(date):
    ''' Make Date data into datetimeformat'''
    date_dt = datetime.strptime(date, '%d %b %Y')
    return date_dt


def strip_spaces(string):
    ''' Strips all spaces within a string'''
    strip = string.replace(" ", "")
    return strip


def remove_v(string):
    ''' STATISTICS:

    Removes "v" from Opposition column in Dataframe.

    Arg: string of 'v Opposition Name'
    Returns: Opposition Name
    '''

    split = string.split()
    del split[0]
    split = ''.join(split)
    return split


def get_stats(page_nums):
    ''' Uses pandas to read tables from a URL with multiple pages. Cleans each table to return data needed.

    Args: list of page numbers
    Returns: 1 dataframe of each table obtained from each URL with appropriate data needed.

    '''
    url= "http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;filter=advanced;home_or_away=1;home_or_away=2;home_or_away=3;orderby=date;page={};result=1;result=2;result=3;spanmax1=jan+2019;spanmax2=1+jan+2019;spanmin1=jan+2000;spanmin2=1+jan+2000;spanval1=span;spanval2=span;team=1;template=results;type=team;view=match"
    dfs = []

    for page in page_nums:
        num_page = url.format(page)
        table = pd.read_html(num_page)
        correct_table = table[3]
        correct_table = clean_stats(correct_table)
        dfs.append(correct_table)

    return pd.concat(dfs).reset_index()


def home_away(ground="Twickenham"):
    '''STATISTICS:

    Determines whether a match was played at home or away.
    Twickenham is the Home Ground for England.

    Arg: Ground at which match was played
    Returns: Whether ground is Home or Away
    '''
    home_ground = "Twickenham"

    if ground == home_ground:
        return "Home"
    else:
        return "Away"


def find_year(string):
    ''' STATISTICS:

    Isolate Year from Date string.

    Arg: Full Written Date
    Returns: Year
    '''

    split = string.split()
    return split[-1]


def clean_stats(correct_table):
    ''' STATISTICS:

    Clean each dataframe obtained from ESPN StatsGuru Page.
    - Cleans Oppositions format
    - Determines if Game is Home or Away
    - Removes unnecessary columns
    - Creates Year of Game Column

    Arg: correct table from ESPEN StatsGuru
    '''

    correct_table["Countries"] = correct_table["Opposition"].apply(remove_v)
    correct_table["Countries"] = correct_table["Countries"].apply(strip_spaces)
    correct_table["Where"] = correct_table["Ground"].apply(home_away)
    correct_table.drop(['Team', 'Result', 'Diff', 'Pens', 'Drop', 'Unnamed: 9', 'Unnamed: 13', 'Opposition', 'Ground'], axis=1, inplace=True)
    correct_table["Year"] = correct_table["Match Date"].apply(find_year)
    correct_table['Match Date'] = correct_table['Match Date'].apply(date_time)
    correct_table.columns = correct_table.columns.str.replace(' ', '')

    return(correct_table)


def strip_letters(string):
    '''WORLD RANKINGS
    Strips the country codes from "Teams" column in dataframe and then strips spaces from double worded countries

    Arg: String in "Team" column
    Example Input: "New Zealand NZL"
    Example Output: "NewZealand"

    '''
    split = string.split()
    split.pop()
    split = ' '.join(split)
    split = strip_spaces(split)
    return split


def clean_dataframe(dataframe):
    '''WORLD RANKINGS:

    Cleans each dataframe that is obtained from World Rankings Page.
    - Removes unnecessary columns
    - Gives columns appropriate headers
    - Adds column for relevant year of Ranking
    - Cleans column of Team Name

    Arg: dataframe for my_years

    '''
    dataframe = dataframe.drop([1,3,4,5], axis=1)
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe[1:]
    dataframe["Year"] = int(year)
    dataframe["Countries"] = dataframe["Teams"].apply(strip_letters)
    dataframe = dataframe.drop(["Teams"], axis = 1)

    return pd.DataFrame(dataframe)


def header_list(table):
    '''COACHES:
    Creates list of headers from html table.

    Arg: Table in html script

    '''
    header = table.find_all('th')
    header_vars = [i.text for i in header]
    header_list = [str.strip(i) for i in header_vars]

    return list(header_list)


def clean_list(list_item):
    '''COACHES:
    Cleans list item obtained from Wikipedia table and returns a clean list of Coaches data

    Arg: List of items in table
    '''

    clean_list = []

    for i in list_item:
        i = str.strip(i) # Remove all white spaces

        if "000000" in i: # Remove all numbers up until the '♠'
            sp_index = i.find('♠')
            remove_zeros = i.replace(i[:sp_index+1], '')
            clean_list.append(remove_zeros)
        elif "[" in i: # Remove references
            pattern = re.compile("^.*\[.*\]$")
            clean_string = re.sub(r'\[.*\]', r'', i)
            clean_list.append(clean_string)
        else:
            clean_list.append(i)

    return clean_list


def date_split_start(date):
    ''' COACHES:
    Splits a date range to return the first date in datetime format'''

    if date == '20 November 2015 – present':
        date = date.replace('20 November 2015 – present', '20 November 2015 – 2 February 2019')
    else:
        date = date

    split = date.split()
    first = ' '.join(split[:3])
    first = datetime.strptime(first, '%d %B %Y')
    return first


def date_split_end(date):
    ''' COACHES:
    Splits a date range to return the second date in datetime format'''

    if date == '20 November 2015 – present':
        date = date.replace('20 November 2015 – present', '20 November 2015 – 2 February 2019')
    else:
        date = date

    split = date.split()
    end = ' '.join(split[-3:])
    end = datetime.strptime(end, '%d %B %Y')
    return end


def clean_coaches(dataframe):
    '''COACHES:
    Cleans coaches dataframe to return needed columns and coaches for
    date range 2000-2019

    Arg: Dataframe
    '''
    dataframe.drop(["Tests", "Won", "Drew", "Lost"], axis=1, inplace=True)
    dataframe.drop(list(range(0,9)), axis='rows', inplace=True)
    dataframe.reset_index(drop=True)

    dataframe["start"] = dataframe["Tenure"].apply(date_split_start)
    dataframe["end"] = dataframe["Tenure"].apply(date_split_end)

    dataframe.drop(["Tenure"], axis=1, inplace=True)
    dataframe.columns = dataframe.columns.str.replace(' ', '')

    return dataframe


def change_year(date):
    ''' Changes date to 2004 if year is prior to 2004
    Args: date(Year)
    '''

    if int(date) < 2004:
        return 2004
    else:
        return date
