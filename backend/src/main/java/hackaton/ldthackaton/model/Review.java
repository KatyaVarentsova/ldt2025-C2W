package hackaton.ldthackaton.model;

import jakarta.persistence.*;

@Entity
@Table(name = "reviews")
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idReview;

    private Integer idCategory;
    private String themeCategory;
    private Integer year;
    private Integer month; // 1–12
    private Integer rating; // 1–5
    private String tonality; // "positive", "neutral", "negative"


    public Long getIdReview() { return idReview; }
    public void setIdReview(Long idReview) { this.idReview = idReview; }

    public Integer getIdCategory() { return idCategory; }
    public void setIdCategory(Integer idCategory) { this.idCategory = idCategory; }

    public String getThemeCategory() { return themeCategory; }
    public void setThemeCategory(String themeCategory) { this.themeCategory = themeCategory; }

    public Integer getYear() { return year; }
    public void setYear(Integer year) { this.year = year; }

    public Integer getMonth() { return month; }
    public void setMonth(Integer month) { this.month = month; }

    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }

    public String getTonality() { return tonality; }
    public void setTonality(String tonality) { this.tonality = tonality; }
}