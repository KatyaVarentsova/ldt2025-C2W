package hackaton.ldthackaton.repository;

import hackaton.ldthackaton.model.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByThemeCategory(String themeCategory);
    List<Review> findByTonality(String tonality);
    List<Review> findByYearAndMonth(Integer year, Integer month);
}