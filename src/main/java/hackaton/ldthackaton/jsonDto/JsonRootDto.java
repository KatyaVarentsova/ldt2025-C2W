package hackaton.ldthackaton.jsonDto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class JsonRootDto {
    private Metadata metadata;
    private List<JsonReviewDto> testReviewsAnalysis;

    // Геттеры и сеттеры
    public Metadata getMetadata() { return metadata; }
    public void setMetadata(Metadata metadata) { this.metadata = metadata; }

    @JsonProperty("test_reviews_analysis")
    public List<JsonReviewDto> getTestReviewsAnalysis() { return testReviewsAnalysis; }
    public void setTestReviewsAnalysis(List<JsonReviewDto> testReviewsAnalysis) { this.testReviewsAnalysis = testReviewsAnalysis; }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Metadata {
        private List<String> themesList;

        @JsonProperty("themes_list")
        public List<String> getThemesList() { return themesList; }
        public void setThemesList(List<String> themesList) { this.themesList = themesList; }
    }
}