import pandas as pd

class Song_Mangaer:


    def __init__(self) -> None:
        self._music_data_frame = None
        pass

    
    def set_table(self, table: pd.DataFrame) -> None:
        self._music_data_frame = table
    

    def get_table(self) -> pd.DataFrame:
        return self._music_data_frame

    
    def check_for_song(self, song_name) -> int:
        return 0


    def check_for_artist(self, artist_name) -> int:
        return 0