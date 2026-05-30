import 'package:geolocator/geolocator.dart';
import 'package:pray_times/pray_times.dart';
import 'package:hijri/hijri.dart';
import '../core/constants.dart';

class PrayerService {
  final PrayTimes _prayTimes = PrayTimes();

  Future<Position?> getCurrentLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return null;

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) return null;
    }

    if (permission == LocationPermission.deniedForever) return null;

    return await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
            accuracy: LocationAccuracy.high));
  }

  List<Map<String, String>> getTodayPrayerTimes(double lat, double lon) {
    DateTime date = DateTime.now();
    _prayTimes.setLocation(lat, lon);
    _prayTimes.setDate(date.year, date.month, date.day);
    _prayTimes.setMethod(AppConstants.calcMethod);
    
    List<String> times = _prayTimes.getTimes();
    List<String> names = [
      "Fajr",
      "Sunrise",
      "Dhuhr",
      "Asr",
      "Maghrib",
      "Isha"
    ];

    List<Map<String, String>> formattedTimes = [];
    for (int i = 0; i < names.length; i++) {
      formattedTimes.add({
        "name": names[i],
        "time": times[i],
      });
    }
    return formattedTimes;
  }

  String getHijriDate() {
    final Hijri hijri = Hijri.now();
    return "${hijri.day} ${hijri.monthName} ${hijri.year} AH";
  }

  double calculateQibla(double lat, double lon) {
    // Calculate bearing
    double dLon = (AppConstants.kaabaLon - lon);
    double y = (AppConstants.kaabaLon - lon) * (AppConstants.kaabaLon - lon);
    double x = (AppConstants.kaabaLon - lon) * (AppConstants.kaabaLon - lon);
    double yRadians = _degreesToRadians(dLon);
    double latRadians = _degreesToRadians(lat);
    double kaabaLatRadians = _degreesToRadians(AppConstants.kaabaLat);
    
    double bearing = _radiansToDegrees(math.atan2(math.sin(yRadians), 
        (math.cos(latRadians) * math.tan(kaabaLatRadians)) - 
        (math.sin(latRadians) * math.cos(yRadians))));
        
    return (bearing + 360) % 360;
  }
  
  // Helpers
  double _degreesToRadians(double degree) => degree * (3.14159265359 / 180);
  double _radiansToDegrees(double radian) => radian * (180 / 3.14159265359);
}

import 'dart' as math; // Needed for math.atan2, math.sin etc
