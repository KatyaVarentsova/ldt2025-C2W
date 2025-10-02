package hackaton.ldthackaton.service;

import hackaton.ldthackaton.dto.RatingStatsDto;
import hackaton.ldthackaton.dto.ThemeDto;
import hackaton.ldthackaton.dto.TonalityStatsDto;
import hackaton.ldthackaton.dto.TotalTonalityDto;
import hackaton.ldthackaton.model.Review;
import hackaton.ldthackaton.repository.ReviewRepository;
import hackaton.ldthackaton.util.ThemeMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class DashboardService {

    @Autowired
    private ReviewRepository reviewRepository;

    private static final String[] MONTH_NAMES = {
            "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    };

    // 1. Список всех тем
    public List<ThemeDto> getAllThemes() {
        return ThemeMapper.getAllThemes().entrySet().stream()
                .map(e -> new ThemeDto(e.getValue(), e.getKey()))
                .sorted(Comparator.comparing(ThemeDto::getIdCategory))
                .collect(Collectors.toList());
    }

    public List<RatingStatsDto> getRatingStats() {
        List<Review> all = reviewRepository.findAll();
        Map<String, RatingStatsDto> map = new HashMap<>(); // ключ: "год-месяц"

        for (Review review : all) {
            // Проверяем, попадает ли отзыв в нужный период
            if (!isInTargetPeriod(review.getYear(), review.getMonth())) {
                continue;
            }

            String key = review.getYear() + "-" + review.getMonth();
            RatingStatsDto dto = map.get(key);

            if (dto == null) {
                dto = new RatingStatsDto();
                dto.setYear(review.getYear());
                dto.setMonth(MONTH_NAMES[review.getMonth()]);
                dto.setMonthNumber(review.getMonth()); // Устанавливаем числовое значение месяца
                map.put(key, dto);
            }

            // Увеличиваем счетчик для соответствующего рейтинга
            switch (review.getRating()) {
                case 1 -> dto.setStar1(dto.getStar1() + 1);
                case 2 -> dto.setStar2(dto.getStar2() + 1);
                case 3 -> dto.setStar3(dto.getStar3() + 1);
                case 4 -> dto.setStar4(dto.getStar4() + 1);
                case 5 -> dto.setStar5(dto.getStar5() + 1);
            }
        }

        // Сортируем по году и месяцу
        return map.values().stream()
                .sorted(Comparator.comparing(RatingStatsDto::getYear)
                        .thenComparing(RatingStatsDto::getMonthNumber))
                .collect(Collectors.toList());
    }

    // 3. Статистика по тональности по месяцам и по темам
    public List<TonalityStatsDto> getSentimentStatsByMonth(String theme) {
        List<Review> reviews;

        // Если тема указана - фильтруем по теме, иначе берем все отзывы
        if (theme != null && !theme.trim().isEmpty()) {
            reviews = reviewRepository.findByThemeCategory(theme);
        } else {
            reviews = reviewRepository.findAll();
        }

        Map<YearMonthKey, TonalityStatsDto> map = new HashMap<>();

        for (Review review : reviews) {
            // Проверяем, попадает ли отзыв в нужный период
            if (!isInTargetPeriod(review.getYear(), review.getMonth())) {
                continue;
            }

            YearMonthKey key = new YearMonthKey(review.getYear(), review.getMonth());
            map.computeIfAbsent(key, k -> {
                TonalityStatsDto dto = new TonalityStatsDto();
                dto.setYear(k.year);
                dto.setMonth(MONTH_NAMES[k.month]);
                dto.setMonthNumber(k.month); // Устанавливаем числовое значение месяца
                return dto;
            });

            String tone = review.getTonality().toLowerCase();
            if ("negative".equals(tone)) {
                map.get(key).setNegative(map.get(key).getNegative() + 1);
            } else if ("neutral".equals(tone)) {
                map.get(key).setNeutral(map.get(key).getNeutral() + 1);
            } else if ("positive".equals(tone)) {
                map.get(key).setPositive(map.get(key).getPositive() + 1);
            }
        }

        // Сортируем по году и месяцу
        return map.values().stream()
                .sorted(Comparator.comparing(TonalityStatsDto::getYear)
                        .thenComparing(TonalityStatsDto::getMonthNumber))
                .collect(Collectors.toList());
    }

    // 4. Общая тональность
    public TotalTonalityDto getTotalSentiment(String theme) {
        TotalTonalityDto dto = new TotalTonalityDto();
        List<Review> reviews;

        // Если тема указана - фильтруем по теме, иначе берем все отзывы
        if (theme != null && !theme.trim().isEmpty()) {
            reviews = reviewRepository.findByThemeCategory(theme);
        } else {
            reviews = reviewRepository.findAll();
        }

        for (Review review : reviews) {
            // Проверяем, попадает ли отзыв в нужный период 01.01.2024 - 31.05.2025
            if (!isInTargetPeriod(review.getYear(), review.getMonth())) {
                continue;
            }

            String tone = review.getTonality().toLowerCase();
            if ("negative".equals(tone)) dto.setNegative(dto.getNegative() + 1);
            else if ("neutral".equals(tone)) dto.setNeutral(dto.getNeutral() + 1);
            else if ("positive".equals(tone)) dto.setPositive(dto.getPositive() + 1);
        }

        return dto;
    }

    private boolean isInTargetPeriod(int year, int month) {
        // Период с января 2024 по май 2025 включительно
        if (year < 2024) return false;
        if (year == 2024) return true; // Весь 2024 год подходит
        if (year == 2025) return month <= 5; // Только январь-май 2025
        return false; // Все что после мая 2025 не подходит
    }

    // Вспомогательный класс для группировки по году и месяцу
    private static class YearMonthKey {
        final int year;
        final int month;

        YearMonthKey(int year, int month) {
            this.year = year;
            this.month = month;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            YearMonthKey that = (YearMonthKey) o;
            return year == that.year && month == that.month;
        }

        @Override
        public int hashCode() {
            return Objects.hash(year, month);
        }
    }
}


