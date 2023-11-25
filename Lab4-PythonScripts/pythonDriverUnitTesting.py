import unittest
import time
import numpy as np
import os
import matplotlib.pyplot as plt
from msox2000aSeriesScopeDriver import Scope

visa_address = 'USB0::2391::6041::MY55280378::INSTR'

class TestScopeDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up for class"""
        print("Setting up for the Scope tests")
        cls.scope = Scope(visa_address)

    # Uncomment if you want to disconnect after tests
    # @classmethod
    # def tearDownClass(cls):
    #     """Tear down for class"""
    #     print("Tearing down after the Scope tests")
    #     cls.scope.disconnect()

    # def test_set_and_get_scope_mode(self):
    #     """Test setting and getting the scope mode"""
    #     for mode in ["RUN", "STOP", "SINGLE"]:
    #         with self.subTest(mode=mode):
    #             self.scope.set_scope_mode(mode)
    #             # Allow some time for mode change if necessary
    #             time.sleep(0.2) 
    #             #retrieved_mode = self.scope.get_scope_mode()
    #             self.assertEqual(mode, mode)

    # def test_set_and_get_time_base(self):
    #     """Test setting and getting the time base"""
    #     test_time_base = 70e-6  # Example value
    #     self.scope.set_time_base(test_time_base)
    #     retrieved_time_base = float(self.scope.get_time_base())
    #     self.assertEqual(retrieved_time_base, test_time_base)

    # def test_set_and_get_time_scroll(self):
    #     """Test setting and getting the time scroll"""
    #     test_time_scroll = 15e-6  # Example value
    #     self.scope.set_time_scroll(test_time_scroll)
    #     retrieved_time_scroll = float(self.scope.get_time_scroll())
    #     self.assertEqual(retrieved_time_scroll, test_time_scroll)

    # def test_set_trigger_settings(self):
    #     """Test setting trigger settings"""
    #     test_settings = {
    #         'channel': 2,
    #         'level': 0.1,
    #         'type': "EDGE",
    #         'slope': "POS"
    #     }
    #     self.scope.set_trigger_settings(**test_settings)
    #     # Implement get_trigger_settings() in your class to retrieve and verify settings
    #     retrieved_settings = self.scope.get_trigger_settings()
    #     self.assertEqual(retrieved_settings, test_settings)

    # Add more tests for other methods as they are implemented.
    # def test_set_and_get_time_base_mode(self):
    #     """Test setting and getting the time base mode"""
    #     test_modes = ["MAIN", "XY", "WIND", "ROLL", "MAIN"]
    #     for mode in test_modes:
    #         with self.subTest(mode=mode):
    #             self.scope.set_time_base_mode(mode)
    #             # Allow some time for mode change if necessary
    #             time.sleep(2)
    #             retrieved_mode = self.scope.get_time_base_mode()
    #             self.assertEqual(retrieved_mode, mode)
    # def test_get_vertical_divisions(self):
    #     """Test getting vertical divisions"""
    #     test_channel = 1
    #     test_divisions = 0.5  # Example value
    #     # Set the divisions first
    #     self.scope.set_vertical_divisions(test_divisions, test_channel)
    #     retrieved_divisions = self.scope.get_vertical_divisions(test_channel)
    #     self.assertEqual(retrieved_divisions, test_divisions)

    # def test_set_vertical_divisions(self):
    #     """Test setting vertical divisions"""
    #     test_channel = 2
    #     test_divisions = 1.5  # Example value
    #     self.scope.set_vertical_divisions(test_divisions, test_channel)
    #     # Check if divisions were set correctly
    #     retrieved_divisions = self.scope.get_vertical_divisions(test_channel)
    #     self.assertEqual(retrieved_divisions, test_divisions)

    # # Add this test function to your TestScopeDriver class
    # def test_auto_scale(self):
    #         """Test the auto-scaling functionality."""
    #         try:
    #             self.scope.auto_scale()
    #             # Optionally, you might want to add a short delay to allow the oscilloscope
    #             # to complete the auto-scaling process, though this is not strictly necessary
    #             # for the test to be valid.
    #             # time.sleep(2)  # Wait for 2 seconds, adjust as needed

    #             # If no exceptions are raised, the test is successful
    #             self.assertTrue(True, "Auto-scaling command executed without errors.")

    #         except Exception as e:
    #             # If an exception occurs, the test should fail.
    #             self.fail(f"Auto-scaling test failed with an exception: {e}")
    # # def test_default_setup(self):
    #         """Test the default setup functionality."""
    #         try:
    #             self.scope.default_setup()
    #             # Optionally, add a delay to allow the oscilloscope time to complete the reset process
    #             # time.sleep(2)  # Adjust the delay time as necessary

    #             # If no exceptions are raised, the test is successful
    #             self.assertTrue(True, "Default setup command executed without errors.")

    #         except Exception as e:
    #             # If an exception occurs, the test should fail.
    #             self.fail(f"Default setup test failed with an exception: {e}")

    # def test_grab_and_plot_data(self):
    #         """Test the grab_data method and plot the results."""
    #         waveform_data = self.scope.grab_data(1)
            
    #         # Check that the data is returned as a numpy array
    #         self.assertIsInstance(waveform_data, np.ndarray)

    #         # Optionally, check if the array is not empty (assuming there should be data)
    #         self.assertTrue(waveform_data.size > 0)

    #         # Plotting the data for manual inspection (not typical in unit tests)
    #         plt.plot(waveform_data)
    #         plt.title("Oscilloscope Channel 1 Waveform")
    #         plt.xlabel("Sample Number")
    #         plt.ylabel("Voltage")
    #         plt.grid(True)
    #         plt.show()
    def test_set_channel_settings(self):
        """Test setting various channel settings."""
        test_settings = {
            'enabled': False,
            'probe_attenuation': '10',
            'coupling': 'DC'
            # Add more settings as needed for testing
        }

        try:
            self.scope.set_channel_settings(channel_number=1, settings=test_settings)
            # If no exceptions are raised, the test is successful
            self.assertTrue(True, "Channel settings updated without errors.")

        except Exception as e:
            # If an exception occurs, the test should fail.
            self.fail(f"Channel settings update failed with an exception: {e}")

        # Optionally, add more tests with different settings or different channels

    # ... other test methods ...

    # def test_get_channel_settings(self):
    #         """Test fetching channel settings."""
    #         try:
    #             # Fetch settings for a channel
    #             settings = self.scope.get_channel_settings(channel_number=1)

    #             # Check that a dictionary is returned
    #             self.assertIsInstance(settings, dict)

    #             # Check for expected keys in the settings dictionary
    #             expected_keys = ['enabled', 'probe_attenuation', 'coupling']  # Add more keys as needed
    #             for key in expected_keys:
    #                 self.assertIn(key, settings)

    #         except Exception as e:
    #             # If an exception occurs, the test should fail.
    #             self.fail(f"Fetching channel settings failed with an exception: {e}")
    # def test_get_screenshot(self):
    #         """Test fetching and saving a screenshot."""
    #         try:
    #             # Call the method to get and save a screenshot
    #             self.scope.get_screenshot()

    #             # The filename is based on the current time, so we just check if any new file is created
    #             # This is a very basic check and might not be reliable
    #             files_after = set(os.listdir())
    #             self.assertTrue(files_after, "Screenshot file created.")

    #         except Exception as e:
    #             # If an exception occurs, the test should fail.
    #             self.fail(f"Screenshot saving failed with an exception: {e}")
    # def test_get_function_generator_settings(self):
    #         """Test fetching function generator settings."""
    #         try:
    #             settings = self.scope.get_function_generator_settings()

    #             # Check that a dictionary is returned
    #             self.assertIsInstance(settings, dict)

    #             # Check for expected keys in the settings dictionary
    #             expected_keys = ['waveform', 'frequency', 'amplitude', 'offset', 'output_load', 'enabled']
    #             for key in expected_keys:
    #                 self.assertIn(key, settings)

    #         except Exception as e:
    #             self.fail(f"Fetching function generator settings failed with an exception: {e}")
    # def test_set_function_generator_settings(self):
    #         """Test setting function generator settings."""
    #         test_settings = {
    #             'waveform': 'SQU',
    #             'frequency': 10000,
    #             'amplitude': 2,
    #             'offset': 0,
    #             'output_load': 'HIGHZ',
    #             'output': "ON"
    #         }

    #         try:
    #             self.scope.set_function_generator_settings(test_settings)
    #             # If no exceptions are raised, the test is successful
    #             self.assertTrue(True, "Function generator settings updated without errors.")

    #         except Exception as e:
    #             self.fail(f"Setting function generator settings failed with an exception: {e}")
    def test_time_measurements(self):
        """Test time measurement methods for a specific channel."""
        test_channel = 1  # Example channel

        try:
            period = self.scope.measure_period(test_channel)
            frequency = self.scope.measure_frequency(test_channel)
            positive_width = self.scope.measure_positive_width(test_channel)
            negative_width = self.scope.measure_negative_width(test_channel)
            duty_cycle = self.scope.measure_duty_cycle(test_channel)
            rise_time = self.scope.measure_rise_time(test_channel)
            fall_time = self.scope.measure_fall_time(test_channel)

            # Check that the returned values are floats
            for measurement in [period, frequency, positive_width, negative_width, duty_cycle, rise_time, fall_time]:
                self.assertIsInstance(measurement, float)

        except Exception as e:
            self.fail(f"Time measurement methods failed with an exception: {e}")
    def test_time_measurements(self):
            """Test time measurement methods for a specific channel."""
            test_channel = 1  # Example channel

            try:
                period = self.scope.measure_period(test_channel)
                frequency = self.scope.measure_frequency(test_channel)
                positive_width = self.scope.measure_positive_width(test_channel)
                negative_width = self.scope.measure_negative_width(test_channel)
                duty_cycle = self.scope.measure_duty_cycle(test_channel)
                rise_time = self.scope.measure_rise_time(test_channel)
                fall_time = self.scope.measure_fall_time(test_channel)

                # Check that the returned values are floats
                for measurement in [period, frequency, positive_width, negative_width, duty_cycle, rise_time, fall_time]:
                    self.assertIsInstance(measurement, float)

            except Exception as e:
                self.fail(f"Time measurement methods failed with an exception: {e}")


if __name__ == '__main__':
    unittest.main()
