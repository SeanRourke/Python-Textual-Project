from statistics import mean


FOLDER = "swimdata/"


def convert2hundreths(timestring):
    """Given a string which represents a time, this function converts the string
    to a number (int) representing the string's hundreths of seconds value, which is
    returned.
    """

    if ":" in timestring:
        mins, rest = timestring.split(":")
        secs, hundreths = rest.split(".")
    else:
        mins = 0
        secs, hundreths = timestring.split(".")
    
    return int(hundreths) + (int(secs) * 100) + ((int(mins) * 60) * 100)


def build_time_string(num_time):
    """  """
    secs, hundreths = f"{(num_time / 100):.2f}".split(".")  # rounding inside the f string
    mins = int(secs) // 60
    seconds = int(secs) - mins*60
    return f"{mins}:{seconds}.{hundreths}"


def get_swimmers_data(filename):
    """ """
    name, age, distance, stroke = filename.removesuffix(".txt").split("-")
    with open(FOLDER + filename) as fh:
        data = fh.read()
    times = data.strip().split(",")
    values = []   # empty list
    for t in times:
        values.append(convert2hundreths(t))
    average = build_time_string(mean(values))

    return name, age, distance, stroke, times, values, average


def convert2range(v, f_min, f_max, t_min, t_max):
    """Given a value (v) in the range f_min-f_max, convert the value
    to its equivalent value in the range t_min-t_max.

    Based on the technique described here:
        http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
    """
    return round(t_min + (t_max - t_min) * ((v - f_min) / (f_max - f_min)), 2)

