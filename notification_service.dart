import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:timezone/timezone.dart' as tz;
import 'package:timezone/data/latest.dart' as tz;
import '../core/constants.dart';

class NotificationService {
  final FlutterLocalNotificationsPlugin notifications =
      FlutterLocalNotificationsPlugin();
  final AudioPlayer audioPlayer = AudioPlayer();

  Future<void> init() async {
    tz.initializeTimeZones();
    
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings(
        requestAlertPermission: true, requestBadgePermission: true);
        
    const initSettings = InitializationSettings(
        android: androidSettings, iOS: iosSettings);

    await notifications.initialize(initSettings);
    await audioPlayer.setSource(AssetSource('audio/takbir.mp3'));
  }

  Future<void> scheduleAdhan(String prayerName, int hour, int minute) async {
    // Simplified: Creating a unique ID based on time
    int id = hour * 60 + minute; 

    await notifications.zonedSchedule(
      id,
      "Adhan Italia",
      "Time for $prayerName - Allahu Akbar",
      _nextInstanceOfTime(hour, minute),
      NotificationDetails(
        android: AndroidNotificationDetails(
          'adhan_channel',
          'Adhan Notifications',
          channelDescription: 'Prayer time notifications',
          importance: Importance.high,
          priority: Priority.high,
          playSound: false, // We play custom audio separately
        ),
        iOS: const DarwinNotificationDetails(presentAlert: true),
      ),
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      matchDateTimeComponents: DateTimeComponents.time,
    );
  }

  Future<void> playTakbir() async {
    await audioPlayer.resume();
  }

  tz.TZDateTime _nextInstanceOfTime(int hour, int minute) {
    final now = tz.TZDateTime.now(tz.local);
    var scheduledDate = tz.TZDateTime(tz.local, now.year, now.month, now.day, hour, minute);
    if (scheduledDate.isBefore(now)) {
      scheduledDate = scheduledDate.add(const Duration(days: 1));
    }
    return scheduledDate;
  }
  
  Future<void> cancelAll() async {
    await notifications.cancelAll();
  }
}
