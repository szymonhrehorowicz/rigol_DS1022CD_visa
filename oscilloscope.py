from pyvisa import ResourceManager
import numpy as np
import time

class Scope:
    _scope = None

    def __init__(self, resource):
        self._resource_manager = ResourceManager()
        self.resource = resource
        self.measure = self.Measure(self._scope)

    def connect(self):
        try:
            self._scope = self._resource_manager.open_resource(self.resource)
            self._scope.read_termination = '\n'
            self._scope.write_termination = '\n'
            self._scope.baud_rate = 9600
            self.IDN = self._scope.query('*IDN?')
            self.manufacturer = self.IDN.split(',')[0]
            self.model = self.IDN.split(',')[1]
            print(f'Successfully connected to the {self.manufacturer} oscilloscope - {self.model}')
        except:
            print('ERROR: When connecting to the oscilloscope')

    def start(self):
        """The :RUN command makes the oscilloscope start running"""
        try:
            self._scope.write(':RUN')
            print('RUN')
        except:
            print('ERROR: RUN')
    
    def stop(self):
        """The :STOP command makes the oscilloscope stop running"""
        try:
            self._scope.write(':STOP')
            print('STOP')
        except:
            print('ERROR: STOP')
    
    def auto_scale(self):
        """ Enable the waveform auto setting function. The oscilloscope will automatically adjust the
            vertical scale, horizontal timebase and trigger mode according to the input signal to
            realize optimum waveform display. This command is equivalent to pressing the AUTO key
            at the front panel.
        """
        try:
            self._scope.write(':AUToscale')
            print('AUToscale')
        except:
            print('ERROR: AUToscale')

    def clear(self):
        """ Clear all the waveforms on the screen. If the oscilloscope is in the RUN state, waveform
            will still be displayed. This command is equivalent to pressing the CLEAR key at the front
            panel.
        """
        try:
            self._scope.write(':AUToscale')
            print('AUToscale')
        except:
            print('ERROR: Couldn\'t AUTOSCALE the oscilloscope')

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
                    scope._scope.write(f':MEASure:SOURce {channel}')
                    self.get_channel()
                else:
                    print('ERROR: There is no {channel} channel')
                pass
            except:
                pass

        def get_channel(self):
            current_channel = None
            try:
                current_channel = scope._scope.query(':MEASure:SOURce?')
                print('Oscilloscope channel is set to %s' % current_channel)
            except:
                print('ERROR: Couldn\'t get current oscilloscope\'s channel')
            return current_channel

rm = ResourceManager()
print(rm.list_resources())
scope = Scope(resource='ASRL4::INSTR')
scope.connect()
scope.measure.get_channel()