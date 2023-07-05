'''
Band Edge Thermometry Reader

Paromita Mitchell 07/05/2023

This program takes in data from two cameras to determine transition points of opacity.
This will allow us to determine set points of temperature behavior.
It also serves as a demonstration of temperature dependence of the Band Edge.

There are a few stages to this:
1. Read from two cameras (temperature reading from hotplate, and wafer)
    a) Average the wafers frames.
    b) Save both the temperature and the wafer measurement with filename time.
2. Live feed.
3. Read temperature from picture, or from external temperature sensor.
4. Threshold check for brightness (compare brightness of two points)
5. Edge detect to determine wafer image visibility as a comparison

'''

'''
STAGE 1:
Read from two 


'''