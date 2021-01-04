import pyb
import time
import uos
from machine import I2S
from machine import Pin
from machine import I2C
from micropython import const
import ustruct
import math

WM8731_RESET_ADR = const(0xF)
WM8731_PWR_DOWN_CTRL_ADR = const(0x6)
WM8731_DIG_INTERFACE_FMT_ADR = const(0x7)

WM8731_BCLKINV_BIT_NUM = const(7)
WM8731_MS_BIT_NUM = const(6)
WM8731_LRSWAP_BIT_NUM = const(5)
WM8731_LRP_BIT_NUM = const(4)
WM8731_IWL_MASK = const(0b000001100)
WM8731_FORMAT_MASK = const(0b000000011)

WM8731_CLKODIV2_BIT_NUM = const(7)
WM8731_CLKIDIV2_BIT_NUM = const(6)
WM8731_SR_MASK = const(0b000111100)
WM8731_SR_BIT_NUM = const(2)
WM8731_BOSR_BIT_NUM = const(1)
WM8731_USB_NORM_BIT_NUM = const(0)
WM8731_SAMPLING_CTRL_ADR = const(0x8)

WM8731_SIDEATT_MASK = const(0b011000000)
WM8731_SIDETONE_BIT_NUM = const(5)
WM8731_DACSEL_BIT_NUM = const(4)
WM8731_BYPASS_BIT_NUM = const(3)
WM8731_INSEL_BIT_NUM = const(2)
WM8731_MUTEMIC_BIT_NUM = const(1)
WM8731_MICBOOST_BIT_NUM = const(0)
WM8731_ANALOG_AUDIO_PATH_CTRL_ADR = const(0x4)

WM8731_LEFT_LINE_IN_ADR = const(0x0)
WM8731_RIGHT_LINE_IN_ADR = const(0x1)
WM8731_LRINBOTH_BIT_NUM = const(8)
WM8731_LINMUTE_BIT_NUM = const(7)
WM8731_LINVOL_BIT_NUM = const(0)
WM8731_LINVOL_MASK = const(0b000011111)
WM8731_RLINBOTH_BIT_NUM = const(8)
WM8731_RINMUTE_BIT_NUM = const(7)
WM8731_RINVOL_BIT_NUM = const(0)
WM8731_RINVOL_MASK = const(0b000011111)

WM8731_HPOR_BIT_NUM = const(4)
WM8731_DACMU_BIT_NUM = const(3)
WM8731_DEEMPH_MASK = const(0b000000110)
WM8731_ADCHPD_BIT_NUM = const(0)
WM8731_DIG_AUDIO_PATH_CTRL_ADR = const(0x5)

WM8731_ACTIVE_BIT_NUM = const(0)
WM8731_ACTIVE_CTRL_ADR = const(0x9)

