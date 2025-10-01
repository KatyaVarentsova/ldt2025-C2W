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

    // 2. Статистика по рейтингам
    public List<RatingStatsDto> getRatingStats() {
        List<Review> all = reviewRepository.findAll();
        Map<YearMonthKey, RatingStatsDto> map = new HashMap<>();

        for (Review review : all) {
            YearMonthKey key = new YearMonthKey(review.getYear(), review.getMonth());
            map.computeIfAbsent(key, k -> {
                RatingStatsDto dto = new RatingStatsDto();
                dto.setYear(k.year);
                dto.setMonth(MONTH_NAMES[k.month]);
                return dto;
            });

            switch (review.getRating()) {
                case 1 -> map.get(key).setStar1(map.get(key).getStar1() + 1);
                case 2 -> map.get(key).setStar2(map.get(key).getStar2() + 1);
                case 3 -> map.get(key).setStar3(map.get(key).getStar3() + 1);
                case 4 -> map.get(key).setStar4(map.get(key).getStar4() + 1);
                case 5 -> map.get(key).setStar5(map.get(key).getStar5() + 1);
            }
        }

        return new ArrayList<>(map.values());
    }

    // 3. Статистика по тональности по месяцам
    public List<TonalityStatsDto> getSentimentStatsByMonth() {
        List<Review> all = reviewRepository.findAll();
        Map<YearMonthKey, TonalityStatsDto> map = new HashMap<>();

        for (Review review : all) {
            YearMonthKey key = new YearMonthKey(review.getYear(), review.getMonth());
            map.computeIfAbsent(key, k -> {
                TonalityStatsDto dto = new TonalityStatsDto();
                dto.setYear(k.year);
                dto.setMonth(MONTH_NAMES[k.month]);
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

        return new ArrayList<>(map.values());
    }

    // 4. Общая тональность
    public TotalTonalityDto getTotalSentiment() {
        TotalTonalityDto dto = new TotalTonalityDto();
        List<Review> all = reviewRepository.findAll();

        for (Review review : all) {
            String tone = review.getTonality().toLowerCase();
            if ("negative".equals(tone)) dto.setNegative(dto.getNegative() + 1);
            else if ("neutral".equals(tone)) dto.setNeutral(dto.getNeutral() + 1);
            else if ("positive".equals(tone)) dto.setPositive(dto.getPositive() + 1);
        }

        return dto;
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

