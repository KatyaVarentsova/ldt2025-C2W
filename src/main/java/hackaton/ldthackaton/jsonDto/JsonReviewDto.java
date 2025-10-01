package hackaton.ldthackaton.jsonDto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public class JsonReviewDto {
    private String id;
    private String text;
    private Integer rating;
    private String date;
    private List<String> predictedThemes;
    private Map<String, String> themeSentiments;
    private String overallSentiment;

    // Геттеры и сеттеры
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }

    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }

    @JsonProperty("predicted_themes")
    public List<String> getPredictedThemes() { return predictedThemes; }
    public void setPredictedThemes(List<String> predictedThemes) { this.predictedThemes = predictedThemes; }

    @JsonProperty("theme_sentiments")
    public Map<String, String> getThemeSentiments() { return themeSentiments; }
    public void setThemeSentiments(Map<String, String> themeSentiments) { this.themeSentiments = themeSentiments; }

    @JsonProperty("overall_sentiment")
    public String getOverallSentiment() { return overallSentiment; }
    public void setOverallSentiment(String overallSentiment) { this.overallSentiment = overallSentiment; }
}