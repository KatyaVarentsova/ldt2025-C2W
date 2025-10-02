package hackaton.ldthackaton.util;

import java.util.HashMap;
import java.util.Map;

public class ThemeMapper {
    private static final Map<String, Integer> THEME_TO_ID = new HashMap<>();

    static {
        THEME_TO_ID.put("Банкоматы", 1);
        THEME_TO_ID.put("Дебетовые карты", 2);
        THEME_TO_ID.put("Кешбэк и бонусы", 3);
        THEME_TO_ID.put("Комиссии и тарифы", 4);
        THEME_TO_ID.put("Кредитные карты", 5);
        THEME_TO_ID.put("Кредиты и займы", 6);
        THEME_TO_ID.put("Мобильное приложение", 7);
        THEME_TO_ID.put("Обслуживание в офисах", 8);
        THEME_TO_ID.put("Переводы и платежи", 9);
        THEME_TO_ID.put("Техподдержка", 10);
    }

    public static Integer getId(String theme) {
        return THEME_TO_ID.get(theme);
    }

    public static boolean isValidTheme(String theme) {
        return THEME_TO_ID.containsKey(theme);
    }

    public static Map<String, Integer> getAllThemes() {
        return new HashMap<>(THEME_TO_ID);
    }
}