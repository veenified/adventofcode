import os
import time
import timeit
from datetime import datetime, timedelta
import requests

def read_input(filename):
    with open(filename, "r") as f:
        return f.read()

def get_input(year, day):
    filename = f"{year}/day{day:02d}_input.txt"

    # Check if the input file already exists
    if not os.path.exists(filename):
        # Set the target time (Eastern Standard Time)
        est_offset = timedelta(hours=-5)
        target_time = datetime(year, 12, day, 0, 0, 0) + est_offset

        # Sleep if the puzzle isn't unlocked yet
        time_until_unlock = (target_time - datetime.utcnow()).total_seconds()
        if time_until_unlock > 0:
            print(f"Puzzle not unlocked yet! Sleeping for {time_until_unlock} seconds...")
            time.sleep(time_until_unlock + 3)  # Extra buffer to avoid firing too early

        print("Downloading input...")
        # Fetch input from Advent of Code
        session_cookie = os.getenv("AOC_USER_ID")
        if not session_cookie:
            raise ValueError("Environment variable 'AOC_USER_ID' is not set")

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {"Cookie": f"session={session_cookie}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch input: {response.status_code} {response.reason}")

        # Write the input data to a file
        with open(filename, "w") as f:
            f.write(response.text)

    # Return the input data
    return read_input(filename)

def run_parts(part1, part2, year, day):
    input = get_input(year, day)
    inputList = [line for line in input.split('\n') if line.strip()]
    start = timeit.default_timer()
    print(f"Part 1 Answer: {part1(inputList)}")
    end = timeit.default_timer()
    print(f"Part 1 Elapsed time: {end-start:,.4f} seconds\n")

    start = timeit.default_timer()
    print(f"Part 2 Answer: {part2(inputList)}")
    end = timeit.default_timer()
    print(f"Part 2 Elapsed time: {end-start:,.4f} seconds\n")
