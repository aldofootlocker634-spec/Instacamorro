class TranslationService {
  // In a real app, use ARB files. Here is a simple Map approach for demo.
  static final Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'app_title': 'Adhan Italia',
      'prayers': 'Prayers',
      'qibla': 'Qibla',
      'settings': 'Settings',
      'fajr': 'Fajr',
      'dhuhr': 'Dhuhr',
      'asr': 'Asr',
      'maghrib': 'Maghrib',
      'isha': 'Isha',
      'enable_notifs': 'Enable Notifications',
      'theme': 'Dark Mode',
      'location_error': 'Please enable location services',
    },
    'it': {
      'app_title': 'Adhan Italia',
      'prayers': 'Preghiere',
      'qibla': 'Qibla',
      'settings': 'Impostazioni',
      'fajr': 'Fajr',
      'dhuhr': 'Dhuhr',
      'asr': 'Asr',
      'maghrib': 'Maghrib',
      'isha': 'Isha',
      'enable_notifs': 'Abilita Notifiche',
      'theme': 'Modalità Scura',
      'location_error': 'Attiva i servizi di localizzazione',
    },
    'ar': {
      'app_title': 'أذان إيطاليا',
      'prayers': 'الصلوات',
      'qibla': 'القبلة',
      'settings': 'الإعدادات',
      'fajr': 'الفجر',
      'dhuhr': 'الظهر',
      'asr': 'العصر',
      'maghrib': 'المغرب',
      'isha': 'العشاء',
      'enable_notifs': 'تفعيل الإشعارات',
      'theme': 'الوضع الداكن',
      'location_error': 'يرجى تفعيل خدمات الموقع',
    },
  };

  static String get(String locale, String key) {
    return _localizedValues[locale]?[key] ?? _localizedValues['en']![key]!;
  }
}
