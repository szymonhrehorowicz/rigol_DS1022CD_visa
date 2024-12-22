from pyvisa import ResourceManager
import time

class Scope:
    _scope = None

    def __init__(self, resource):
        self._resource_manager = ResourceManager()
        self.resource = resource

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
        try:
            self._scope.write(':RUN')
            print('Oscilloscope is running')
        except:
            print('ERROR: Couldn\'t START the oscilloscope')
    
    def stop(self):
        try:
            self._scope.write(':STOP')
            print('Oscilloscope is stopped')
        except:
            print('ERROR: Couldn\'t STOP the oscilloscope')
        

scope = Scope(resource='ASRL18::INSTR')
scope.connect()
scope.stop()
time.sleep(2)
scope.start()
