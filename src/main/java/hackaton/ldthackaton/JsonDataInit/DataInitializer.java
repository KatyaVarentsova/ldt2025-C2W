package hackaton.ldthackaton.JsonDataInit;

import hackaton.ldthackaton.jsonService.JsonDataProcessor;
import hackaton.ldthackaton.model.Review;
import hackaton.ldthackaton.repository.ReviewRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    private final ReviewRepository reviewRepository;
    private final JsonDataProcessor jsonDataProcessor;

    public DataInitializer(ReviewRepository reviewRepository, JsonDataProcessor jsonDataProcessor) {
        this.reviewRepository = reviewRepository;
        this.jsonDataProcessor = jsonDataProcessor;
    }

    @Override
    @Transactional
    public void run(String... args) throws Exception {
        if (reviewRepository.count() == 0) {
            try {
                String jsonFilePath = "C:/Users/ersho/IdeaProjects/LDT-Hackaton/src/main/java/hackaton//ldthackaton/data/banking_analysis_results.json";
                List<Review> reviews = jsonDataProcessor.processJsonFile(jsonFilePath);

                // Пакетное сохранение
                int batchSize = 1000;
                for (int i = 0; i < reviews.size(); i += batchSize) {
                    int end = Math.min(i + batchSize, reviews.size());
                    List<Review> batch = reviews.subList(i, end);
                    reviewRepository.saveAll(batch);
                    reviewRepository.flush(); // Принудительно сохраняем пачку
                    System.out.println("Saved batch: " + end + "/" + reviews.size());
                }

                System.out.println("Successfully loaded " + reviews.size() + " reviews into database");
            } catch (Exception e) {
                System.err.println("Error loading data from JSON: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
}