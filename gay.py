import time
import gpiod

def test_all_pins():
    """Tests all GPIO pins on the Raspberry Pi 5"""
    # Correct chip name for Raspberry Pi 5
    chip_name = 'gpiochip4'
    chip = None
    
    try:
        # Get access to the GPIO chip
        chip = gpiod.Chip(chip_name)
        print(f"Using chip: {chip_name}")
        
        # Get the number of available pins
        num_pins = chip.num_lines()
        print(f"Number of available pins: {num_pins}")
        
        # Store all lines we're using for proper cleanup
        active_lines = []
        
        # Test all available pins
        for pin in range(num_pins):
            line = None
            try:
                print(f"\nTesting pin {pin}...")
                
                # Request the GPIO line for control
                line = chip.get_line(pin)
                
                # Configure the line as output
                line.request(consumer=f"pin_test_{pin}", type=gpiod.LINE_REQ_DIR_OUT)
                active_lines.append(line)
                
                # Turn on the device (set high level)
                line.set_value(1)
                print(f"Pin {pin} - Device turned ON")
                
                # Wait for 10 seconds
                print("Waiting for 10 seconds...")
                time.sleep(10)
                
                # Turn off the device (set low level)
                line.set_value(0)
                print(f"Pin {pin} - Device turned OFF")
                
                # Release the line
                line.release()
                active_lines.remove(line)
                
                print(f"Pin {pin} test completed successfully")
                
            except Exception as e:
                print(f"Error testing pin {pin}: {str(e)}")
                # Try to release the line if there was an error
                if line:
                    try:
                        line.set_value(0)  # Ensure device is turned off
                        line.release()
                        if line in active_lines:
                            active_lines.remove(line)
                    except:
                        pass
        
        print("\nAll pins testing completed")
        
    except Exception as e:
        print(f"Error accessing chip {chip_name}: {str(e)}")
    
    finally:
        # Always ensure all devices are turned off and resources are released
        print("\nEnsuring all devices are turned off...")
        
        # Turn off all active lines
        for line in active_lines:
            try:
                line.set_value(0)  # Ensure device is turned off
            except:
                pass
        
        # Release all active lines
        for line in active_lines:
            try:
                line.release()
            except:
                pass
        
        # Close the chip
        if chip:
            try:
                chip.close()
            except:
                pass

if __name__ == "__main__":
    print("=== Testing All GPIO Pins on Raspberry Pi 5 ===")
    print("This will test each pin sequentially for 10 seconds each")
    print("Press Ctrl+C to stop the testing\n")
    
    test_all_pins()
    
    print("\n=== Testing completed ===")