import time
import gpiod

# Relay pin configuration (GPIO23)
RELAY_PIN = 23

# Initialize variables
chip = None
line = None

try:
    # Access the GPIO chip
    chip = gpiod.Chip('gpiochip4')  # Usually gpiochip4 on Raspberry Pi 5
    print("GPIO chip opened successfully")
    
    # Request GPIO line for control
    line = chip.get_line(RELAY_PIN)
    print(f"GPIO line {RELAY_PIN} acquired")
    
    # Configure line as output
    line.request(consumer="relay_control", type=gpiod.LINE_REQ_DIR_OUT)
    print("Line configured as output")
    
    # TURN ON relay (set LOW level - 0V)
    line.set_value(0)
    print("Device turned ON for 10 seconds")
    
    # Wait for 10 seconds
    time.sleep(10)
    
    # TURN OFF relay (set HIGH level - 3.3V)
    line.set_value(1)
    print("Device turned OFF")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Always release resources
    print("Starting cleanup procedure...")
    
    # Ensure relay is turned OFF (set HIGH level)
    if line:
        try:
            line.set_value(1)
            print("Relay guaranteed to be OFF")
        except Exception as e:
            print(f"Error turning off relay: {str(e)}")
    
    # Release line
    if line:
        try:
            line.release()
            print("GPIO line released")
        except Exception as e:
            print(f"Error releasing line: {str(e)}")
    
    # Close chip
    if chip:
        try:
            chip.close()
            print("GPIO chip closed")
        except Exception as e:
            print(f"Error closing chip: {str(e)}")
    
    print("Cleanup procedure completed")