class WM8731:
    def __init__(self, i2c):
        self.i2c = i2c
        self.hwaddr = 0b0011010
        #sr = 'ADC48_DAC48'
        sr = 'ADC8_DAC8'
        self.reset()
        self.disable_power_down()
        self.set_interface_format()
        self.set_sampling_rate(sr)
        self.conf_analog_path()
        self.conf_linein(0)
        self.conf_digital_path()
        self.activate()
        
    def writeReg(self, regadr, val):
        #self.i2c.writeto_mem(self.hwaddr, regadr, ustruct.pack("<b", val))
        data = bytearray(2)
        data[0] = ((regadr&0x7F)<<1) + ((val&0x0100)>>8) #left 7 bits are register adr, one data bit (MSB) right
        data[1] = val&0x00FF #8 lower data bits
        self.i2c.writeto(self.hwaddr, data)
        
    def reset(self):
        self.writeReg(WM8731_RESET_ADR, 0)
        
    def disable_power_down(self):
        self.writeReg(WM8731_PWR_DOWN_CTRL_ADR, 0)
        
    def set_interface_format(self):
        #16bit, DSP Mode: MSB on 1st BCLK, WM8731 is master
        data = 0
        data &= ~(1<<WM8731_BCLKINV_BIT_NUM) #0: clk not inverted
        
        data |= (1<<WM8731_MS_BIT_NUM) #1: WM8731 is master
        data &= ~(1<<WM8731_LRSWAP_BIT_NUM) #0: L/R not swapped
        data &= ~(1<<WM8731_LRP_BIT_NUM) #0: MSB is available on 1st BCLK rising edge after DACLRC rising edge
        
        data &= ~(WM8731_IWL_MASK) #all 0: 16 bits
        data |= (WM8731_FORMAT_MASK) #all 1: DSP Mode, frame sync + 2 data packed word
        self.writeReg(WM8731_DIG_INTERFACE_FMT_ADR, data);

    def set_sampling_rate(self, sr):
        if 'ADC48_DAC48' in sr:
            data = 0
            data &= ~(1<<WM8731_CLKODIV2_BIT_NUM) #0: clk out not divided
            data &= ~(1<<WM8731_CLKIDIV2_BIT_NUM) #0: clk in not divided
            data &= ~(WM8731_SR_MASK)
            data &= ~(1<<WM8731_BOSR_BIT_NUM)
            data |= (1<<WM8731_USB_NORM_BIT_NUM) #1: USB mode (clk is 12 MHz)
        elif 'ADC8_DAC8' in sr:
            data = 0
            data &= ~(1<<WM8731_CLKODIV2_BIT_NUM) #0: clk out not divided
            data &= ~(1<<WM8731_CLKIDIV2_BIT_NUM) #0: clk in not divided
            data |= (3<<WM8731_SR_BIT_NUM)
            data &= ~(1<<WM8731_BOSR_BIT_NUM)
            data |= (1<<WM8731_USB_NORM_BIT_NUM) #1: USB mode (clk is 12 MHz)
        self.writeReg(WM8731_SAMPLING_CTRL_ADR, data)

    def conf_analog_path(self):
        data = 0
        data &= ~(WM8731_SIDEATT_MASK) #all 0: 6dB attenuation of sidetone
        data &= ~(1<<WM8731_SIDETONE_BIT_NUM) #0: no sidetone
        data |= (1<<WM8731_DACSEL_BIT_NUM) #1: enable DAC
        data &= ~(1<<WM8731_BYPASS_BIT_NUM) #0: no bypass
        data &= ~(1<<WM8731_INSEL_BIT_NUM) #0: select line in
        data &= ~(1<<WM8731_MUTEMIC_BIT_NUM) #0: disable micmute
        data &= ~(1<<WM8731_MICBOOST_BIT_NUM) #0: no mic boost
        self.writeReg(WM8731_ANALOG_AUDIO_PATH_CTRL_ADR, data)

    def conf_linein(self, volume_dB):
        data = 0
        data &= ~(1<<WM8731_LRINBOTH_BIT_NUM) #0: decouple left and right channel
        data &= ~(1<<WM8731_LINMUTE_BIT_NUM) #0: disable mute
        data |= (0b10111<<WM8731_LINVOL_BIT_NUM)&WM8731_LINVOL_MASK #0b10111: default 0dB
        self.writeReg(WM8731_LEFT_LINE_IN_ADR, data)

        data = 0
        data &= ~(1<<WM8731_RLINBOTH_BIT_NUM) #0: decouple left and right channel
        data &= ~(1<<WM8731_RINMUTE_BIT_NUM) #0: disable mute
        data |= (0b10111<<WM8731_RINVOL_BIT_NUM)&WM8731_RINVOL_MASK #0b10111: default 0dB
        self.writeReg(WM8731_RIGHT_LINE_IN_ADR, data)

    def conf_digital_path(self):
        data = 0
        data &= ~(1<<WM8731_HPOR_BIT_NUM) #0: clear dc offset when highpass enabled
        data &= ~(1<<WM8731_DACMU_BIT_NUM) #0: disable DAC mute
        data &= ~(WM8731_DEEMPH_MASK) #00: disable de-emphasis control
        data &= ~(1<<WM8731_ADCHPD_BIT_NUM) #0: enable ADC highpass filter
        self.writeReg(WM8731_DIG_AUDIO_PATH_CTRL_ADR, data)
    
    def activate(self):
        data = 0|(1<<WM8731_ACTIVE_BIT_NUM)
        self.writeReg(WM8731_ACTIVE_CTRL_ADR, data)
        
sinTable = [0,  429,  858, 1286, 1715, 2143, 2571, 2998, 3425, 3851, 4277, 4702,
  5126, 5549, 5971, 6393, 6813, 7232, 7649, 8066, 8481, 8894, 9306, 9717,
 10126,10533,10938,11341,11743,12142,12539,12935,13328,13718,14107,14492,
 14876,15257,15635,16011,16384,16754,17121,17485,17846,18204,18559,18911,
 19260,19605,19947,20286,20621,20952,21280,21605,21925,22242,22555,22864,
 23170,23471,23768,24062,24351,24636,24916,25193,25465,25732,25996,26255,
 26509,26759,27004,27245,27481,27712,27938,28160,28377,28589,28796,28998,
 29196,29388,29575,29757,29934,30106,30273,30434,30591,30742,30888,31028,
 31163,31293,31418,31537,31650,31759,31862,31959,32051,32137,32218,32294,
 32364,32428,32487,32540,32587,32630,32666,32697,32722,32742,32756,32764,
 32767]

NSAMP_QUAD = 120

