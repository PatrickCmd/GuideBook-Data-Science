#!/usr/bin/env python
# coding: utf-8

# # Guide Book Data Science

# ## Data Processing and Cleaning


from collections import Counter, defaultdict
from typing import List, Dict, Any
import pandas as pd

from input_data import INPUT_DATA

pd.set_option("precision", 2)


def events_per_user(event_metrics: List[Dict[str, Any]]) -> defaultdict:
    """Takes event_metrics as input data and returns a list of events
    triggered per user.
    
    Args:
        event_metrics (List[Dict[str, Any]]): Input data, a list of metrics event
        dictionaries of form:
        [
           {"event": "event name", "properties": {"user_id": 1234}},
           ...
           {"event": "another event name", "properties": {"user_id": 567}}
        ]
    Returns:
        user_events (defaultdict(list)): Defaultdict of list of events as values of
        user_id as key of form:
        {
          1234: ['event name', 'another event name'],
          567: ['event name', 'another event name'],
        }
    """

    user_events = defaultdict(list)
    for event_metric in event_metrics:
        user_events[event_metric["properties"]["user_id"]].append(event_metric["event"])

    return user_events


def user_events_trigger_count(user_events: defaultdict) -> dict:
    """Returns the count of times each user triggered each event
    Args:
        user_events (defaultdict(list)): Defaultdict of list of events as values of
        user_id as key of form:
        {
          1234: ['event name', 'another event name'],
          567: ['event name', 'another event name'],
        }
    Returns:
        user_events_triggers (dict): A dictionary of Counter objects of times each
        user triggered each event.
        {
          1234: Counter({'event name': 2, 'another event name': 1}),
          567: Counter({'event name': 10, 'another event name': 12}),
        }
    """

    user_events_triggers = {}
    for user, events in user_events.items():
        user_events_triggers[user] = Counter(events)
    return user_events_triggers


def user_event_times_count(user_events_triggers: dict) -> dict:
    """Returns a more processed dictionary object of user_events_triggers
    showing clearly what events each user triggered and the number of times
    of each event.
    
    Args:
        user_events_triggers (dict): A dictionary of Counter objects of times each
        user triggered each event.
        {
          1234: Counter({'event name': 2, 'another event name': 1}),
          567: Counter({'event name': 10, 'another event name': 12}),
        }
    Returns:
        user_event_times (dict): Dictionary showing clearly what events each user
        triggered and the number of times of each event of form:
        {
          1234: {'events':
                  {
                    {'event name': 2, 'another event name': 1}
                  }
                },
          567: {'events':
                  {
                    {'event name': 10, 'another event name': 12}
                  }
                },,
        }
    """

    user_event_times = defaultdict(dict)
    for user, events in user_events_triggers.items():
        user_event_times[user]["events"] = {}
        for ev in events:
            user_event_times[user]["events"].update({ev: events[ev]})
    return dict(user_event_times)


def generate_user_events_dataset(user_event_times: dict) -> dict:
    """Generates a dataset of dictionary of pandas series with user_ids
    acting as keys and pandas series as values. Trigger counts are used
    as data and event names are used as indices in the pandas series.
    Later the dictionary keys will form columns when generating a pandas
    dataframe.
    Args:
        user_event_times (dict): Dictionary of events each user
        triggered and the number of times of each event of form:
        {
          1234: {'events':
                  {
                    {'event name': 2, 'another event name': 1}
                  }
                },
          567: {'events':
                  {
                    {'event name': 10, 'another event name': 12}
                  }
                },,
        }
    """
    user_events_ds = {}
    for user, triggers in user_event_times.items():
        user_events_ds[user] = pd.Series(
            data=triggers["events"].values(), index=triggers["events"].keys()
        )
    return user_events_ds


def generate_dataframe(dataset: dict) -> pd.DataFrame:
    """Returns a Pandas DataFrame from dataset dictionary"""

    df = pd.DataFrame(dataset)
    return df


def transpose_clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Transponses a pandas dataframe for indices to become columns
    and viseversa and returns a cleaned dataframe.
    """

    df = dataframe.T
    df.fillna(0, inplace=True)
    df = df.astype("int64")

    return df


# Driving Code
if __name__ == "__main__":

    # Data processing
    user_events = events_per_user(INPUT_DATA)
    user_events_triggers = user_events_trigger_count(user_events)
    user_event_times = user_event_times_count(user_events_triggers)

    # generating dataset
    user_events_ds = generate_user_events_dataset(user_event_times)
    # Getting pandas dataframe from generated dataset
    df = generate_dataframe(user_events_ds)
    # Cleaning generated dataframe
    df = transpose_clean_data(df)
    print(df)
