package hackaton.ldthackaton.jsonService;

import com.fasterxml.jackson.databind.ObjectMapper;
import hackaton.ldthackaton.jsonDto.JsonReviewDto;
import hackaton.ldthackaton.jsonDto.JsonRootDto;
import hackaton.ldthackaton.model.Review;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
public class JsonDataProcessor {

    private final Map<String, Integer> themeToIdMap = new HashMap<>();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // Маппинг месяцев
    private final Map<String, Integer> monthMap = Map.ofEntries(
            Map.entry("Январь", 1),
            Map.entry("Февраль", 2),
            Map.entry("Март", 3),
            Map.entry("Апрель", 4),
            Map.entry("Май", 5),
            Map.entry("Июнь", 6),
            Map.entry("Июль", 7),
            Map.entry("Август", 8),
            Map.entry("Сентябрь", 9),
            Map.entry("Октябрь", 10),
            Map.entry("Ноябрь", 11),
            Map.entry("Декабрь", 12)
    );

    public List<Review> processJsonFile(String filePath) throws IOException {
        JsonRootDto rootDto = objectMapper.readValue(new File(filePath), JsonRootDto.class);

        // Инициализируем маппинг тем
        initializeThemeMapping(rootDto.getMetadata().getThemesList());

        List<Review> reviews = new ArrayList<>();

        for (JsonReviewDto jsonReview : rootDto.getTestReviewsAnalysis()) {
            reviews.addAll(convertJsonReviewToEntities(jsonReview));
        }

        return reviews;
    }

    private void initializeThemeMapping(List<String> themesList) {
        themeToIdMap.clear();
        for (int i = 0; i < themesList.size(); i++) {
            themeToIdMap.put(themesList.get(i), i + 1); // ID начинаются с 1
        }
    }

    private List<Review> convertJsonReviewToEntities(JsonReviewDto jsonReview) {
        List<Review> reviews = new ArrayList<>();

        // Парсим дату
        LocalDate reviewDate = parseDate(jsonReview.getDate());
        if (reviewDate == null) return reviews;

        int year = reviewDate.getYear();
        int month = reviewDate.getMonthValue();

        // Если есть predicted_themes, создаем записи для каждой темы
        if (jsonReview.getPredictedThemes() != null && !jsonReview.getPredictedThemes().isEmpty()) {
            for (String theme : jsonReview.getPredictedThemes()) {
                Review review = createReviewEntity(jsonReview, theme, year, month);
                reviews.add(review);
            }
        }
        // Если predicted_themes пуст, но есть theme_sentiments
        else if (jsonReview.getThemeSentiments() != null && !jsonReview.getThemeSentiments().isEmpty()) {
            for (String theme : jsonReview.getThemeSentiments().keySet()) {
                Review review = createReviewEntity(jsonReview, theme, year, month);
                reviews.add(review);
            }
        }
        // Если вообще нет тем, создаем одну запись без темы
        else {
            Review review = createReviewEntity(jsonReview, null, year, month);
            reviews.add(review);
        }

        return reviews;
    }

    private Review createReviewEntity(JsonReviewDto jsonReview, String theme, int year, int month) {
        Review review = new Review();

        // Маппинг темы
        if (theme != null && themeToIdMap.containsKey(theme)) {
            review.setIdCategory(themeToIdMap.get(theme));
            review.setThemeCategory(theme);
        } else {
            review.setIdCategory(0); // или null, если нет темы
            review.setThemeCategory("Не определена");
        }

        review.setYear(year);
        review.setMonth(month);
        review.setRating(jsonReview.getRating());

        // Маппинг тональности
        String tonality = determineTonality(jsonReview, theme);
        review.setTonality(tonality);

        return review;
    }

    private String determineTonality(JsonReviewDto jsonReview, String theme) {
        // Приоритет 1: тональность для конкретной темы
        if (theme != null && jsonReview.getThemeSentiments() != null) {
            String themeSentiment = jsonReview.getThemeSentiments().get(theme);
            if (themeSentiment != null) {
                return mapSentimentToTonality(themeSentiment);
            }
        }

        // Приоритет 2: общая тональность
        if (jsonReview.getOverallSentiment() != null) {
            return mapSentimentToTonality(jsonReview.getOverallSentiment());
        }

        // Приоритет 3: определяем по рейтингу
        return mapRatingToTonality(jsonReview.getRating());
    }

    private String mapSentimentToTonality(String sentiment) {
        if (sentiment == null) return "neutral";

        return switch (sentiment.toLowerCase()) {
            case "negative", "neg" -> "negative";
            case "positive", "pos" -> "positive";
            default -> "neutral";
        };
    }

    private String mapRatingToTonality(Integer rating) {
        if (rating == null) return "neutral";

        return switch (rating) {
            case 1, 2 -> "negative";
            case 3 -> "neutral";
            case 4, 5 -> "positive";
            default -> "neutral";
        };
    }

    private LocalDate parseDate(String dateStr) {
        if (dateStr == null || dateStr.trim().isEmpty()) {
            return LocalDate.now(); // или null, в зависимости от логики
        }

        try {
            // Пробуем разные форматы дат
            DateTimeFormatter[] formatters = {
                    DateTimeFormatter.ofPattern("dd.MM.yyyy"),
                    DateTimeFormatter.ofPattern("MM.yyyy"),
                    DateTimeFormatter.ofPattern("yyyy-MM-dd")
            };

            for (DateTimeFormatter formatter : formatters) {
                try {
                    return LocalDate.parse(dateStr, formatter);
                } catch (Exception e) {
                    // Пробуем следующий формат
                }
            }

            // Если ни один формат не подошел
            return LocalDate.now();
        } catch (Exception e) {
            return LocalDate.now();
        }
    }

    // Метод для получения маппинга тем (может пригодиться)
    public Map<String, Integer> getThemeMapping() {
        return Collections.unmodifiableMap(themeToIdMap);
    }
}