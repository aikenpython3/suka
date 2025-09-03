import time
import gpiod

def test_all_pins():
    """Tests all GPIO pins on the Raspberry Pi 5"""
    # Typically gpiochip4 on Raspberry Pi 5
    chip_name = 'gpiochip4'
    
    try:
        # Get access to the GPIO chip
        chip = gpiod.Chip(chip_name)
        print(f"Using chip: {chip_name}")
        print(f"Number of available pins: {chip.num_lines}")
        
        # Test all available pins
        for pin in range(chip.num_lines):
            try:
                print(f"\nTesting pin {pin}...")
                
                # Request the GPIO line for control
                line = chip.get_line(pin)
                
                # Configure the line as output
                line.request(consumer=f"pin_test_{pin}", type=gpiod.LINE_REQ_DIR_OUT)
                
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
                
                print(f"Pin {pin} test completed successfully")
                
            except Exception as e:
                print(f"Error testing pin {pin}: {str(e)}")
                # Try to release the line if there was an error
                try:
                    line.release()
                except:
                    pass
        
        print("\nAll pins testing completed")
        
    except Exception as e:
        print(f"Error accessing chip {chip_name}: {str(e)}")
    
    finally:
        # Always release resources
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