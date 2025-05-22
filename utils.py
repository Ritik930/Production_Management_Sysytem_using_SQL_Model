from datetime import time, datetime, timedelta


def determine_shift():
    now = datetime.now().time()
    shift_a_start = time(7 , 0)
    shift_b_start = time(19, 0)

    if shift_a_start <= now < shift_b_start:
        return "A"
    return "B"
