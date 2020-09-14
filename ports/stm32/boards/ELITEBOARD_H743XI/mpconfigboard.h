#define MICROPY_HW_BOARD_NAME       "ELITEBOARD_H743XI"
#define MICROPY_HW_MCU_NAME         "STM32H743"

#define MICROPY_HW_ENABLE_RTC       (1)
#define MICROPY_HW_ENABLE_RNG       (1)
#define MICROPY_HW_ENABLE_ADC       (1)
#define MICROPY_HW_ENABLE_DAC       (1)
#define MICROPY_HW_ENABLE_USB       (1)
#define MICROPY_HW_ENABLE_SDCARD    (1)
#define MICROPY_HW_HAS_SWITCH       (0)
#define MICROPY_HW_HAS_FLASH        (1)

#define MICROPY_BOARD_EARLY_INIT    ELITEBOARD_H743XI_board_early_init
void ELITEBOARD_H743XI_board_early_init(void);

// The board has an 16MHz HSE, the following gives 400MHz CPU speed
#define MICROPY_HW_CLK_PLLM (1)
#define MICROPY_HW_CLK_PLLN (50)  //60 would be 480MHz
#define MICROPY_HW_CLK_PLLP (2)
#define MICROPY_HW_CLK_PLLQ (2)
#define MICROPY_HW_CLK_PLLR (2)

// The USB clock is set using PLL3
#define MICROPY_HW_CLK_PLL3M (32)
#define MICROPY_HW_CLK_PLL3N (96)
#define MICROPY_HW_CLK_PLL3P (2)
#define MICROPY_HW_CLK_PLL3Q (1)
#define MICROPY_HW_CLK_PLL3R (2)

// 4 wait states
#define MICROPY_HW_FLASH_LATENCY    FLASH_LATENCY_4

// UART config
#define MICROPY_HW_UART2_TX         (pin_D5)
#define MICROPY_HW_UART2_RX         (pin_D6)
#define MICROPY_HW_UART4_TX         (pin_B9)
#define MICROPY_HW_UART4_RX         (pin_H14)
#define MICROPY_HW_UART6_TX         (pin_C6)
#define MICROPY_HW_UART6_RX         (pin_C7)
#define MICROPY_HW_UART7_TX         (pin_F7)
#define MICROPY_HW_UART7_RX         (pin_F6)
#define MICROPY_HW_UART8_TX         (pin_J8)
#define MICROPY_HW_UART8_RX         (pin_E0)

//#define MICROPY_HW_UART_REPL        PYB_UART_4
//#define MICROPY_HW_UART_REPL_BAUD   115200

// I2C busses
#define MICROPY_HW_I2C2_SCL         (pin_H4)
#define MICROPY_HW_I2C2_SDA         (pin_H5)
#define MICROPY_HW_I2C4_SCL         (pin_B6)
#define MICROPY_HW_I2C4_SDA         (pin_H12)

// SPI
#define MICROPY_HW_SPI1_NSS         (pin_G10)
#define MICROPY_HW_SPI1_SCK         (pin_G11)
#define MICROPY_HW_SPI1_MISO        (pin_G9)
#define MICROPY_HW_SPI1_MOSI        (pin_D7)

#define MICROPY_HW_SPI2_NSS         (pin_I0)
#define MICROPY_HW_SPI2_SCK         (pin_I1)
#define MICROPY_HW_SPI2_MISO        (pin_I2)
#define MICROPY_HW_SPI2_MOSI        (pin_I3)

//#define MICROPY_HW_SPI5_NSS         (pin_K0)
//#define MICROPY_HW_SPI5_SCK         (pin_)
//#define MICROPY_HW_SPI5_MISO        (pin_)
//#define MICROPY_HW_SPI5_MOSI        (pin_J10)

// USRSW is pulled low. Pressing the button makes the input go high.
//#define MICROPY_HW_USRSW_PIN        (pin_C13)
//#define MICROPY_HW_USRSW_PULL       (GPIO_NOPULL)
//#define MICROPY_HW_USRSW_EXTI_MODE  (GPIO_MODE_IT_RISING)
//#define MICROPY_HW_USRSW_PRESSED    (1)

// LEDs
#define MICROPY_HW_LED1             (pin_J0)    
#define MICROPY_HW_LED2             (pin_J1)
#define MICROPY_HW_LED3             (pin_J2)
#define MICROPY_HW_LED4             (pin_J3)    
#define MICROPY_HW_LED5             (pin_J4)
#define MICROPY_HW_LED6             (pin_J5)
#define MICROPY_HW_LED7             (pin_J6)    
#define MICROPY_HW_LED8             (pin_J7)
#define MICROPY_HW_LED_ON(pin)      (mp_hal_pin_high(pin))
#define MICROPY_HW_LED_OFF(pin)     (mp_hal_pin_low(pin))

// USB config
#define MICROPY_HW_USB_FS              (1)
#define MICROPY_HW_USB_VBUS_DETECT_PIN (pin_A9)
#define MICROPY_HW_USB_OTG_ID_PIN      (pin_A10)
#define MICROPY_HW_USB_CDC_NUM      (2)
#define MICROPY_HW_USB_ENABLE_CDC2  (1)

// FDCAN bus
#define MICROPY_HW_CAN1_NAME  "FDCAN1"
#define MICROPY_HW_CAN1_TX    (pin_H13)
#define MICROPY_HW_CAN1_RX    (pin_D0)

// SD card detect switch
#define MICROPY_HW_SDCARD_DETECT_PIN        (pin_C13)
#define MICROPY_HW_SDCARD_DETECT_PULL       (GPIO_PULLUP)
#define MICROPY_HW_SDCARD_DETECT_PRESENT    (GPIO_PIN_RESET)

#define MICROPY_HW_SDMMC_D0 (pin_C8)
#define MICROPY_HW_SDMMC_D1 (pin_C9)
#define MICROPY_HW_SDMMC_D2 (pin_C10)
#define MICROPY_HW_SDMMC_D3 (pin_C11)
#define MICROPY_HW_SDMMC_CK (pin_C12)
#define MICROPY_HW_SDMMC_CMD (pin_D2)

// Ethernet via RMII
#define MICROPY_HW_ETH_MDC          (pin_C1)
#define MICROPY_HW_ETH_MDIO         (pin_A2)
#define MICROPY_HW_ETH_RMII_REF_CLK (pin_A1)
#define MICROPY_HW_ETH_RMII_CRS_DV  (pin_A7)
#define MICROPY_HW_ETH_RMII_RXD0    (pin_C4)
#define MICROPY_HW_ETH_RMII_RXD1    (pin_C5)
#define MICROPY_HW_ETH_RMII_TX_EN   (pin_B11)
#define MICROPY_HW_ETH_RMII_TXD0    (pin_B12)
#define MICROPY_HW_ETH_RMII_TXD1    (pin_B13)
