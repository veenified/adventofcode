from utils.utils import get_input, run_parts

# Part 1:
# iven the test_input, we need to calculate the distance traveled by each reindeer after 1000 seconds and return the winning reindeers distance (max distance).
# Comet should travel 1120 km, and Dancer should travel 1056 km.
# So the answer is 1120 for test_input.
# Part 2:
# Given the test_input, we need to calculate the point accumlated by each reindeer after 1000 seconds and return the winning reindeers points (max points).
# Comet should accumulate 312 points, and Dancer should accumulate 689 points.
# So the answer is 689 for test_input.
test_input = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

def calculate_distance_at_time(speed: int, duration: int, rest: int, total_time: int) -> int:
    """Calculate the distance a reindeer travels after total_time seconds."""
    cycle_time = duration + rest
    
    # Calculate full cycles and remaining time
    full_cycles = total_time // cycle_time
    remaining_time = total_time % cycle_time
    
    # Distance from full cycles
    distance = full_cycles * speed * duration
    
    # Distance from remaining time (only if still flying)
    if remaining_time > 0:
        flying_time = min(remaining_time, duration)
        distance += flying_time * speed
    
    return distance

def part1(input_lines: list[str]):
    # Determine total time (1000 for test input, 2503 for actual input)
    reindeers = [line for line in input_lines if line.strip()]
    total_time = 1000 if len(reindeers) == 2 else 2503
    
    max_distance = 0
    for line in input_lines:
        if not line.strip():  # Skip empty lines
            continue
        speed, duration, rest = int(line.split()[3]), int(line.split()[6]), int(line.split()[13])
        distance = calculate_distance_at_time(speed, duration, rest, total_time)
        
        if distance > max_distance:
            max_distance = distance
    return max_distance

def part2(input_lines: list[str]):
    # Parse all reindeer data
    reindeers = []
    for line in input_lines:
        if not line.strip():  # Skip empty lines
            continue
        speed, duration, rest = int(line.split()[3]), int(line.split()[6]), int(line.split()[13])
        reindeers.append({"speed": speed, "duration": duration, "rest": rest, "points": 0})
    
    # Determine total time (1000 for test input, 2503 for actual input)
    total_time = 1000 if len(reindeers) == 2 else 2503
    
    # For each second, calculate distances and award points
    for second in range(1, total_time + 1):
        distances = []
        for reindeer in reindeers:
            distance = calculate_distance_at_time(
                reindeer["speed"], 
                reindeer["duration"], 
                reindeer["rest"], 
                second
            )
            distances.append(distance)
        
        # Find maximum distance
        max_distance = max(distances)
        
        # Award points to all reindeer at the maximum distance
        for i, distance in enumerate(distances):
            if distance == max_distance:
                reindeers[i]["points"] += 1
    
    # Return maximum points
    return max(reindeer["points"] for reindeer in reindeers)

if __name__ == "__main__":
    # print(part1(test_input.split("\n")))
    # print(part2(test_input.split("\n")))
    run_parts(part1, part2, 2015, 14)