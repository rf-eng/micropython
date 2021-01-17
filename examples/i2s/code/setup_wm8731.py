from micropython import const
from machine import Pin
from machine import I2C


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
        #data &= ~(1<<WM8731_INSEL_BIT_NUM) #0: select line in
        data |= (1<<WM8731_INSEL_BIT_NUM) #1: select mic in
        data &= ~(1<<WM8731_MUTEMIC_BIT_NUM) #0: disable micmute
        #data &= ~(1<<WM8731_MICBOOST_BIT_NUM) #0: no mic boost
        data |= (1<<WM8731_MICBOOST_BIT_NUM) #1: 20dB mic boost
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


i2c = I2C(2, freq=100000)
codec = WM8731(i2c)
