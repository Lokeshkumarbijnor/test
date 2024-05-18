import traceback

import streamlit as st
import pandas as pd
import requests
import os
import shutil


st.set_page_config(page_title='Easter Game Downloader', layout="wide")

st.title("Easter Game Downloader")
st.subheader("2,42,809+ games and counting...")
st.markdown("---")
#df = pd.read_sql_table('maintable', 'sqlite:///DW_GAMES.db', index_col=0)

#df.insert(0, 'DOWNLOAD', True)

# Pickle file path
game_pickle_file = os.path.join(os.getcwd(), "games_data.pkl")

# Creating a Pickle File
#df.to_pickle(game_pickle_file)

# Reading from Pickle File
file_url = "https://github.com/Lokeshkumarbijnor/test/raw/main/games_data.pkl"

if not os.path.exists(game_pickle_file):
    print("Downloading file from internet...")
    res = requests.get(file_url)
    res = res.content
    with open(game_pickle_file, 'wb') as p_file:
        p_file.write(res)

df = pd.read_pickle(game_pickle_file)


#print(df.head())
category_list = df['CATEGORY'].unique().tolist()


#st_df = st.data_editor(df.head(), num_rows="dynamic")


def validate_string(input_string=None):
    output_string = input_string
    invalid_char_list = r'/\:*?"><|'
    if output_string:
        for i in invalid_char_list:
            if i in output_string:
                output_string = output_string.replace(i, '-')
    return output_string


def download_file(url=None, my_bar_status=None, f_name=None):
    if f_name:
        local_filename = f_name

    else:
        local_filename = url.split('/')[-1]
    base_file_name = local_filename.split("\\")[-1]
    try:
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers['content-length'])
            chunk_size = 8192
            #print(chunk_size)
            #print(total_size)
            size_downloaded = 0
            per_size = ((chunk_size / total_size) * 100) / (total_size / chunk_size)
            percent_complete = 0

            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if my_bar_status:
                        if percent_complete > 100:
                            percent_complete = 100
                        my_bar_status.progress(percent_complete, text=f"Downloading: {base_file_name.strip('.zip')}")
                        if not size_downloaded:
                            size_downloaded = chunk_size
                        percent_complete = int((size_downloaded / total_size) * 100)
                        size_downloaded = size_downloaded + chunk_size

                        # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    #print(chunk)
                    f.write(chunk)
    except:
        print(f"Error found in downloading: {traceback.format_exe()}")
        st.write(f"Error: {base_file_name}")
        if os.path.exists(local_filename):
            os.remove(local_filename)
    finally:
        #st.write(f"Downloaded: {base_file_name}")
        return local_filename


with st.sidebar:
    default_console = None
    category = st.multiselect("category", options=category_list, default=category_list[0])

    console_list = df.loc[df['CATEGORY'].isin(category), 'CONSOLE'].unique().tolist()
    if console_list:
        default_console = console_list[0]
    if default_console:
        console = st.multiselect("Console", options=console_list, default=console_list[0])
    else:
        console = st.multiselect("Console", options=console_list)
    game_list = df.loc[df['CONSOLE'].isin(console), 'GAMENAME'].unique().tolist()

    print("Total games:", len(game_list))
    batch_divider = 1000
    batch_dict = {}
    batch_list = []
    s_range = 0
    e_range = 0
    len_games = len(game_list)
    if len(game_list) > 1000:
        if len_games > 1000:
            counter = 1
            start_pointer = 1
            while len_games > 1000:
                sub_part = len_games - 1000
                end_pointer = 1000 * counter
                batch_dict[counter] = (start_pointer, end_pointer)
                len_games = len_games - 1000
                if len_games < 1000:
                    batch_dict[counter + 1] = (end_pointer, len_games)
                else:
                    counter = counter + 1
                start_pointer = end_pointer
                # print(sub_part)
    else:
        batch_dict[1] = (1, len_games)
    if batch_dict:
        batch_list = list(batch_dict.values())
    if batch_list:
        print(f"batch List: {batch_list}")
        try:
            batch = st.multiselect("Batch: ", options=batch_list, default=batch_list[0])
        except:
            print(f"ERROR: {traceback.format_exe()}")
    else:
        batch = st.multiselect("Batch: ", options=[0], default=0)
    print("BATCH", batch)
    if batch:
        s_range = batch[0][0]
        e_range = batch[0][-1]

        if e_range != 0:
            e_range = e_range + 1

    print("Range...")
    print(s_range, e_range)

    if s_range and e_range:
        if s_range == 1:
            s_range = 0
        game = st.multiselect("Game: ", options=game_list, default=game_list[s_range:e_range])
    else:
        game = st.multiselect("Game: ", options=[0], default=0)

    #button = st.button("Submit", on_click=print_new_df)

new_df = df.loc[df['CATEGORY'].isin(category) & df['CONSOLE'].isin(console) & df['GAMENAME'].isin(game)]
new_df = new_df.reset_index(drop=True)
updated_df = st.data_editor(new_df, key="data_editor", hide_index=True, num_rows="dynamic", column_config={
    "DOWNLOAD": st.column_config.CheckboxColumn("DOWNLOAD", help="Select all to download all the games.", default=True),

    "GAMENAME": st.column_config.TextColumn("NAME"),
    "GAMEURL": st.column_config.LinkColumn("URL"),
    "CATEGORY": None,
    "CONSOLE": None,
    "URL": None,

},

                            )
#print("************************")
#print(updated_df[updated_df.DOWNLOAD])
#print("************************")

if st.button("DOWNLOAD"):
    print("Downloading Started...")
    new_df_for_download = updated_df[updated_df.DOWNLOAD]
    if not new_df_for_download.empty:
        #print("Data Updated")
        #print(new_df_for_download)
        d_total_games = new_df_for_download.shape[0]
        #print(d_total_games)
        d_count = 0
        d_percentage = 1
        my_main_bar = st.progress(0, text=f"Downloading (1/{d_total_games})")
        for index, row in new_df_for_download.iterrows():
            if d_percentage > 100:
                d_percentage = 100
            d_count = d_count+1
            my_main_bar.progress(d_percentage, text=f"Downloading ({d_count}/{d_total_games})")
            d_percentage = int((d_count / d_total_games) * 100)
            #print(os.getcwd())
            # Creating category folder
            file_path = ''
            cwd = os.getcwd()
            category_name = validate_string(row['CATEGORY'])
            category_path = os.path.join(cwd, category_name)
            if not os.path.exists(category_path):
                os.mkdir(category_path)
            # Creating console folder
            console_name =  validate_string(row['CONSOLE'])
            console_path = os.path.join(category_path, console_name)
            if not os.path.exists(console_path):
                os.mkdir(console_path)

            # Creating file path
            game_file_name = validate_string(row['GAMENAME'])
            game_file_path = os.path.join(console_path, game_file_name)
            if not os.path.exists(game_file_path):
                #url = r"https://myrient.erista.me/files/Redump/Arcade%20-%20Konami%20-%20e-Amusement/Action%20Deka%20%28Japan%29%20%28System%20Disc%29.zip"
                url = row['GAMEURL']
                my_bar = st.progress(0, text=f"Downloading Started...")
                file_name = download_file(url, my_bar, game_file_path)
                #complete_created_path = os.path.join(os.getcwd(), file_name)
                #shutil.move(complete_created_path, game_file_path)
                my_bar.empty()

        my_main_bar.empty()


else:
    pass