def getSinValue(Index):
    IndexPeriod = Index % (4*NSAMP_QUAD)

    if (IndexPeriod < NSAMP_QUAD):
        IndexTable = IndexPeriod
    elif (IndexPeriod < 2*NSAMP_QUAD):
        IndexTable = 2*NSAMP_QUAD - IndexPeriod
    elif (IndexPeriod < 3*NSAMP_QUAD):
        IndexTable = IndexPeriod - 2*NSAMP_QUAD
    else:
        IndexTable = 4*NSAMP_QUAD - IndexPeriod
      
    if (IndexPeriod > 2*NSAMP_QUAD):
        return -sinTable[IndexTable]
    else:
        return sinTable[IndexTable]


def i2s_callback(s):
    pass
    #print('callback worked')
    
#======= USER CONFIGURATION =======
WAV_FILE = 'pcm1608s.wav'
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 8000
#======= USER CONFIGURATION =======

sck_pin = Pin('BTN1') 
ws_pin = Pin('BTN1')  
sd_pin = Pin('BTN1')

buflen = 2048

buf_1 = bytearray(buflen)
buf_2 = bytearray(buflen)
buf_3 = bytearray(buflen)
buf_4 = bytearray(buflen)
buf_5 = bytearray(buflen)
buf_6 = bytearray(buflen)
buf_7 = bytearray(buflen)
buf_8 = bytearray(buflen) #max 32*1024
buf_9 = bytearray(buflen)
buf_10 = bytearray(buflen)

i2c = I2C(2, freq=100000)
codec = WM8731(i2c)

audio_out = I2S(
    1, # TODO add constant for this
    sck=sck_pin, ws=ws_pin, sd=sd_pin, 
    mode=I2S.TX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    buffers = [buf_1, buf_2, buf_3, buf_4, buf_5, buf_6, buf_7, buf_8, buf_9, buf_10],
    #buffers = [buf_1],
    callback=i2s_callback)

testMode = False
isStarted = False
idx = 0
bufcnt = 0
samplecnt = 0

if not(testMode):
    wav = open(WAV_FILE,'rb')
    wav.seek(44) # advance to first byte of Data section in WAV file
    isStarted = False
    while True:
        try:
            buffer = audio_out.getbuffer()
            if buffer != None:
                num_read = wav.readinto(buffer)
                num_written = audio_out.putbuffer(buffer)
                if isStarted == False:
                    audio_out.start()
                    isStarted = True
                # end of WAV file?
                if num_read == 0:
                    # advance to first byte of Data section
                    pos = wav.seek(44) 
                    
        except (KeyboardInterrupt, Exception) as e:
            print('caught exception {} {}'.format(type(e).__name__, e))
            break

else:
    while True:
        try:
            buffer = audio_out.getbuffer()
            if buffer != None:
                #print(type(buffer))
                #num_read = wav.readinto(buffer)
                bufcnt += 1
                bufcnt %= 8
                #print(samplecnt)
                #print(idx)
                samplecnt = 0
                if True:
                    for cnt in range(0,len(buffer),4):                               
                        if testMode:
                            if samplecnt == 0:
                                sample = 2**15-1 #-0*int((bufcnt+1)*0.1*2**15)                    
        #                     elif samplecnt in range(30, 30+20, 1):
        #                         sample = int((idx%200)/200*2**14)
        #                     elif samplecnt == (buflen//4)-1: #2 bytes, 2 channels (left/right)
        #                         sample = int((idx%200)/200*2**14) #2**15
                            else:
                                sample = 0*idx #*int(((idx%512)/512)*2**14)
                        else:
                            #sample = int((bufcnt+1)*0.1*getSinValue(8*idx))
                            if samplecnt == 0:
                                sample = 2**15-1 #-0*int((bufcnt+1)*0.1*2**15)
                            else:
                                sample = int((2**15-1)*(0.5*math.sin(2*math.pi*(idx)*(1/32+7e-5)))) 
                                #sample = int(0.5*getSinValue(3*idx))
                        
                        #sample = int(10*(idx%4096))
                        #myint = ustruct.pack( "<i", sample )
                        buffer[cnt] = sample & 0xFF # myint[0] #sample & 0xFF
                        buffer[cnt+1] = sample>>8 # myint[1] #sample>>8
                        #buffer[cnt+2] = 0 #1*(2**15) & 0xFF #sample & 0xFF
                        #buffer[cnt+3] = 0 #1*(2**15) >>8 #sample>>8
                        samplecnt += 1
                        idx += 1

                audio_out.putbuffer(buffer)            
                #print(num_written)
                if isStarted == False:
                    audio_out.start()
                    isStarted = True
            else:
                pass
                        
        except (KeyboardInterrupt, Exception) as e:
            print('caught exception {} {}'.format(type(e).__name__, e))
            audio_out.deinit()
            break
