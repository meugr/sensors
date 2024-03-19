### requirements
BME280I2C library -- https://github.com/finitespace/BME280  
Just download latest release and install to ArduinoIDE (Sketch - Include Library - Add .ZIP Library)

### IDE settings
board: Arduino nano  
platform: AtMega328P (Old Bootloader)

### Known issues
1) Do not edit data.csv via nano. Nano make newline in the end of file and broke it. Use vi/vim instead and delete all empty str and last newline.
2) That's all))
