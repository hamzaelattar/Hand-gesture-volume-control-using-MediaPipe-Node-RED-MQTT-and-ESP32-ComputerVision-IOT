
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(
  SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1
);

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("Erreur OLED !");
    while (true);
  }
}

void loop() {
  for (int volume = 0; volume <= 100; volume += 5) {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(15, 5);
    display.println("GESTURE VOLUME");

    display.setTextSize(2);
    display.setCursor(35, 25);
    display.print(volume);
    display.println("%");

    display.drawRect(10, 52, 108, 10, SSD1306_WHITE);
    display.fillRect(
      12, 54,
      map(volume, 0, 100, 0, 104),
      6, SSD1306_WHITE
    );

    display.display();
    delay(300);
  }
}

