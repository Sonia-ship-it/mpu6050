#include <MPU6050.h>
#include <Wire.h>


MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed!");
    while (1);
  }
  Serial.println("MPU6050 connected successfully!");
}

void loop() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  float pitch = atan2(ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
  float roll  = atan2(ay, sqrt(ax * ax + az * az)) * 180.0 / PI;
  float yaw   = atan2(az, sqrt(ax * ax + ay * ay)) * 180.0 / PI; 

  Serial.print(pitch);
  Serial.print(",");
  Serial.print(roll);
  Serial.print(",");
  Serial.println(yaw);

  delay(100);
}
