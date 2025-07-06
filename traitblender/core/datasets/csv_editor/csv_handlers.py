import pandas as pd
from io import StringIO

def get_table(csv_data: str) -> pd.DataFrame:
    """
    Get a pandas dataframe from a csv string
    Args:
        csv_data: str
    Returns:
        pd.DataFrame
    Example:
        >>> get_table("name,age,score\nJohn,25,88.5\nJane,30,92.0\nBob,35,77")
        >>> name  age  score
        >>> 0   John   25   88.5
        >>> 1   Jane   30   92.0
        >>> 2    Bob   35   77.0
    """
    df = pd.read_csv(StringIO(csv_data))
    return df

def to_csv(df: pd.DataFrame) -> str:       
    """
    Convert a pandas dataframe to a csv string
    Args:
        df: pd.DataFrame
    Returns:
        str
    """ 
    return df.to_csv()