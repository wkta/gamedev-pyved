import pyved


MyEvTypes = pyved.game_events_enum((
    'PlayerDies',  # contains hp_val
    'LivesChange',  # contains num_lives
))
