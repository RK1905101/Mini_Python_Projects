from typing import List, Tuple

def to_minutes(time_str: str) -> int:
    """Convert time string (HH:MM) to minutes since midnight."""
    try:
        h, m = map(int, time_str.split(":"))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("Invalid time range")
        return h * 60 + m
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid time format: {time_str}. Use HH:MM format.")

def to_time_str(minutes: int) -> str:
    """Convert minutes since midnight to time string (HH:MM)."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"

def intersect_intervals(list1: List[Tuple[int, int]], 
                       list2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Find intersection of two sorted interval lists."""
    i, j = 0, 0
    result = []
    
    while i < len(list1) and j < len(list2):
        start1, end1 = list1[i]
        start2, end2 = list2[j]
        
        start = max(start1, start2)
        end = min(end1, end2)
        
        if start < end:
            result.append((start, end))
        
        if end1 < end2:
            i += 1
        else:
            j += 1
    
    return result

def merge_overlapping_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping or adjacent intervals."""
    if not intervals:
        return []
    
    intervals = sorted(intervals)
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    return merged

def find_common_slots(schedules: List[List[Tuple[str, str]]]) -> List[Tuple[str, str]]:
    """Find common free time slots across all participants."""
    if not schedules:
        return []
    
    # Convert all schedules to minutes and merge overlapping intervals
    schedules_in_minutes = []
    for person in schedules:
        slots = [(to_minutes(s), to_minutes(e)) for s, e in person]
        slots = merge_overlapping_intervals(slots)
        schedules_in_minutes.append(slots)
    
    # Find intersection of all schedules
    common = schedules_in_minutes[0]
    for schedule in schedules_in_minutes[1:]:
        common = intersect_intervals(common, schedule)
        if not common:  # Early exit if no overlap
            break
    
    return [(to_time_str(s), to_time_str(e)) for s, e in common]

def get_valid_input(prompt: str, input_type=str, validator=None):
    """Get validated input from user."""
    while True:
        try:
            value = input(prompt).strip()
            if input_type == int:
                value = int(value)
                if validator and not validator(value):
                    print(f"Invalid input. Please try again.")
                    continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def main():
    print("=" * 40)
    print("   Virtual Study Group Scheduler")
    print("=" * 40)
    
    # Get number of participants
    n = get_valid_input(
        "\nEnter number of participants: ", 
        int, 
        lambda x: x > 0
    )
    
    schedules = []
    
    # Collect schedules from each participant
    for i in range(n):
        print(f"\n{'─' * 40}")
        print(f"Participant {i + 1}")
        print(f"{'─' * 40}")
        
        k = get_valid_input(
            "Number of free slots: ", 
            int, 
            lambda x: x >= 0
        )
        
        slots = []
        for j in range(k):
            while True:
                try:
                    start = get_valid_input(f"  Slot {j + 1} start (HH:MM): ")
                    end = get_valid_input(f"  Slot {j + 1} end (HH:MM): ")
                    
                    # Validate that end time is after start time
                    if to_minutes(end) <= to_minutes(start):
                        print("  ⚠️  End time must be after start time!")
                        continue
                    
                    slots.append((start, end))
                    break
                except ValueError as e:
                    print(f"  ⚠️  {e}")
        
        schedules.append(slots)
    
    # Find and display common slots
    print("\n" + "=" * 40)
    common = find_common_slots(schedules)
    
    if common:
        print("✅ Common free slots found:")
        print("=" * 40)
        for s, e in common:
            duration = to_minutes(e) - to_minutes(s)
            print(f"  🕒 {s} to {e} ({duration} minutes)")
    else:
        print("❌ No common time slots found.")
        print("=" * 40)
        print("\n💡 Tip: Try expanding your availability or")
        print("   checking with fewer participants.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")