#include "py/mphal.h"

void ELITEBOARD_H743XI_board_early_init(void) {
    // Turn off the USB switch
    #define USB_PowerSwitchOn pin_G6
    mp_hal_pin_output(USB_PowerSwitchOn);
    mp_hal_pin_low(USB_PowerSwitchOn);
}
