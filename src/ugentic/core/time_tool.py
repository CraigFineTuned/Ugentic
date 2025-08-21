# Time Tool for UGENTIC Agents

from datetime import datetime

class TimeTool:
    def __init__(self):
        self.name = "Time Tool"
        self.description = "Provides the current date and time information."
        print(f"{self.name} initialized.")

    def get_current_datetime(self):
        """Returns the current date and time in a human-readable format."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [TimeTool]: Retrieved current datetime: {current_time}")
        return {"status": "success", "datetime": current_time}

    def get_current_timestamp(self):
        """Returns the current Unix timestamp."""
        timestamp = datetime.now().timestamp()
        print(f"  [TimeTool]: Retrieved current timestamp: {timestamp}")
        return {"status": "success", "timestamp": timestamp}

# Example Usage (for testing)
if __name__ == "__main__":
    time_tool = TimeTool()
    
    # Get current datetime
    dt_result = time_tool.get_current_datetime()
    print(f"Datetime Result: {dt_result}")

    # Get current timestamp
    ts_result = time_tool.get_current_timestamp()
    print(f"Timestamp Result: {ts_result}")
