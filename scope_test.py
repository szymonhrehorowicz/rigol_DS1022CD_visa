from pyvisa import ResourceManager
import numpy as np
import matplotlib.pyplot as plt

class Scope:
    _scope = None

    def __init__(self, resource):
        self._resource_manager = ResourceManager()
        self.resource = resource
        self.measure = self.Measure(self._scope)
        self.data_manager = self.DataManager()

    def connect(self):
        try:
            self._scope = self._resource_manager.open_resource(self.resource)
            self._scope.read_termination = '\n'
            self._scope.write_termination = '\n'
            self._scope.baud_rate = 9600
            self._scope.timeout = 5000  # Set a high timeout value
            self.IDN = self._scope.query('*IDN?')
            self.manufacturer = self.IDN.split(',')[0]
            self.model = self.IDN.split(',')[1]
            print(f'Successfully connected to the {self.manufacturer} oscilloscope - {self.model}')
        except Exception as e:
            print(f'ERROR: When connecting to the oscilloscope: {e}')

    def start(self):
        """The :RUN command makes the oscilloscope start running"""
        try:
            self._scope.write(':RUN')
            print('RUN')
        except Exception as e:
            print(f'ERROR: RUN: {e}')
    
    def stop(self):
        """The :STOP command makes the oscilloscope stop running"""
        try:
            self._scope.write(':STOP')
            print('STOP')
        except Exception as e:
            print(f'ERROR: STOP: {e}')

    def write(self, cmd):
        self._scope.write(cmd)

    def query(self, cmd):
        return self._scope.query(cmd)
    
    def auto_scale(self):
        """Enable the waveform auto setting function."""
        try:
            self._scope.write(':AUToscale')
            print('AUToscale')
        except Exception as e:
            print(f'ERROR: AUToscale: {e}')

    def clear(self):
        """Clear all the waveforms on the screen."""
        try:
            self._scope.write(':CLEar')
            print('Clear')
        except Exception as e:
            print(f'ERROR: Couldn\'t clear the oscilloscope: {e}')

    def acquire_data(self, channel='CHAN1'):
        try:
            self.stop()

            self._scope.write(f':{channel}:DISP ON')  # Ensure the channel is on
            self.write(':WAVeform:DATA? CHANnel1')
            y = scope._scope.read_bytes(1028)
            y = np.frombuffer(y[4:], dtype=np.uint8)
            y_scale = float(self.query(f':{channel}:SCALe?'))
            y_offset = float(self.query(f':{channel}:OFFSet?'))
            x_scale = float(self.query(':TIMebase:SCALe?'))
            x_offset = float(self.query(':TIMebase:OFFSet?'))

            y = (y - y_offset) * 8 * y_scale / 256
            x = np.linspace(0, x_scale * 12, len(y))

            data = self.Data(channel, y.tolist(), y_scale, y_offset, x.tolist(), x_scale, x_offset)
            self.data_manager.add_data(data)

            self.start()
        except Exception as e:
            print(f'ERROR: Couldn\'t acquire data: {e}')

    class Data:
        def __init__(self, channel, y, y_scale, y_offset, x, x_scale, x_offset):
            self.channel = channel
            self.y = y,
            self.y = self.y[0]
            self.y_scale = y_scale
            self.y_offset = y_offset
            self.x = x,
            self.x = self.x[0]
            self.x_scale = x_scale
            self.x_offset = x_offset

        def plot(self):
            plt.plot(self.x, self.y)
            plt.xlabel('Time (s)')
            plt.ylabel('Voltage (V)')
            plt.title(f'Oscilloscope {self.channel} Data')
            plt.show()

    class DataManager:
        def __init__(self):
            self.data_arr = []

        def add_data(self, data):
            self.data_arr.append(data)

        def plot_latest(self):
            self.data_arr[-1].plot()
        
        def plot_all(self):
            for data in self.data_arr:
                data.plot()

    class Measure:
        def __init__(self, scope) -> None:
            self.scope = scope
            self.available_channels = [
                'D0', 'D1', 'D2', 'D3',
                'D4', 'D5', 'D6', 'D7',
                'D8', 'D9', 'D10', 'D11',
                'D12', 'D13', 'D14', 'D15',
                'CHAN1', 'CHAN2', 'MATH']

        def set_channel(self, channel):
            try:
                if channel in self.available_channels:
                    self.scope.write(f':MEASure:SOURce {channel}')
                    self.get_channel()
                else:
                    print(f'ERROR: There is no {channel} channel')
            except Exception as e:
                print(f'ERROR: Couldn\'t set the channel: {e}')

        def get_channel(self):
            current_channel = None
            try:
                current_channel = self.scope.query(':MEASure:SOURce?')
                print('Oscilloscope channel is set to %s' % current_channel)
            except Exception as e:
                print(f'ERROR: Couldn\'t get current oscilloscope\'s channel: {e}')
            return current_channel

scope = Scope(resource='ASRL4::INSTR')
scope.connect()