class cfg:
    bokeh_width, bokeh_height = 1000, 800
    instance_time_start = "12:30"
    instance_time_end = "18:30"
    instance_start = "2025-03-28 00:00:00"
    prediction_strategy = "naive"  # "prophet" or "naive" or "weekly"
    inventory_strategy = "proportional" # "min_peak" or "min_total" or proportional or nochange"
